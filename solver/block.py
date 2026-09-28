import numpy as np
from numpy.typing import ArrayLike
from .terminal import TerminalOwner, Terminal, TerminalIndex

class Junction(TerminalOwner):
    def __init__(self, name: str):
        super().__init__(name)
        self.value = None
        
    def add_terminal(self) -> Terminal:
        return super().add_terminal(f"{self.name}_t{len(self.terminals)}")


class Block(TerminalOwner):
    def compute(self, index : dict[Terminal, TerminalIndex]) -> list[tuple[dict[int, int], int]]:
        raise NotImplementedError("The compute method must be implemented in subclasses of Block.")

class PortNetwork(Block):
    def __init__(self, name: str, ports: int = 1):
        super().__init__(name)
        self.ports = ports

        for i in range(ports):
            self.add_terminal(f"p{i}_in")
            self.add_terminal(f"p{i}_out")

    def _port2terminal(self, port: int, out : bool = False ) -> int:
        return self.terminals[f'p{port}{"_out" if out else "_in"}']


class ZParamPortNetwork(PortNetwork):
    def __init__(self, name: str, matrix: ArrayLike):
        super().__init__(name, len(matrix))
        self.Z = np.asarray(matrix)
        if self.Z.ndim != 2 or self.Z.shape[0] != self.Z.shape[1]:
            raise TypeError('The Port Network Matrix must be square')

    def compute(self, index) -> list[tuple[dict[int, int], int]]:
        v, i = [], []
        for n in range(self.ports):                     # In
            aux = index[self._port2terminal(n)]
            v += [aux.v]
            i += [aux.i]
        for n in range(self.ports):                     # Out
            aux = index[self._port2terminal(n, True)]
            v += [aux.v]
            i += [aux.i]

        eq = []
        for n in range(self.ports):
            eq.append(({i[n]:1, i[n + self.ports]:1}, 0))        # Current continuity in port.

            eq_dict = {v[n]:1, v[n+self.ports]:-1} 
            for m in range(self.ports):
                eq_dict[i[n]] = eq_dict.get(i[m], 0) - self.Z[n,m] 
            eq.append((eq_dict, 0))

        return eq


class Resistance(Block):
    def __init__(self, name, value):
        super().__init__(name)
        self.R = value
        self.add_terminal('1')
        self.add_terminal('2')

    def compute(self, index : dict[Terminal, TerminalIndex]) -> list[tuple[dict[int, int], int]]:
        t1 = self.terminals['1']
        t2 = self.terminals['2']

        v1, i1 = index[t1]
        v2, i2 = index[t2]

        eq = [
            ({i1: 1, i2:1}, 0),                     # I1 + I2 = 0
            ({v1: 1, v2:-1, i1:-self.R}, 0)         # V1 - V2 - I1*R = 0
        ]
        return eq

class VoltageSource(Block):
    def __init__(self, name, value):
        super().__init__(name)
        self.voltage = value
        self.add_terminal('1')
        self.add_terminal('2')

    def compute(self, index : dict[Terminal, tuple[int, int]]) -> list[tuple[dict[int, int], int]]:
        t1 = self.terminals['1']
        t2 = self.terminals['2']

        v1, i1 = index[t1]
        v2, i2 = index[t2]

        eq = [
            ({i1: 1, i2:1}, 0),                     # I1 + I2 = 0
            ({v1: 1, v2:-1}, self.voltage)          # V1 - V2 = V 
        ]
        return eq

class Ground(Block):
    def __init__(self, name):
        super().__init__(name)
        self.add_terminal('1')

    def compute(self, index):
        v = index[self.terminals['1']].v
        eq = [
            ({v:1}, 0)
        ]

        return eq
    