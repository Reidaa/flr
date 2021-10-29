# is it a queue ? is it a list ? It's a QIST
# rotating list ?
# something that look like an array, fifo like a queue and accessible (only in the past) like a list

from collections.abc import MutableSequence


class Qist(MutableSequence):

    def __init__(self, size: int):
        self.__size = size
        self.__max_index = size - 1
        self.__mini_index = 0
        self.__head_index: int = 0
        self.__list = [None] * size

    def _check(self, i: int):
        if i > self.__size:
            raise IndexError("index out of range")

    def __get_head_index(self):
        return self.__head_index - 1

    def __compute_backward_index(self, i) -> int:
        # TODO: Needs improvements
        n = self.__get_head_index()
        for _ in range(abs(i)):
            n -= 1
            if n == self.__mini_index - 1:
                n = self.__max_index
        return n

    def __compute_forward_index(self, i: int) -> int:
        n = self.__get_head_index()
        for _ in range(i):
            n += 1
            if n == self.__max_index + 1:
                n = self.__mini_index
        return n

    def __len__(self):
        return self.__size

    def __getitem__(self, i: int):
        if i < 0:
            self._check(abs(i))
            return self.__list[self.__compute_backward_index(i)]
        if i >= 0:
            self._check(i)
            return self.__list[self.__compute_forward_index(i)]

    def __delitem__(self, i):
        self.__list[i] = None

    def __str__(self):
        return self.__list.__str__()

    def __repr__(self):
        return self.__list.__repr__()

    def __eq__(self, other):
        return other == self.__list

    # TODO: Decide on reversing iterator or not
    # def __iter__(self):
    #     self.iter_i = self.get_head_index()
    #     return self
    #
    # def __next__(self):
    #     if abs(self.iter_i) < self.__len__():
    #         result = self.__list[self.__compute_backward_index(self.iter_i)]
    #         self.iter_i -= 1
    #         return result
    #     else:
    #         raise StopIteration

    def __iter__(self):
        self.iter_i = 1
        return self

    def __next__(self):
        if self.iter_i <= self.__len__():
            result = self.__list[self.__compute_forward_index(self.iter_i)]
            self.iter_i += 1
            return result
        else:
            raise StopIteration

    def append(self, value) -> None:
        if self.__head_index == self.__size:
            self.__head_index = 0
        self.__list[self.__head_index] = value
        self.__head_index += 1




    def __setitem__(self, i, value):
        pass

    def insert(self, index: int, value) -> None:
        pass