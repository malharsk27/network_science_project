import dataset
import readability
import information
import textProp
import numpy as np
from sklearn.svm import SVC

features_train = []
labels_train = []

dataset.createDataset()
data = dataset.data
data = sorted(data, key=lambda k: k['qId'])

count = 0
for row in data:
    featureVector = []
    ts = readability.TextStatistics()
    tp = textProp.TextProperties()
    inf = information.Informativity()
    totalEntropy = 0
    model, stats = inf.markov_model(inf.chars(row['answerBody']), 3)
    for prefix in stats:
        totalEntropy = totalEntropy + inf.entropy(stats, stats[prefix])
    featureVector.append(abs(totalEntropy))  # information
    featureVector.append(tp.relevancy(row['answerBody'], row['qBody'], row['qTags']))  # relevancy
    featureVector.append(tp.UniqueWords(row['answerBody']))  # unique
    featureVector.append(tp.NonstopWords(row['answerBody']))  # nonstop
    featureVector.append(tp.subjective(row['answerBody']))  # subjectivity
    featureVector.append(row['answerScore'] * 100)  # answerScore
    featureVector.append(row['answererDownvotes'])  # downvotes
    featureVector.append(row['answererUpvotes'])  # upvotes
    featureVector.append(row['answerCommCount'])  # comments
    featureVector.append(ts.text_standard(row['answerBody']))  # readability
    featureVector.append(ts.difficult_words(row['answerBody']))  # difficultWords
    featureVector.append(row['answererReputation'])  # reputation
    features_train.append(featureVector)
    label = 0
    if row['acceptAnsID'] == row['answerId']:
        label = 1
    labels_train.append(label)
    count = count + 1
    if count > 100:
        break
    print(count)

print(len(features_train))
print(len(labels_train))
# 153150
# 114626
# 109255
