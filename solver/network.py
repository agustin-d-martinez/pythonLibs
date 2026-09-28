import numpy as np
from .block import Block, Ground, Junction
from .node import Node, NodeTType
from .terminal import Terminal, Connection, TerminalOwner, TerminalIndex

from collections import deque, defaultdict

from scipy.sparse import coo_array
from scipy.sparse.linalg import spsolve

class Network():
    def __init__(self):
        self.blocks : list[Block] = []
        self.connections : list[Connection] = []
        self.junctions : list[Junction] = []

    def add(self, b : TerminalOwner) -> None:
        if isinstance(b, Block):
            self.add_block(b)
        elif isinstance(b, Junction):
            self.add_junction(b)
        else:
            raise TypeError('Ony 2 types available: Block and Junction')

    def add_block(self, block: Block) -> None:
        self.blocks.append(block)

    def add_junction(self, junction: Junction) -> None:
        self.junctions.append(junction)

    def connect(self, a : Terminal | Junction , b: Terminal | Junction) -> None:
        if isinstance(a, Junction):
            a = a.add_terminal()
        if isinstance(b, Junction):
            b = b.add_terminal()

        connection = Connection(a=a, b=b)
        self.connections.append(connection)
        
    def build_nodes(self):
        adjacency = self._build_adjacency()
        visited : set[Terminal] = set()
        nodes : list[Node] = []

        all_terminals = set([terminal for block in self.blocks for terminal in block.terminals.values()])
        for terminal in all_terminals:
            if terminal not in visited:
                visited.add(terminal)
                nodes.append(self._flood_fill(terminal, adjacency, visited))

        return nodes

    def _build_adjacency(self) -> dict[Terminal, list[Terminal]]:
        adjacency : dict[Terminal, list[Terminal]] = defaultdict(list)
        gnd_terminal = Terminal('GND')
        for conn in self.connections:
            if isinstance(conn.a.block, Ground):
                adjacency[conn.a].append(gnd_terminal)
                adjacency[gnd_terminal].append(conn.a)
            if isinstance(conn.b.block, Ground):
                adjacency[conn.b].append(gnd_terminal)
                adjacency[gnd_terminal].append(conn.b)
            adjacency[conn.a].append(conn.b)
            adjacency[conn.b].append(conn.a)
            

        for junction in self.junctions:
            terminals = list(junction.terminals.values())
            for t1, t2 in zip(terminals, terminals[1:]):
                adjacency[t1].append(t2)
                adjacency[t2].append(t1) 
        return adjacency

    @staticmethod
    def _flood_fill(start : Terminal, adjacency : dict[Terminal, list[Terminal]], visited : set[Terminal]) -> Node:
        node = Node()
        queue = deque([start])

        while queue:
            for next_terminal in adjacency[queue[0]]:
                if next_terminal not in visited:
                    visited.add(next_terminal)
                    queue.append(next_terminal)
            if isinstance(queue[0].block, Ground):
                node.ttype = NodeTType.GND
            node.connections.add(queue.popleft())

        return node

    def solve(self):
        nodes = self.build_nodes()
        block_idx, node_idx, n = self._build_global_index(nodes)

        eq : list[tuple[dict[int, int], int]]= []
        for block in self.blocks:
            eq += block.compute(block_idx)

        for node in nodes:
            coef = {}
            for terminal in node.physical_terminals:
                v_idx, i_idx = block_idx[terminal]
                coef[i_idx] = coef.get(i_idx, 0) + 1                # I_node1 + I_node2 + ... = 0 
            eq.append((coef, 0))             


        # Transform data from compute -> A,B matrix
        rows, cols, vals = [], [], []
        B = np.zeros(len(eq))
        for row, (dict_a, coefs_b) in enumerate(eq):
            for col, coef in dict_a.items():
                rows.append(row)
                cols.append(col)
                vals.append(coef)
            B[row] = coefs_b

        # Solve A*x=B
        A = coo_array((vals, (rows, cols)), shape=(len(eq), n)).tocsr()
        x = spsolve(A, B)
        return x, block_idx, node_idx

    def _build_global_index(self, nodes : list[Node]) -> tuple[dict[Terminal, TerminalIndex], dict[Node, int]]:
        block_index : dict[Terminal, TerminalIndex] = {}
        node_index : dict[Node, int] = {}
        n = 0
        for node in nodes:
            node_index[node] = n
            m = 0
            for term in node.physical_terminals:
                block_index[term] = TerminalIndex(n, n + m + 1)
                m += 1
            n += 1 + m

        #Non conected terminals (it shoulden't exist)
        for block in self.blocks:
            for terminal in block.terminals.values():
                if terminal not in block_index:
                    block_index[terminal] = TerminalIndex(n, n + 1)         # Terminal = (V, I)
                    n += 2         

        return block_index, node_index, n