
"""
Counting Tokens

Write code to count the frequency of all tokens in the input data.

You will be provided with a document. You should:

Split the document up on whitespace to get words/tokens

Look up each word/token in the provided vocabulary (if it is not in the vocabulary, ignore that word/token)

Count how often each word/token appears in the document

Return a list of (token_id, count) pairs, for only the words/tokens that appear in the document

Example
Input arguments:

"Chocolate is delicious"

{"Chocolate": 0, "is": 1, "delicious": 2} 

Return:

[(0, 1), (1, 1), (2, 1)]
"""

# This is the function you need to implement
def count_words(text: str, vocab: dict[str, int]) -> list[tuple[int, int]]:
    """Count the frequency of each word in a document.

    Args:
        text (str): the text of a document
        vocab (dict[str, int]): a dictionary that maps from strings to integers, where each string is a token and each integer is an ID

    Returns:
        list[tuple[int, int]]: A list of tuples, where each tuple has the ID of a word and the count of its frequency
    """
    # TODO
    res = {}
    for i in text.split(" "):
        ind = vocab[i]
        res[ind] = res.get(ind, 0) + 1
    return list(res.items())

