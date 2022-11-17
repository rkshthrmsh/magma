from collections import OrderedDict
import io

import hwtypes
import pyverilog.dataflow.visit
import pyverilog.vparser.parser
from ..array import Array
from ..bit import Bit
from ..bits import Bits
from ..circuit import Circuit
from ..interface import IO
from ..passes.tsort import tsort
from ..t import In, Out, InOut, Type
from .verilog_importer import (ImportMode, MultipleModuleDeclarationError,
                               MultiplePortDeclarationError, VerilogImporter,
                               VerilogImportError)
from .verilog_utils import int_const_str_to_int
from magma.bitutils import clog2
from magma.conversions import concat
from magma.stubify import stubify
from magma.wire import wire


class PyverilogImportError(VerilogImportError):
    pass


def _evaluate_node(node, params):
    """Evaluates the pyverilog node @node"""
    if isinstance(node, pyverilog.vparser.ast.IntConst):
        return int_const_str_to_int(node.value)
    if isinstance(node, pyverilog.vparser.ast.Rvalue):
        return _evaluate_node(node.var, params)
    if isinstance(node,
                  (pyverilog.vparser.ast.Minus, pyverilog.vparser.ast.Uminus)):
        l = _evaluate_node(node.left, params)
        r = _evaluate_node(node.right, params)
        return l - r
    if isinstance(node, pyverilog.vparser.ast.Plus):
        l = _evaluate_node(node.left, params)
        r = _evaluate_node(node.right, params)
        return l + r
    if isinstance(node, pyverilog.vparser.ast.Divide):
        l = _evaluate_node(node.left, params)
        r = _evaluate_node(node.right, params)
        return l // r  # floor division
    if isinstance(node, pyverilog.vparser.ast.Times):
        l = _evaluate_node(node.left, params)
        r = _evaluate_node(node.right, params)
        return l * r  # floor division
    if isinstance(node, pyverilog.vparser.ast.Identifier):
        return params[node.name]
    if isinstance(node, pyverilog.vparser.ast.SystemCall):
        syscall = node.syscall
        if syscall == "clog2":
            operand = _evaluate_node(node.children()[0], params)
            return clog2(operand)
        raise PyverilogImportError(
            f"Unsupported verilog system call: {syscall}")
    raise PyverilogImportError(f"Unsupported expression: {type(node)}")


def _get_width(width, param_map, metadata=None):
    """Evaluates width.msb, width.lsb and returns their difference"""
    msb = _evaluate_node(width.msb, param_map)
    lsb = _evaluate_node(width.lsb, param_map)
    if metadata is not None:
        metadata["msb"] = msb
        metadata["lsb"] = lsb
    return msb - lsb + 1


def _parse_port(port):
    """
    Returns the pair (name: str, io: Union[(Input|Output|Inout), None]), where
    the second element is the pyverilog encoded type of the input, or None (if
    the port list name-only.
    """
    if isinstance(port, pyverilog.vparser.parser.Ioport):
        io = port.first
        return (io.name, io)
    if isinstance(port, pyverilog.vparser.parser.Port):
        return (port.name, None)
    # Not expected to reach here.
    raise PyverilogImportError(f"Unsupported port type: {type(port)}")


def _magma_type(io, params):
    """
    Returns the magma type corresponding to @io, which is a pyverilog Input,
    Output, or Inout.
    """
    direction = InOut
    if isinstance(io, pyverilog.vparser.parser.Input):
        direction = In
    elif isinstance(io, pyverilog.vparser.parser.Output):
        direction = Out

    typ = Bit
    if io.width is not None:
        width = _get_width(io.width, params)
        typ = Bits[width]

    # Generate multidimensional arrays if necessary. Note that we guard with
    # hasattr to make this backwards compatible.
    if hasattr(io, "dimensions") and io.dimensions is not None:
        for length in reversed(io.dimensions.lengths):
            width = _get_width(length, params)
            typ = Array[width, typ]

    return direction(typ)


def _get_lines(src, start, end):
    return "\n".join(src.split("\n")[start - 1:end])


class _ModuleGraphVisitor(pyverilog.dataflow.visit.NodeVisitor):
    """
    This implementation of pyverilog's NodeVisitor collects all module
    definitions in the root node.
    """
    def __init__(self):
        self.defns = OrderedDict()

    def visit_ModuleDef(self, defn):
        if defn.name in self.defns:
            raise MultipleModuleDeclarationError(defn.name)
        self.defns[defn.name] = defn


class PyverilogImporter(VerilogImporter):
    """Implementation of VerilogImporter using pyverilog"""
    def __init__(self, type_map):
        super().__init__(type_map)
        self._magma_defn_to_pyverilog_defn = {}

    def _import_defn(self, defn, mode):
        ports = {}
        default_params = {}
        # Parse module declaration for parameters (and default values) and port
        # declarations.
        for param_list in defn.paramlist.params:
            for param in param_list.list:
                default_params[param.name] = _evaluate_node(
                    param.value, default_params)
        for port in defn.portlist.ports:
            name, io = _parse_port(port)
            if name in ports:
                raise MultiplePortDeclarationError(name)
            ports[name] = io
        # Check that the port declaration is not mixed-style, i.e. either all
        # declared in the module declaration, or all declared in the body.
        is_io = (p is not None for p in ports.values())
        if not all(is_io) and any(is_io):
            raise MixedPortDeclarationsError()
        # Iterate on the body of the moudle definition for paramters (and
        # default values) and port declarations.
        for child in defn.children():
            if not isinstance(child, pyverilog.vparser.parser.Decl):
                continue
            for subchild in child.children():
                if isinstance(subchild, pyverilog.vparser.parser.Parameter):
                    default_params[subchild.name] = _evaluate_node(
                        subchild.value, default_params)
                elif isinstance(subchild, (pyverilog.vparser.parser.Input,
                                           pyverilog.vparser.parser.Output,
                                           pyverilog.vparser.parser.Inout)):
                    ports[subchild.name] = subchild
        # Convert pyverilog ports to magma types and define a magma circuit.
        decl = {n: self.map_type(n, _magma_type(port, default_params))
                for n, port in ports.items()}

        class _FromVerilog(Circuit):
            name = defn.name
            io = IO(**decl)

        return _FromVerilog, default_params

    def import_(self, src, mode):
        parser = pyverilog.vparser.parser.VerilogParser()
        ast = parser.parse(src)
        visitor = _ModuleGraphVisitor()
        visitor.visit(ast)
        for name, defn in visitor.defns.items():
            circ, default_params = self._import_defn(defn, mode)
            self._magma_defn_to_pyverilog_defn[circ] = defn
            if mode is ImportMode.DEFINE:
                circ.verilogFile = _get_lines(src, defn.lineno, defn.end_lineno)
                circ.verilog_source = src
            circ.coreir_config_param_types = {
                k: type(v)
                for k, v in default_params.items()
            }
            circ.default_kwargs = default_params
            self.add_module(circ)


def _show(node, **kwargs):
    buf = io.StringIO()
    node.show(buf=buf, **kwargs)
    return buf.getvalue()


def _update_unique(dct, mapping):
    for k, v in mapping.items():
        assert k not in dct, (k)
        dct[k] = v


def _get_instances(defn):
    for child in defn.children():
        if isinstance(child, pyverilog.vparser.parser.Instance):
            yield child
        elif isinstance(child, pyverilog.vparser.parser.InstanceList):
            yield from child.instances


def _get_wires(defn):
    for child in defn.children():
        if not isinstance(child, pyverilog.vparser.parser.Decl):
            continue
        for subchild in child.children():
            if not isinstance(subchild, pyverilog.vparser.parser.Wire):
                continue
            yield subchild


def _wire_directed_to_undirected(directed, undirected):
    if isinstance(directed, Bits[1]):
        directed = directed[0]
    if isinstance(undirected, Bits[1]):
        undirected = undirected[0]
    if directed.is_input():
        if isinstance(undirected, Type) and undirected.is_input():
            return False
        directed @= undirected
        return True
    if directed.is_output():
        undirected @= directed
        return True
    if directed.is_inout():
        wire(directed, undirected)
        return True
    raise Exception()


def _get_offset(name, metadata):
    try:
        msb, lsb = metadata[name].values()
    except KeyError:
        return 0
    return lsb


def _evaluate_arg(node, values, metadata={}):
    if isinstance(node, pyverilog.vparser.parser.IntConst):
        return _evaluate_node(node, {})
    if isinstance(node, pyverilog.vparser.parser.Identifier):
        return values[node.name]
    if isinstance(node, pyverilog.vparser.parser.Pointer):
        offset = _get_offset(node.var.name, metadata)
        value = _evaluate_arg(node.var, values)
        index = _evaluate_node(node.ptr, {})
        return value[index - offset]
    if isinstance(node, pyverilog.vparser.parser.Partselect):
        offset = _get_offset(node.var.name, metadata)
        value = _evaluate_arg(node.var, values)
        msb = _evaluate_node(node.msb, {})
        lsb =  _evaluate_node(node.lsb, {})
        return value[lsb - offset : msb + 1 - offset]
    if isinstance(node, pyverilog.vparser.parser.Concat):
        return concat(*(_evaluate_arg(n, values) for n in reversed(node.list)))
    raise Exception()


def _process_port_connections(
        pyverilog_inst,
        magma_inst,
        containing_magma_defn,
        wires,
        metadata,
):
    stash = []
    magma_values = {}
    magma_values.update(wires)
    magma_values.update(containing_magma_defn.interface.ports)
    for child in pyverilog_inst.children():
        if not isinstance(child, pyverilog.vparser.parser.PortArg):
            continue
        magma_port = getattr(magma_inst, child.portname)
        magma_arg = _evaluate_arg(child.argname, magma_values, metadata)
        wired = _wire_directed_to_undirected(magma_port, magma_arg)
        if not wired:
            stash.append((magma_port, magma_arg))
    return stash


class PyverilogNetlistImporter(PyverilogImporter):
    def __init__(self, type_map, stdcells):
        super().__init__(type_map)
        self._stdcells = stdcells

    def import_(self, src, mode):
        super().import_(src, mode)
        if mode is not ImportMode.DEFINE:
            return
        modules = {
            defn.name: defn
            for defn in self._magma_defn_to_pyverilog_defn.keys()
        }
        try:
            _update_unique(modules, self._stdcells)
        except AssertionError as e:
            raise MultipleModuleDeclarationError(e.args[0])

        for magma_defn, pyverilog_defn in (
                self._magma_defn_to_pyverilog_defn.items()
        ):
            metadata = {}
            mod = False
            wires = {}
            for wire in _get_wires(pyverilog_defn):
                assert (
                    not wire.signed
                    and wire.dimensions is None
                    and wire.value is None
                )
                T = Bit
                if wire.width is not None:
                    width = _get_width(wire.width, {}, metadata.setdefault(wire.name, {}))
                    T = Bits[width]
                mod = True
                assert wire.name not in wires
                wires[wire.name] = T(name=wire.name)
            stash = []
            for pyverilog_inst in _get_instances(pyverilog_defn):
                instance_module = modules[pyverilog_inst.module]
                mod = True
                with magma_defn.open():
                    magma_inst = instance_module(name=pyverilog_inst.name)
                    stash += _process_port_connections(
                        pyverilog_inst,
                        magma_inst,
                        magma_defn,
                        wires,
                        metadata,
                    )
                    stubify(magma_inst.interface)
            for inst_port, driver in stash:
                inst_port @= driver.trace()
            if mod:
                magma_defn.verilogFile = ""
                magma_defn.verilog_source = ""
                magma_defn._is_definition = True
                stubify(magma_defn)
