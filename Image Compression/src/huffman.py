import numpy as np
from graphviz import Digraph

from utils.log_business import MyLogger


class Node:
    def __init__(self, symbols: set = None, freq: int = 0):
        if not symbols:
            symbols = set()
        self.symbols = symbols
        self.freq = freq
        self.left = None
        self.right = None

    def __str__(self):
        return f"{self.symbols}:{self.freq}"

    def __repr__(self):
        return f"{self.symbols}:{self.freq}"

    def update(self):
        if isinstance(self.left, Node):
            self.symbols = self.symbols.union(self.left.symbols)
            self.freq += self.left.freq

        if isinstance(self.right, Node):
            self.symbols = self.symbols.union(self.right.symbols)
            self.freq += self.right.freq


class HuffmanTree:
    def __init__(self, log_path):
        self.logger = MyLogger('src.huffman', log_path)

    def create_tree(self, freq_dict: dict[any, int]) -> Node:
        self.logger.info('creating tree')
        nodes = []
        for symbol, freq in freq_dict.items():
            nodes.append(Node({symbol}, freq))

        self.logger.debug('nodes list created')

        self.logger.debug('ready to create tree')
        while len(nodes) > 1:
            nodes.sort(key=lambda x: x.freq)
            parent = Node()
            parent.left = nodes.pop(0)
            parent.right = nodes.pop(0)
            parent.update()
            nodes.append(parent)

        self.logger.debug('tree created')
        return nodes[0]

    def encode(self, root: Node, symbol: any) -> str:
        if not root.symbols or root.symbols == {symbol}:
            return ''

        if symbol in root.left.symbols:
            return '0' + self.encode(root.left, symbol)

        if symbol in root.right.symbols:
            return '1' + self.encode(root.right, symbol)

        self.logger.error(f'character {symbol} not in tree')
        raise ValueError(f'{symbol} not in tree')

    @staticmethod
    def decode(root: Node, binary: str) -> np.ndarray:
        decoded = []
        node = root
        for code in binary:
            node = node.left if code == '0' else node.right
            if len(node.symbols) == 1:
                decoded.append(list(node.symbols)[0])
                node = root

        return np.array(decoded)

    def encode_array(self, array: list[any]):
        """
        Encodes an array of characters using a tree

            Parameters
            ----------
                array : list of str
                    list of characters to encode

            Returns
            -------
                out : dict
                    dictionary of characters and their encoded codes
        """
        self.logger.info('encoding array')
        freq_dict = {}
        for symbol in array:
            freq_dict[symbol] = freq_dict.get(symbol, 0) + 1

        self.logger.debug('frequency dictionary created')
        root = self.create_tree(freq_dict)

        self.logger.debug('tree created')
        encoded_dict = {}
        for symbol in freq_dict.keys():
            encoded_dict[symbol] = self.encode(root, symbol)

        self.logger.debug('encoded dictionary created')
        return root, encoded_dict

    def visualize_tree(self, root, dot=None, dpi=300, size='10,10', engine='dot'):
        if dot is None:
            dot = Digraph(engine=engine)
            dot.attr('node', shape='circle', style='filled', color='lightblue')
            dot.attr(size=size)
            dot.attr(dpi=str(dpi))

        # Limit the length of the string representation of root.symbols
        if len(root.symbols) == 1:
            label = f"{str(root.symbols)}:{root.freq}"
        else:
            label = f"{len(root.symbols)}:{root.freq}"
        dot.node(str(id(root)), label=label)
        if root.left is not None:
            dot.edge(str(id(root)), str(id(root.left)), label='0')
            self.visualize_tree(root.left, dot=dot, dpi=dpi, size=size, engine=engine)
        if root.right is not None:
            dot.edge(str(id(root)), str(id(root.right)), label='1')
            self.visualize_tree(root.right, dot=dot, dpi=dpi, size=size, engine=engine)
        return dot
