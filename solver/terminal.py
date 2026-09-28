from __future__ import annotations
from typing import NamedTuple


class TerminalIndex(NamedTuple):
    v: int
    i: int

class Terminal:
    def __init__(self, name : str, block : TerminalOwner | None = None):
        self.name = name
        self.block : TerminalOwner = block
        self.value = None

    def __repr__(self):
        return f"Terminal(name={self.name}, block={self.block.name if self.block else None})"

class Connection():
    def __init__(self, a : Terminal, b : Terminal):
        self.a = a
        self.b = b

class TerminalOwner():
    def __init__(self, name : str):
        self.name = name
        self.terminals : dict[str, Terminal] = {}

    def add_terminal(self, name : str ):
        t = Terminal(name, self)
        self.terminals[name] = t
        return t
