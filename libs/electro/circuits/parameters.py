from typing import Literal
import numpy as np
from numpy.typing import ArrayLike
from dataclasses import dataclass, field

PARAMETER_TYPE = Literal['Z', 'Y', 'G', 'H', 'T', 'S', 'St']

# terminals: 2 per port. 0,1 (port1); 2,3 (port2); 4,5 (port3); ....
# 0 --███-- 2
# 1 --███-- 3

# X_VAR: ([OUTPUTS], [INPUTS])
Z_VAR = (['V1', 'V2'], ['I1', 'I2'])
Y_VAR = (['I1', 'I2'], ['V1', 'V2'])
H_VAR = (['V1', 'I2'], ['I1', 'V2'])
G_VAR = (['I1', 'V2'], ['V1', 'I2'])
T_VAR = (['V1', 'I1'], ['V2', '-I2'])
S_VAR = (['b1', 'b2'], ['a1', 'a2'])
ST_VAR = (['a1', 'b1'], ['b2', 'a2'])

class Block():
    _id_counter = 0
    def __init__(self, matrix : ArrayLike, type : PARAMETER_TYPE, name : str | None = None ):
        self.matrix = np.asarray(matrix)
        self.type = type
        
        self._id_counter += 1
        self.name = name if name else f"{self.type}_{self._id_counter}"

        if self.type in ('H', 'G', 'T') and self.matrix.shape[0] != 2:
            raise ValueError(f"The matrix type {self.type} is only defined as a TWO-port Network.")

    def equation(self) -> np.ndarray:
    # 0 = M * (V|I)
    # 0 = (1|-Z) * (V|I)
    # 0 = (Y|-1) * (V|I)    
        n = self.matrix.shape[0]
        match self.type:
            case 'Z':
                mat = np.hstack((np.eye(n),-self.matrix))

            case 'Y':
                mat = np.hstack((self.matrix, -np.eye(n)))

            case 'G':
                mat = np.array([[-self.matrix[0,0], 0, 1, -self.matrix[0,1]],
                                [-self.matrix[1,0], 1, 0, -self.matrix[1,1]]])

            case 'H':
                mat = np.array([[1, -self.matrix[0,1], -self.matrix[0,0], 0],
                                [0, -self.matrix[1,1], -self.matrix[1,0], 1]])
            case 'T':
                mat = np.array([[1, -self.matrix[0,0], 0, self.matrix[0,1]],
                                [0, -self.matrix[1,0], 1, self.matrix[1,1]]])

            case _:
                pass
            
        return mat
    
## Defaulted networks #################################################
class Z_Network(Block):
    def __init__(self, matrix : ArrayLike, name : str | None = None ):
        super().__init__(matrix=matrix, type='Z', name=name)

class Y_Network(Block):
    def __init__(self, matrix : ArrayLike, name : str | None = None ):
        super().__init__(matrix=matrix, type='Z', name=name)

class G_Network(Block):
    def __init__(self, matrix : ArrayLike, name : str | None = None ):
        super().__init__(matrix=matrix, type='Z', name=name)

class H_Network(Block):
    def __init__(self, matrix : ArrayLike, name : str | None = None ):
        super().__init__(matrix=matrix, type='Z', name=name)

class T_Network(Block):
    def __init__(self, matrix : ArrayLike, name : str | None = None ):
        super().__init__(matrix=matrix, type='Z', name=name)

class S_Network(Block):
    def __init__(self, matrix : ArrayLike, zo : complex = 50, name : str | None = None ):
        self.zo = zo
        super().__init__(matrix=matrix, type='Z', name=name)


## Transformations #################################################3
# From Z:
def z_to_y(z : Block) -> Block:
    matriz = np.linalg.inv(z.matrix)
    return Block(matrix=matriz, type='Y')

def z_to_h(z : Block) -> Block:
    N = z.matrix.shape[0]
    if N != 2:
        raise ValueError('H-Parameters are Two-port network only')
    matrix = _matrix_rearranger(z, Z_VAR, H_VAR)
    return Block(matrix=matrix, type='H', name=z.name)

def z_to_g(z : Block) -> Block:
    N = z.matrix.shape[0]
    if N != 2:
        raise ValueError('G-Parameters are Two-port network only')
    matrix = _matrix_rearranger(z, Z_VAR, G_VAR)
    return Block(matrix=matrix, type='G', name=z.name)

def z_to_t(z : Block) -> Block:
    N = z.matrix.shape[0]
    if N != 2:
        raise ValueError('T-Parameters are Two-port network only')
    
    # Eliminate - sign
    t_var = [[m.replace('-', '') for m in i] for i in T_VAR]

    out_matrix = _matrix_rearranger(z, Z_VAR, t_var)

    # Invert signal 
    for i, arg in enumerate(T_VAR[0]):
        if '-' in arg:
            out_matrix[i, :] = -1* out_matrix[i,:]
    for i, arg in enumerate(T_VAR[1]):
        if '-' in arg:
            out_matrix[:, i] = -1* out_matrix[:,i]
    return Block(matrix=out_matrix, type='T', name=z.name)

# From y:
def y_to_z(y: Block) -> Block:
    matrix = np.linalg.inv(y.matrix)
    return Block(matrix=matrix, type='Z', name=y.name)

def y_to_h(y : Block) -> Block:
    N = y.matrix.shape[0]
    if N != 2:
        raise ValueError('H-Parameters are Two-port network only')
    
    matrix = _matrix_rearranger(y, Y_VAR, H_VAR)
    return Block(matrix=matrix, type='H', name=y.name)

def y_to_g(y : Block) -> Block:
    N = y.matrix.shape[0]
    if N != 2:
        raise ValueError('G-Parameters are Two-port network only')
    matrix = _matrix_rearranger(y, Y_VAR, G_VAR)
    return Block(matrix=matrix, type='G', name=y.name)

def y_to_t(y : Block) -> Block:
    N = y.matrix.shape[0]
    if N != 2:
        raise ValueError('T-Parameters are Two-port network only')
    
    # Eliminate - sign
    t_var = [[m.replace('-', '') for m in i] for i in T_VAR]

    out_matrix = _matrix_rearranger(y, Y_VAR, t_var)

    # Invert signal 
    for i, arg in enumerate(T_VAR[0]):
        if '-' in arg:
            out_matrix[i, :] = -1* out_matrix[i,:]
    for i, arg in enumerate(T_VAR[1]):
        if '-' in arg:
            out_matrix[:, i] = -1* out_matrix[:,i]
    return Block(matrix=out_matrix, type='T', name=y.name)

# From G:
def g_to_h(g : Block) -> Block:
    matriz = np.linalg.inv(g.matrix)
    return Block(matrix=matriz, type='H', name=g.name)

def g_to_z(g : Block) -> Block:
    N = g.matrix.shape[0]
    if N != 2:
        raise ValueError('H-Parameters are Two-port network only')
    matrix = _matrix_rearranger(g, G_VAR, Z_VAR)
    
    return Block(matrix=matrix, type='Z', name=g.name)

def g_to_y(g : Block) -> Block:
    N = g.matrix.shape[0]
    if N != 2:
        raise ValueError('G-Parameters are Two-port network only')
    matrix = _matrix_rearranger(g, G_VAR, Y_VAR)
    return Block(matrix=matrix, type='Y', name=g.name)

def g_to_t(g : Block) -> Block:
    N = g.matrix.shape[0]
    if N != 2:
        raise ValueError('T-Parameters are Two-port network only')
    
    # Eliminate - sign
    t_var = [[m.replace('-', '') for m in i] for i in T_VAR]

    out_matrix = _matrix_rearranger(g, G_VAR, t_var)

    # Invert signal 
    for i, arg in enumerate(T_VAR[0]):
        if '-' in arg:
            out_matrix[i, :] = -1* out_matrix[i,:]
    for i, arg in enumerate(T_VAR[1]):
        if '-' in arg:
            out_matrix[:, i] = -1* out_matrix[:,i]
    return Block(matrix=out_matrix, type='T', name=g.name)

# From H:
def h_to_g(h: Block) -> Block:
    matriz = np.linalg.inv(h.matrix)
    return Block(matrix=matriz, type='G', name=h.name)

def h_to_z(h : Block) -> Block:
    N = h.matrix.shape[0]
    if N != 2:
        raise ValueError('H-Parameters are Two-port network only')
    
    matrix = _matrix_rearranger(h, H_VAR, Z_VAR)
    return Block(matrix=matrix, type='Z', name=h.name)

def h_to_y(h : Block) -> Block:
    N = h.matrix.shape[0]
    if N != 2:
        raise ValueError('G-Parameters are Two-port network only')
    matrix = _matrix_rearranger(h, H_VAR, Y_VAR)
    return Block(matrix=matrix, type='Y', name=h.name)

def h_to_t(h : Block) -> Block:
    N = h.matrix.shape[0]
    if N != 2:
        raise ValueError('T-Parameters are Two-port network only')
    
    # Eliminate - sign
    t_var = [[m.replace('-', '') for m in i] for i in T_VAR]

    out_matrix = _matrix_rearranger(h, H_VAR, t_var)

    # Invert signal 
    for i, arg in enumerate(T_VAR[0]):
        if '-' in arg:
            out_matrix[i, :] = -1* out_matrix[i,:]
    for i, arg in enumerate(T_VAR[1]):
        if '-' in arg:
            out_matrix[:, i] = -1* out_matrix[:,i]
    return Block(matrix=out_matrix, type='T', name=h.name)

# From s:
def s_to_st(s: Block) -> Block:
    N = s.matrix.shape[0]
    if N != 2:
        raise ValueError('ST-Parameters are Two-port network only')
    matrix = _matrix_rearranger(s, S_VAR, ST_VAR)
    return Block(matrix=matrix, type='ST', name=s.name)

# From st:
def st_to_s(st: Block) -> Block:
    N = st.matrix.shape[0]
    if N != 2:
        raise ValueError('ST-Parameters are Two-port network only')
    matrix = _matrix_rearranger(st, ST_VAR, S_VAR)
    return Block(matrix=matrix, type='S', name=st.name)


def _matrix_rearranger(matriz : np.ndarray,
                       actual_arrange : tuple[list, list],
                       new_arrange : tuple[list, list]):
    # actual_arrange : (INPUTS, OUTPUTS)
    # new_arange : (INPUTS, OUTPUTS)
    
    # OUTPUT = M * INPUT
    # 0 = OUTPUT - M * INPUT
    # 0 = 1 * OUTPUT - M * INPUT
    # 0 = (1 | -M) * (OUTPUT | INPUT)
    
    # Rearrange de col y fil
    
    # 0 = (M_new) * (OUT | IN)
    # 0 = M_new_left * OUT + M_new_right * IN
    # OUT = - inv(M_new_left) * M_new_right * IN
    # RESULTADO = - inv(M_new_left) * M_new_right 
    
    N = matriz.shape[0]
    M_tot = np.hstack((np.eye(N), -matriz))

    #print(M_tot)

    out_in_og : list[str] = actual_arrange[1] + actual_arrange[0]
    out_in_new = new_arrange[1] + new_arrange[0]
    new_idx_order = [out_in_og.index(x) for x in out_in_new]
    
    M_new = np.zeros((N, 2*N))
    for i in range(2*N):
        M_new[:, i] = M_tot[:, new_idx_order[i]] 
    
    M_left = M_new[:,:N]
    M_right = M_new[:,N:]
    res = - np.linalg.inv(M_left) @ M_right
    return res


class Node():
    def __init__(self):
        self.connections: list[tuple[Block, int]] = [] 

    def connect(self, block : Block, terminal : int ):
        self.connections.append((block, terminal))

class Constrains():
    def __init__(self):
        self.node1 : Node
        self.node2 : Node
        self.val : float

class VoltageSource(Constrains):
    def __init__(self, nodep : Node, noden : Node, value : float):
        self.node1 = nodep
        self.node2 = noden
        self.val = value

class CurrentSource(Constrains):
    def __init__(self, node1 : Node, node2 : Node, value : float):
        self.node1 = node1
        self.node2 = node2
        self.val = value

class Impedance(Constrains):
    def __init__(self, node1 : Node, node2 : Node, value : float):
        self.node1 = node1
        self.node2 = node2
        self.val = value

class Ground(Constrains):
    def __init__(self, node : Node):
        self.node1 = node
        self.node2 = node
        self.val = 0


class Network():
    def __init__(self):
        self.blocks : list[Block] = []
        
        self.nodes : list[Node] = []
        self.terminal_to_node : dict[tuple[Block, int],Node] = {}

        self.constrains : list[Constrains] = []
    
    ### ADD ###########################################################################################
    def add_block(self, block : Block) -> None:
        self.blocks.append(block)
    
    def add_load(self, block1 : Block, block2 : Block, terminal1: int, terminal2: int, value : float ) -> None:
        node1 = self.terminal_to_node.get((block1, terminal1))
        if not node1:
            node1 = Node()
            node1.connect(block1, terminal1)
            self.nodes.append(node1)
            self.terminal_to_node[(block1, terminal1)] = node1
        
        node2 = self.terminal_to_node.get((block2, terminal2))
        if not node2:
            node2 = Node()
            node2.connect(block2, terminal2)
            self.nodes.append(node2)
            self.terminal_to_node[(block2, terminal2)] = node2

        self.constrains.append(Impedance(node1, node2, value))

    #def add_load(self, block : Block, port: int, value : float ) -> None:
    #    term1, term2 = self._port_to_terminal_num(block, port)
    #    self.add_load(block=block, terminal1=term1, terminal2=term2)

    def add_voltage_source(self, blockp : Block, blockn : Block, terminalp: int, terminaln: int, value : float) -> None:
        nodep = self.terminal_to_node.get((blockp, terminalp))
        if not nodep:
            nodep = Node()
            nodep.connect(blockp, terminalp)
            self.nodes.append(nodep)
            self.terminal_to_node[(blockp, terminalp)] = nodep
        
        noden = self.terminal_to_node.get((blockn, terminaln))
        if not noden:
            noden = Node()
            noden.connect(blockn, terminaln)
            self.nodes.append(noden)
            self.terminal_to_node[(blockn, terminaln)] = noden

        self.constrains.append(VoltageSource(nodep, noden, value))

    def add_current_source(self, blockp : Block, blockn : Block, terminalp: int, terminaln: int, value : float ) -> None:
        nodep = self.terminal_to_node.get((blockp, terminalp))
        if not nodep:
            nodep = Node()
            nodep.connect(blockp, terminalp)
            self.nodes.append(nodep)
            self.terminal_to_node[(blockp, terminalp)] = nodep
        
        noden = self.terminal_to_node.get((blockn, terminaln))
        if not noden:
            noden = Node()
            noden.connect(blockn, terminaln)
            self.nodes.append(noden)
            self.terminal_to_node[(blockn, terminaln)] = noden

        self.constrains.append(CurrentSource(nodep, noden, value))

    def add_ground(self, block : Block, terminal : int) -> None:
        node = self.terminal_to_node.get((block, terminal))
        if not node:
            node = Node()
            node.connect(block, terminal)
            self.nodes.append(node)
            self.terminal_to_node[(block, terminal)] = node
        
        self.constrains.append(Ground(node))


    ### CONNECTIONS ####################################################################################
    def connect(self, block1 : Block, block2: Block, terminal1: int, terminal2: int) -> None:
        node = self.terminal_to_node.get((block1, terminal1))
        if node:
            node.connect(block2, terminal2)
            self.terminal_to_node[(block2, terminal2)] = node
            return
        
        node = self.terminal_to_node.get((block2, terminal2))
        if node:
            node.connect(block1, terminal1)
            self.terminal_to_node[(block1, terminal1)] = node
            return
        
        node = Node()
        node.connect(block1, terminal1)
        node.connect(block2, terminal2)
        self.nodes.append(node)
        self.terminal_to_node[(block1, terminal1)] = node
        self.terminal_to_node[(block2, terminal2)] = node

    def series_series(self, block1 : Block, block2 : Block ) -> None:
        self.connect(block1=block1, block2=block2, terminal1=1, terminal2=0 )
        self.connect(block1=block1, block2=block2, terminal1=3, terminal2=2 )

    def parallel_parallel(self, block1 : Block, block2 : Block) -> None:
        self.connect(block1=block1, block2=block2, terminal1=0, terminal2=0 )
        self.connect(block1=block1, block2=block2, terminal1=1, terminal2=1 )
        self.connect(block1=block1, block2=block2, terminal1=2, terminal2=2 )
        self.connect(block1=block1, block2=block2, terminal1=3, terminal2=3 )

    def parallel_series(self, block1 : Block, block2 : Block) -> None:
        self.connect(block1=block1, block2=block2, terminal1=0, terminal2=0 )
        self.connect(block1=block1, block2=block2, terminal1=1, terminal2=1 )

        self.connect(block1=block1, block2=block2, terminal1=3, terminal2=2 )

    def series_parallel(self, block1 : Block, block2 : Block) -> None:
        self.connect(block1=block1, block2=block2, terminal1=1, terminal2=0 )

        self.connect(block1=block1, block2=block2, terminal1=2, terminal2=2 )
        self.connect(block1=block1, block2=block2, terminal1=3, terminal2=3 )

    def cascade(self, block1 : Block, block2 : Block) -> None:
        self.connect(block1=block1, block2=block2, terminal1=2, terminal2=0)
        self.connect(block1=block1, block2=block2, terminal1=3, terminal2=1)


    def series_port(self, block1 : Block, block2 : Block, port1 : int, port2: int) -> None:
        _, term1b = self._port_to_terminal_num(block1, port1)
        term2a, _ = self._port_to_terminal_num(block2, port2)

        self.connect(block1=block1, block2=block2, terminal1=term1b, terminal2=term2a)

    def parallel_port(self, block1 : Block, block2 : Block, port1 : int, port2: int) -> None:
        term1a, term1b = self._port_to_terminal_num(block1, port1)
        term2a, term2b = self._port_to_terminal_num(block2, port2)

        self.connect(block1=block1, block2=block2, terminal1=term1a, terminal2=term2a)
        self.connect(block1=block1, block2=block2, terminal1=term1b, terminal2=term2b)

    def cascade_port(self, block1 : Block, block2 : Block, port1 : int, port2 : int) -> None:
        self.parallel_port(block1, block2, port1, port2)



    def solve(self):
        mat = self._create_system_matriz()
    
    def _create_system_matriz(self) -> np.ndarray:
# La matriz tendra la forma:
# 0 = M * (V|I, Vnodo|Inodo)
# 0 = [1-Z] [V|I]
# 0 = [...] [Vnodo|Inodo]
# Vnodo: Relaciones de tensión. Eg.: V1 = Vnodo0 - Vnodo1 -> 0 = -V1 0 0 0 Vnodo0 -Vnodo1   -> 0 = [-V1 0 0 0 1 -1] * (V|I|Vnod)
#                               Eg.: I1 = I2 + I3 -> 0 = 0 0 0 -I1 I2 I3                    -> 0 = [0 0 0 -1 1 1] * (V|I|Vnod)
      
        mat = []
        for block in self.blocks:
            mat  += block.equation()

        # Definir dims max.
        # Crear mat = np.zeros(dims max)
        # Cargar matrices en columnas y filas correspondientes. mat[idxs_row][idxs_col] = matriz_bloque ?
        
        # Cargar nodos. Añado filas debajo con las tensiones. Cada nodo es una tensión. 
        return
    
    def _create_constrain_matriz(self) -> np.ndarray:
        pass
        # Crear matriz de constrains para cada valor. v1 = 5    -> E = [5 0 0 0 0 0 0 ]
        # 0 = M * (V|I|Vnodo) - E

    ### HELPERS ##################################################################################3## 
    def _port_to_terminal_num(self, block : Block, port : int) -> tuple[int, int]:
        # Ports defined from 1 to N.
        # Terminals defines as 0,1 (port1); 2,3 (port2); 4,5 port(3) ...
        if port > block.matrix.shape[0]:
            raise ValueError(f"serched for port {port}. Block {block.name} with maximum port {block.matrix.shape[0]}")
        terminal = port * 2 - 1

        return (terminal - 1, terminal) 

    def _find_node(self, block : Block, terminal : int) -> (Node | None):
        for node in self.nodes:
            if (block, terminal) in node.connections:
                return node

        return None 