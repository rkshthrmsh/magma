from magma.simulator import PythonSimulator
from magma.bit_vector import BitVector

class Coroutine:
    """
    Makes the initial call to __next__ upon construction to immediately
    start the routine.

    Overrides __getattr__ to support inspection of the local variables
    """
    def __init__(self, *args, **kwargs):
        self.reset(*args, **kwargs)

    @classmethod
    def definition(cls, *args, **kwargs):
        return cls._definition(*args, **kwargs)

    def reset(self, *args, **kwargs):
        self.co = self.definition(*args, **kwargs)
        next(self.co)

    def __getattr__(self, key):
        return self.co.gi_frame.f_locals[key]

    def send(self, *args):
        return self.co.send(*args)

    def __next__(self):
        return next(self.co)

    def next(self):
        return self.__next__()

def coroutine(func):
    class _Coroutine(Coroutine):
        _definition = func

    return _Coroutine


def check(circuit, sim, number_of_cycles):
    simulator = PythonSimulator(circuit, clock=circuit.CLK)
    for cycle in range(number_of_cycles):
        for i in range(2):
            simulator.step()
            simulator.evaluate()
        # Coroutine has an implicit __next__ call on construction so it already
        # is in it's initial state
        for name, port in circuit.interface.ports.items():
            if port.isinput():  # circuit output
                assert getattr(sim, name) == BitVector(simulator.get_value(getattr(circuit, name)))
        next(sim)

def testvectors(circuit, sim, number_of_cycles, inputs_generator=None):
    outputs = []
    inputs = []
    for cycle in range(number_of_cycles):
        out_ports = {}
        in_ports = {}
        for name, port in circuit.interface.ports.items():
            if name == "CLK":
                continue
            if port.isinput():  # circuit output
                out_ports[name] = getattr(sim, name)
            if port.isoutput():  # circuit input
                in_ports[name] = getattr(inputs_generator, name)
        outputs.append(out_ports)
        inputs.append(in_ports)
        if in_ports:
            sim.send(in_ports)
        else:
            next(sim)
        next(inputs_generator)
    return inputs, outputs
