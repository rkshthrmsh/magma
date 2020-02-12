from magma import *


def test_input_as_output(caplog):
    magma.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.O, buf.I)
    assert caplog.records[0].msg == """\
\033[1mtests/test_wire/test_errors.py:11\033[0m: Using `main.O` (an input) as an output
>>     wire(main.O, buf.I)"""
    magma.config.set_debug_mode(False)


def test_output_as_input(caplog):
    magma.config.set_debug_mode(True)
    A = DeclareCircuit('A', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    wire(main.I, a.O)
    assert caplog.records[0].msg == """\
\033[1mtests/test_wire/test_errors.py:25\033[0m: Using `main.a.O` (an output) as an input
>>     wire(main.I, a.O)"""
    magma.config.set_debug_mode(False)


def test_multiple_outputs_to_input_warning(caplog):
    magma.config.set_debug_mode(True)
    A = DeclareCircuit('A', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bits[2]), "O", Out(Bit))

    a = A()
    wire(main.I[0], a.I)
    wire(main.I[1], a.I)
    assert caplog.records[0].msg == """\
\033[1mtests/test_wire/test_errors.py:40\033[0m: Adding the output `main.I[1]` to the wire `main.a.I` which already has output(s) `[main.I[0]]`
>>     wire(main.I[1], a.I)"""
    magma.config.set_debug_mode(False)


def test_muliple_outputs_circuit(caplog):
    magma.config.set_debug_mode(True)
    A = DeclareCircuit('A', "I", In(Bit), "O", Out(Bit), "U", Out(Bit))

    main = DefineCircuit("main", "I", In(Bits(2)), "O", Out(Bit))

    a = A()
    wire(a, main.I)
    assert caplog.records[0].msg == """\
\033[1mtests/test_wire/test_errors.py:48\033[0m: Can only wire circuits with one output. Argument 0 to wire `main.a` has outputs [inst0.O, inst0.U]
>>     wire(a, main.I)"""
    magma.config.set_debug_mode(False)


def test_muliple_outputs_circuit(caplog):
    magma.config.set_debug_mode(True)
    A = DeclareCircuit('A', "I", In(Bit), "J", In(Bit), "O", Out(Bit), "U", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    a(main)
    assert caplog.records[0].msg == """\
\033[1mtests/test_wire/test_errors.py:68\033[0m: Number of inputs is not equal to the number of outputs, expected 2 inputs, got 1. Only 1 will be wired.
>>     a(main)"""
    magma.config.set_debug_mode(False)


def test_no_inputs_circuit(caplog):
    magma.config.set_debug_mode(True)
    A = DeclareCircuit('A', "O", Out(Bit), "U", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    wire(main.I, a)
    assert caplog.records[0].msg == """\
\033[1mtests/test_wire/test_errors.py:82\033[0m: Wiring an output to a circuit with no input arguments, skipping
>>     wire(main.I, a)"""
    magma.config.set_debug_mode(False)


def test_muliple_inputs_circuit(caplog):
    magma.config.set_debug_mode(True)
    A = DeclareCircuit('A', "I", In(Bit), "J", In(Bit), "O", Out(Bit), "U", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    wire(main.I, a)
    assert caplog.records[0].msg == """\
\033[1mtests/test_wire/test_errors.py:96\033[0m: Wiring an output to a circuit with more than one input argument, using the first input main.a.I
>>     wire(main.I, a)"""
    magma.config.set_debug_mode(False)


def test_no_key(caplog):
    magma.config.set_debug_mode(True)
    A = DeclareCircuit('A', "I", In(Bit), "J", In(Bit), "O", Out(Bit), "U", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = A()
    a(K=main.I)
    assert caplog.records[0].msg == """\
\033[1mtests/test_wire/test_errors.py:110\033[0m: Instance main.a does not have input K
>>     a(K=main.I)"""
    magma.config.set_debug_mode(False)


def test_const_array_error(caplog):
    magma.config.set_debug_mode(True)
    Buf = DeclareCircuit('Buf', "I", In(Array[1, Bit]), "O", Out(Array[1, Bit]))

    main = DefineCircuit("main", "O", Out(Array[1, Bit]))

    buf = Buf()

    wire(1, buf.I)
    wire(buf.O, main.O)

    assert caplog.records[0].msg == """\
\033[1mtests/test_wire/test_errors.py:125\033[0m: Cannot wire 1 (type=<class 'int'>) to main.buf.I (type=Array[1, In(Bit)]) because conversions from IntegerTypes are only defined for Bits, not general Arrays
>>     wire(1, buf.I)"""
    magma.config.set_debug_mode(False)
