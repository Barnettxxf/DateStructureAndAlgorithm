# -*- coding: utf-8 -*-

__author__ = 'barnett'

from .link_list import LNode


class StackUnderflow(ValueError):
    pass


class SStack(object):
    """ based on simple list """

    def __init__(self):
        self._elems = []

    def is_empty(self):
        return self._elems is []

    def top(self):
        if self.is_empty():
            raise StackUnderflow('in SStack.top()')
        return self._elems[-1]

    def push(self, elem):
        self._elems.append(elem)

    def pop(self):
        if self.is_empty():
            raise StackUnderflow('in SStack.pop()')
        return self._elems.pop()


class LStack(object):
    """ based on link list"""

    def __init__(self):
        self._top = None

    def is_empty(self):
        return self._top is None

    def top(self):
        if self.is_empty():
            raise StackUnderflow('in LStack.top()')
        return self._top.elem

    def push(self, elem):
        self._top = LNode(elem, self._top)

    def pop(self):
        if self.is_empty():
            raise StackUnderflow('in LStack.pop()')
        p = self._top
        self._top = p.next
        return p.elem


"""
Application example
example one: checking brackets is in pair or not in a text;
example two: realization of simple calculation expression recognition
example three: bag problem
"""


# Example One
def check_parens(text):
    """ checking brackets is in pair or not """

    parens = "()[]{}"
    open_parens = '({['
    opposite = {')': '(', '}': '{', ']': '['}

    def parentheses(text):
        """ generator for searching brackets """
        i, text_len = 0, len(text)
        while True:
            while i < text_len and text[i] not in parens:
                i += 1
            if i > text_len:
                return
            yield text[i], i
            i += 1

    st = SStack()
    for pr, i in parentheses(text):
        if pr in open_parens:
            st.push(pr)
        elif st.pop() != opposite[pr]:
            print('Unmatching is found at', i, 'for', pr)
        else:
            print("macth one in location", i, 'for', pr)

    print('All parentheses are correctly matched.')
    return True


# Example Two
class ESStack(SStack):
    def depth(self):
        return len(self._elems)


priority = {'(': 1, '+': 3, '-': 3, '*': 5, '/': 5}
infix_operators = '+-*/()'


def tokens(line):
    i, llen = 0, len(line)
    while i < llen:
        while line[i].isspace():
            i += 1
        if i >= llen:
            break
        if line[i] in infix_operators:
            yield line[i]
            i += 1
            continue

        j = i + 1
        while j < llen and not line[j].isspace() and line[j] not in infix_operators:
            if (line[j] == 'e' or line[j] == 'E') and j + 1 < llen and line[j + 1] == '-':
                j += 1
            j += 1
        yield line[i:j]
        i = j


def suffix_exp_evaluator(line):
    return line.split()


def suf_exp_evaluator(exp):
    operator = '+-*/'
    st = ESStack()

    for x in exp:
        if x not in operator:
            st.push(x)
            continue

        if st.depth() < 2:
            raise SyntaxError('Short of operand(s).')
        a = st.pop()
        b = st.pop()

        if x == '+':
            c = b + a
        elif x == '-':
            c = b - a
        elif x == '*':
            c = b * a
        else:
            c = b / a

        st.push(c)

    if st.depth() == 1:
        return st.pop()
    raise SyntaxError('Extra operand(s).')


def trans_infix_sufix(line):
    st = SStack()
    exp = []

    for x in tokens(line):
        if x not in infix_operators:
            exp.append(x)
        elif st.is_empty() or x == '(':
            st.push(x)
        elif x == ")":
            while not st.is_empty() and st.top() != '(':
                exp.append(st.top())
            if st.is_empty():
                raise SyntaxError('Missing "(".')
            st.pop()
        else:
            while not st.is_empty() and priority[st.top()] >= priority[x]:
                exp.append(st.pop())
            st.push(x)

    while not st.is_empty():
        if st.top() == '(':
            raise SyntaxError('Extra "(".')
        exp.append(st.pop())

    return exp


def test_trans_infix_sufix(s):
    print(s)
    print(trans_infix_sufix(s))
    print("Value: ", suf_exp_evaluator(trans_infix_sufix(s)))


# Example three
