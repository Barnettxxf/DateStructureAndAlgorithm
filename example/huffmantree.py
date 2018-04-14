# -*- coding: utf-8 -*-
from DateStructureAndAlgorithm.bintree import BinTree, BinTNode, PrioQueue

__author__ = 'barnett'


class HTNode(BinTNode):
    def __lt__(self, othernode):
        return self.data < othernode.data


class HuffmanPrioQ(PrioQueue):
    def number(self):
        return len(self._elems)


def huffman_tree(weights):
    trees = HuffmanPrioQ()
    for w in weights:
        trees.enqueue(HTNode(w))
    while trees.number() > 1:
        t1 = trees.dequeue()
        t2 = trees.dequeue()
        x = t1.data + t2.data
        trees.enqueue(HTNode(x, t1, t2))
    return trees.dequeue()
