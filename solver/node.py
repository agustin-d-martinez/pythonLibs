from .block import Block
from .terminal import Terminal
from typing import Any
from enum import Enum

class NodeTType(Enum):
    ANY = '1'
    GND = '2'

class Node():
    def __init__(self):
        self.connections : set[Terminal]= set()
        self.ttype : str | NodeTType = NodeTType.ANY
        self.value : Any = None

    @property
    def physical_terminals(self) -> set[Terminal]:
        return {t for t in self.connections if isinstance(t.block, Block)}
    
    def __repr__(self):
        return f"Node(connections={[t.name for t in self.connections]}, value={self.value})"