from ..array import ArrayKind, ArrayType
from ..bit import BitType, VCC, GND
from ..wire import wiredefaultclock
from .verilog import find
from collections import OrderedDict

def get_type(port):
    if isinstance(port, ArrayType):
        width = port.N
    else:
        assert isinstance(port, BitType)
        width = 1
    return "UInt<{}>".format(width)

def get_name(port):
    if port is VCC: return "UInt<1>(\"h1\")"
    if port is GND: return "UInt<1>(\"h0\")"

    if isinstance(port, ArrayType):
        if not port.iswhole(port.ts):
            # the sequence of values is concantenated
            port = [get_name(i) for i in port.ts]
            port.reverse()
            return '{' + ','.join(port) + '}'
    assert not port.anon()
    return port.name.qualifiedname(sep="_")

def compileinstance(instance):
    instance_name = str(instance.name)
    s = "inst {} of {}\n".format(instance_name, str(instance.__class__.__name__))
    for name, port in instance.interface.ports.items():
        if port.isinput():
            value = port.value()
            if not value:
                print('Warning (firrtl): input', str(port), 'not connected to an output')
                value = port
        else:
            value = port
        if isinstance(port, ArrayType):
            for index, subport in enumerate(port.ts):
                s += "{}.{}[{}] <= {}\n".format(instance_name, name, index, get_name(subport))
        else:
            s += "{}.{} <= {}\n".format(instance_name, name, get_name(value))
    return s

def compiledefinition(cls):

    # for now only allow Bit or Array(n, Bit)
    for name, port in cls.interface.ports.items():
        if isinstance(port, ArrayKind):
            if not isinstance(port.T, BitKind):
                print('Error: Argument', port, 'must be a an Array(n,Bit)')

    s = 'module {} :\n'.format(cls.__name__)
    for name, port in cls.interface.ports.items():
        if port.isinput():
            direction = "output"
        elif port.isoutput():
            direction = "input"
        else:
            raise NotImplementedError()  # Does FIRRTL have an inout?
        s += '{} {} : {}\n'.format(direction, name, get_type(port))

    import re
    if cls.firrtl:
        s += cls.firrtl + '\n'
    else:
        # declare a wire for each instance output
        for instance in cls.instances:
            for port in instance.interface.ports.values():
                if port.isoutput():
                    s += 'wire {} : {}\n'.format(get_name(port), get_type(port))

        #print('compile instances')
        # emit the structured verilog for each instance
        for instance in cls.instances:
            wiredefaultclock(cls, instance)
            s += compileinstance(instance)

        # assign to module output arguments
        for input in cls.interface.inputs():
            output = input.value()
            if output:
                iname = get_name(input)
                oname = get_name(output)
                s += 'assign %s = %s;\n' % (iname, oname)

    return "\n  ".join(s.splitlines())


def compile(main):
    defn = find(main,OrderedDict())

    code = 'circuit main :\n'
    for k, v in defn.items():
         print('compiling', k)
         code += "  " + "\n  ".join(compiledefinition(v).splitlines()) + '\n'
    return code

