import numpy as np
from sklearn import preprocessing, decomposition, cross_validation
from sklearn import naive_bayes
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix

clf = LinearSVC(C=0.5, class_weight='auto')
pca = decomposition.PCA(n_components=10, whiten=True)
infile = np.genfromtxt(input(“Input file:”), delimiter=',')
scaler = preprocessing.StandardScaler().fit(infile[:, :-1])
data = scaler.transform(infile[:, :-1])
data = pca.fit_transform(data)
answers = infile[:, -1]

train_vectors, test_vectors, train_answers, test_answers = cross_validation.train_test_split(
    data, answers, test_size=0.1) 
scores = cross_validation.cross_val_score(clf, train_vectors, train_answers, cv=10) 
predict = cross_validation.cross_val_predict(clf, test_vectors, test_answers, cv=10)

print("%s\nAccuracy: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std() * 2))
print(confusion_matrix(test_answers, predict))
print(classification_report(test_answers, predict,digits=3))
