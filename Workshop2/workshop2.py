# TODO
# import libraries

import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn import metrics

def readfile(filename):
    examples_msg = []
    examples_labels = []
    for line in open(filename):
        example = json.loads(line.strip())
        for msg, tlabel in zip(example['messages'], example['sender_labels']):
            examples_msg.append(msg)
            examples_labels.append(tlabel)
    return examples_msg, np.array(examples_labels)

train = readfile('Workshop2/mod-train.jsonl')
dev = readfile('Workshop2/mod-train.jsonl')

print(train[0])


text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', LogisticRegression(solver='saga', penalty=None))])

text_clf.fit(train[0], train[1])

predicted = text_clf.predict(dev[0])

print(np.mean(predicted == dev[1]))
print(metrics.classification_report(dev[1], predicted))
print(metrics.confusion_matrix(dev[1], predicted))




