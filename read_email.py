import sys
import os
import codecs
import email
import math
from random import shuffle
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer

ham = 0
spam = 1
base_path = "datasets/"
folders = [("easy_ham", ham), ("hard_ham", ham), ("spam", spam)]

def parseFolder(foldername):
	null_count = 0
	path = base_path + foldername + "/"
	feature_list = []
	for filename in os.listdir(path):
		if filename == ".DS_Store":
			continue
		f = open(path+filename, 'r')
		content = email.message_from_file(f)
		sender = content['Sender']
		payload = ""
		if not content.is_multipart():
			payload = content.get_payload()
			if payload != None:
				try:
					features = str(payload)
					feature_list.append(str('Nigga'))
				except ValueError:
					null_count += 1
					print len(payload)
	
		# if content.is_multipart():
		# 	for payload in content.get_payload():
		#  		if payload.is_multipart():
		# 			feature_list.append(payload.get_payload())
		# else:
		# 	feature_list.append(content.get_payload())
	return feature_list

# Parse different datasets
y = []
feature_list = []
for foldername, value in folders:
	result = parseFolder(foldername)
	feature_list.extend(result)
	y.extend([value] * len(result))

print "LENGTH: ", len(y)

# Shuffle 
n = len(y)
feature_list_shuf = []
y_shuf = []
index_shuf = range(n)
shuffle(index_shuf)
for i in index_shuf:
    feature_list_shuf.append(feature_list)
    y_shuf.append(y)

# Partition
partition = 0.5
size_training = int(math.floor(partition*n))

vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)
processed_list = vectorizer.fit_transform(feature_list_shuf)

training_x = processed_list[0:size_training]
training_y = y[0:size_training]
test_x = processed_list[size_training:n]
test_y = y[size_training:n]

#Train classifier
clf = svm.SVC()
clf.fit(training_x, training_y)

#Check classifier
prediction = clf.predict(test_x)
correct = [i for i,j in zip(prediction, test_y) if i==j]
correct = len(correct)
print correct*100/len(test_x)