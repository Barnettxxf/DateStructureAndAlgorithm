# -*- coding: utf-8 -*-

__author__ = 'barnett'


class LNode(object):
    """ Link-List node  object """

    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_


class LinkValueError(ValueError):
    pass


class LList(object):
    """ Link-List object """

    def __init__(self):
        self._head = None

    def is_empty(self):
        return self._head is None

    def prepend(self, elem):
        self._head = LNode(elem, self._head)

    def append(self, elem):
        if self._head is None:
            self._head = LNode(elem)
            return
        p = self._head
        while p.next is not None:
            p = p.next
        p.next = LNode(elem)

    def pop(self):
        if self._head is None:
            raise LinkValueError('in pop')
        e = self._head.elem
        self._head = self._head.next
        return e

    def pop_last(self):
        if self._head is None:
            raise LinkValueError
        p = self._head
        if p.next is None:
            e = p.elem
            self._head = None
            return e
        while p.next is not None:
            p = p.next
        e = p.elem
        p.next = None
        return e

    def find(self, pred):
        """
        Pred is a judgement condition function, with operating each element in link-list.
        :param pred: a function, operating parameter elem and return bool
        :return: element that meet the judgement condition
        """
        p = self._head
        while p is not None:
            if pred(p.elem):
                return p.elem
            p = p.next

    def printall(self):
        p = self._head
        while p is not None:
            print(p.elem, end='')
            if p.next is not None:
                print(',', end='')
            p = p.next
        print('')

    def for_each(self, proc):
        """
        Operate each element in link-list
        :param proc: a function name, which operate each element in link-list
        :return: None
        """
        p = self._head
        while p is not None:
            proc(p.elem)
            p = p.next

    def elements(self):
        """ generator for link-list """
        p = self._head
        while p is not None:
            yield p.elem
            p = p.next

    def reverse(self):
        p = None
        while self._head is not None:
            q = self._head
            self._head = q.next
            q.next = p
            p = q
        self._head = p

    def sort_elem(self):
        """ insert sort algorithm, moving elements"""
        if self._head is None:
            return
        crt = self._head.next
        while crt is not None:
            x = crt.elem
            p = self._head
            while p is not crt and p.elem <= x:
                p = p.next
            while p is not crt:
                y = p.elem
                p.elem = x
                x = y
                p = p.next
            crt.elem = x
            crt = crt.next

    def sort_link(self):
        """ insert sort algorithm, moving links"""
        p = self._head
        if p is None or p.next is None:
            return
        rem = p.next
        p.next= None
        while rem is not None:
            p = self._head
            p.next = None
            while p is not None:
                p = self._head
                q = None
                while p is not None and p.elem <= rem.elem:
                    q = p
                    p = p.next
                if q is None:
                    self._head = rem
                else:
                    q.next = rem
                q = rem
                rem = rem.next
                q.next = p


class LRList(LList):
    """ add _rear to increase `append` efficiency """

    def __init__(self):
        super(LRList, self).__init__()
        self._rear = None

    def prepend(self, elem):
        if self._head is None:
            self._head = elem
            self._rear = self._head
        else:
            self._head = elem

    def append(self, elem):
        if self._head is None:
            self._head = elem
            self._rear = self._head
        else:
            self._rear.next = elem
            self._rear = self._rear.next

    def pop_last(self):
        if self._head is None:
            raise LinkValueError('in pop_last')
        p = self._head
        if p.next is None:
            e = p.elem
            self._head = None
            return e
        while p.next is not None:
            p = p.next
        e = p.next.elem
        p.next = None
        self._rear = p
        return e

    def reverse(self):
        """ need finish """
        self._rear = self._head
        self._rear.next = None
        super(LRList, self).reverse()


class LCList(object):
    """ Circle link-list """

    def __init__(self):
        self._rear = None

    def is_empty(self):
        return self._rear is None

    def prepend(self, elem):
        p = LNode(elem)
        if self._rear is None:
            p.next = p
            self._rear = p
        else:
            p.next = self._rear.next
            self._rear.next = p

    def append(self, elem):
        self.prepend(elem)
        self._rear = self._rear.next

    def pop(self):
        if self._rear is None:
            raise LinkValueError('in pop')
        p = self._rear.next
        if self._rear is p:
            self._rear = None
        else:
            self._rear.next = self._rear
        return p.elem

    def pop_last(self):
        if self._rear is None:
            raise LinkValueError('in pop_last')
        p = self._rear.next
        while True:
            if p.next is self._rear:
                p.next = self._rear.next
                return p.next.elem
            p = p.next

    def printall(self):
        if self.is_empty():
            return
        p = self._rear.next
        while True:
            print(p.elem)
            if p is self._rear:
                break
            p = p.next

    def find(self, pred):
        """
        Pred is a judgement condition function, with operating each element in link-list.
        :param pred: a function, operating parameter elem and return bool
        :return: element that meet the judgement condition
        """
        p = self._rear.next
        while p is not self._rear:
            if pred(p.elem):
                return p.elem
            p = p.next

    def for_each(self, proc):
        """
        Operate each element in link-list
        :param proc: a function name, which operate each element in link-list
        :return: None
        """
        p = self._rear.next
        while p is not self._rear:
            proc(p.elem)
            p = p.next

    def elements(self):
        """ generator for link-list """
        p = self._rear.next
        while p is not self._rear:
            yield p.elem
            p = p.next


class DLNode(LNode):
    def __init__(self, elem, prev=None, next_=None):
        super(DLNode, self).__init__(elem, next_)
        self.prev = prev


class LDList(LRList):
    """ Double link-list """

    def __init__(self):
        super(LDList).__init__()

    def prepend(self, elem):
        p = DLNode(elem, None, self._head)
        if self._head is None:
            self._rear = p
        else:
            p.next.prev = p
        self._head = p

    def append(self, elem):
        p = DLNode(elem, self._rear, None)
        if self._head is None:
            self._head = p
        else:
            p.prev.next = p
        self._rear = p

    def pop(self):
        if self._head is None:
            raise LinkValueError('in pop of LDList')
        e = self._head.elem
        if self._head is not None:
            self._head.prev = None
        return e

    def pop_last(self):
        if self._head is None:
            raise LinkValueError('in pop of LDList')
        e = self._rear.elem
        self._rear = self._rear.prev
        if self._rear is None:
            self._head = None
        else:
            self._rear.next = None
        return e


class LDCList(object):
    """ Double circle link-list (need finish)"""
    pass


if __name__ == '__main__':
    mlist1 = LList()
    for i in range(10):
        mlist1.prepend(i)
    for i in range(10, 20):
        mlist1.append(i)
    mlist1.printall()
