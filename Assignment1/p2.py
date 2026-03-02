
"""
    In this question, you will implement classes for the three document vector representations discussed in the lecture:

Vector

Sparse Vector

Dictionary

All three classes will have the same methods:

__init__ which takes a document, represented as a list of integers. For the Vector, you will also receive the size of the vocabulary as an integer. You must give your class an instance variable, self.length that is a floating point number indicating the length of the vector (note, this is the length in vector space, |v|).

get_count which takes an integer (the ID of a word/token) and returns the count for it in this document (and zero if it does not appear)

cosine_similarity which compares two instances of the same object and calculates their cosine similarity

The evaluation code checks (a) the correctness of outputs, (b) the size of objects, and (c) the time for processing. Outputs must be exactly correct. Size must be within +/- 50% of our solution (ie, if ours uses 100 bytes you can use between 50 and 150 bytes). Time must be within +/- 70% of our solution (ie, if ours takes 1 second you must use between 0.3 and 1.7 seconds).

Implementation details
Vector - Your implementation should use a list with a count for every value in the vocabulary. You can assume that the token IDs will all be in [0, vocab_length - 1].

Sparse Vector - Store the values sorted by token ID. That way when calculating similarity you can make just one pass through the list. You move through both lists at the same time, counting common tokens and moving past those that are not in common.

Dict - When calculating similarity, if the count for a token in one object is zero you don't need to look it up in the other object.

In all cases, you should compute and store the length of the vector in the constructor (which you will need to have for the similarity computation).

Example
Constructor arguments:

doc = [2, 1, 1, 0, 3]

vocab_length = 4 

Count should be 1 for 0, 2 for 1, 1 for 2, and 1 for 3

Comparing a doc with itself should return a cosine similarity of  approximately 1

"""
   
from collections import Counter
# These are the classes you need to implement
class DocVector(object):
    def __init__(self, vocab_length: int, doc: list[int]) -> None:
        """Store a document using a list the size of the vocabulary.

        Args:
            vocab_length (int): the size of the vocabulary
            doc (list[int]): a list of token IDs that represent a document
        """
        
        # TODO
        self.doc = doc # 这个可以不要
        self.vocab_length = vocab_length # 这个可以不要
        self.s = [0] * vocab_length # 用来 存储 每个 token 的 出现次数
        # 遍历 doc 中的每个 token，如果 token 在 vocab_length 范围内，则将该 token 的出现次数加 1
        for i in doc:
            if 0 <= i < self.vocab_length: # 如果 token 在 vocab_length 范围内，则将该 token 的出现次数加 1
                self.s[i] += 1

        # 计算向量的长度 |v| = sqrt(sum(x^2))
        self.length = sum(x * x for x in self.s) ** 0.5


    def get_count(self, token: int) -> int:
        """Get how frequently a given token appeared in the document.

        Args:
            token (int): the token ID

        Returns:
            int: the frequency of the token
        """
        # TODO
        # 主要是token 是否在 vocab_length 范围内
        if 0 <= token < self.vocab_length:
            return self.s[token]
        return 0    

    def cosine_similarity(self, other: "DocVector") -> float:
        """Compare two documents of the same object type.

        Args:
            other (DocVector): the other document, also represented by this class you are defining

        Returns:
            float: the cosine similarity of the two documents
        """
        # TODO
        # 计算两个向量的点积
        dot_product = sum(a * b for a,b in zip(self.s, other.s))
        if self.length == 0 or other.length == 0: # 如果两个向量的长度为0，则返回0
            return 0.0
        return dot_product / (self.length * other.length)


class DocSparse(object):
    def __init__(self, doc: list[int]) -> None:
        """Store a document using a list, with tuples (token ID, count) for just the tokens in this document

        Args:
            doc (list[int]): a list of token IDs that represent a document
        """
        # TODO
        self.doc = doc 
        self.s = sorted(Counter(doc).items(), key=lambda x: x[0]) # 注意要求是按 token ID 排序，所以用 sorted 排序
        self.length = sum(count * count for _, count in self.s) ** 0.5 # 向量长度
        

    def get_count(self, token: int) -> int:
        """Get how frequently a given token appeared in the document.

        Args:
            token (int): the token ID

        Returns:
            int: the frequency of the token
        """
        # TODO
        # 遍历 self.s 中的每个 tuple，如果 tuple 的第一个元素（token ID）等于 token，则返回 tuple 的第二个元素（出现次数）
        for i in self.s:
            if i[0] == token:
                return i[1]
        return 0


    def cosine_similarity(self, other: "DocSparse") -> float:
        """Compare two documents of the same object type.

        Args:
            other (DocSparse): the other document, also represented by this class you are defining

        Returns:
            float: the cosine similarity of the two documents
        """
        # TODO
        # 计算两个向量的点积
        dot_product = 0.0
        # 整体思路，双指针
        i = j = 0
        len_self = len(self.s)
        len_other = len(other.s)
        while i < len_self and j < len_other:
            id_self, count_self = self.s[i] 
            id_other, count_other = other.s[j]
            if id_self == id_other: # 如果 token ID 相同，则将两个出现次数相乘，并加到点积中
                dot_product += count_self * count_other
                i += 1
                j += 1
            elif id_self < id_other: # 如果 self 的 token ID 小于 other 的 token ID，则移动 self 的指针
                i += 1
            else: # 如果 self 的 token ID 大于 other 的 token ID，则移动 other 的指针
                j += 1

        if self.length == 0 or other.length == 0:
            return 0.0
        return dot_product / (self.length * other.length)

class DocDict(object):
    def __init__(self, doc: list[int]) -> None:
        """Store a document using a dictionary with token IDs as keys and counts as values.

        Args:
            doc (list[int]): a list of token IDs that represent a document
        """
        # TODO
        self.doc = doc
        self.length = 0
        self.s = dict(Counter(doc))
        self.length = sum(self.s[x] ** 2 for x in self.s.keys()) ** 0.5



    def get_count(self, token: int) -> int:
        """Get how frequently a given token appeared in the document.

        Args:
            token (int): the token ID

        Returns:
            int: the frequency of the token
        """
        # TODO
        return self.s.get(token, 0) # 如果 token 在字典中，则返回 token 的出现次数，否则返回0


    def cosine_similarity(self, other: "DocDict") -> float:
        """Compare two documents of the same object type.

        Args:
            other (DocDict): the other document, also represented by this class you are defining

        Returns:
            float: the cosine similarity of the two documents
        """
        # TODO
        dot_product = 0.0
        for token, count_self in self.s.items():
            count_other = other.s.get(token, 0) # 如果 token 在 other 的字典中，则返回 token 的出现次数，否则返回0
            if count_other:
                dot_product += count_self * count_other # 如果 token 在两个字典中都存在，则将两个出现次数相乘，并加到点积中

        if self.length == 0 or other.length == 0: # 如果两个向量的长度为0，则返回0
            return 0.0
        return dot_product / (self.length * other.length) # 返回两个向量的点积除以两个向量的长度


if __name__ == "__main__":
    print("哈哈哈哈")
