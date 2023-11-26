from queue import PriorityQueue


class HuffmanTree:
    class __Node:
        def __init__(self, value, freq, left_child, right_child):
            self.value = value
            self.freq = freq
            self.left_child = left_child
            self.right_child = right_child

        @classmethod
        def init_leaf(cls, value, freq):
            return cls(value, freq, None, None)

        @classmethod
        def init_node(cls, left_child, right_child):
            freq = left_child.freq + right_child.freq
            return cls(None, freq, left_child, right_child)

        def is_leaf(self):
            return self.value is not None

        def __eq__(self, other):
            return (self.value, self.freq, self.left_child, self.right_child) == (
                other.value,
                other.freq,
                other.left_child,
                other.right_child,
            )

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self.freq < other.freq

        def __le__(self, other):
            return self.freq <= other.freq

        def __gt__(self, other):
            return not (self <= other)

        def __ge__(self, other):
            return not (self < other)

    def __init__(self, arr):
        q = PriorityQueue()

        # calculate frequencies and insert them into a priority queue
        for val, freq in self.__calc_freq(arr).items():
            q.put(self.__Node.init_leaf(val, freq))

        while q.qsize() >= 2:
            u = q.get()
            v = q.get()

            q.put(self.__Node.init_node(u, v))

        self.__root = q.get()

        # dictionary to store the Huffman table
        self.__value_to_bitstring = {}

    def value_to_bitstring_table(self):
        if not self.__value_to_bitstring:
            self.__create_huffman_table()
        return self.__value_to_bitstring

    def __create_huffman_table(self):
        def tree_traverse(current_node, bitstring=""):
            if current_node is None:
                return
            if current_node.is_leaf():
                self.__value_to_bitstring[current_node.value] = bitstring
                return
            tree_traverse(current_node.left_child, bitstring + "0")
            tree_traverse(current_node.right_child, bitstring + "1")

        tree_traverse(self.__root)

    def __calc_freq(self, arr):
        freq_dict = {}
        for elem in arr:
            freq_dict[elem] = freq_dict.get(elem, 0) + 1
        return freq_dict
