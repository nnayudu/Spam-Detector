import sys
import os
import codecs
import email
from random import shuffle
from sklearn import svm

ham = 0
spam = 1
base_path = "datasets/"
folders = [("easy_ham", ham), ("hard_ham", ham), ("spam", spam)]

def parseFolder(foldername):
	path = base_path + foldername + "/"
	feature_list = []
	for filename in os.listdir(path):
		if filename == ".DS_Store":
			continue
		f = open(path+filename, 'r')
		content = email.message_from_file(f)
		features = (content.get_param('Return-Path'), content.get_payload())
		feature_list.append(features)
	
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
for foldername,value in folders:
	result = parseFolder(foldername)
	feature_list = feature_list + result
	y = y + ([value] * len(result))

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
size_training = math.floor(partition*n)
training_x = feature_list[0:size_training]
training_y = y[0:size_training]
test_x = feature_list[size_training:n]
test_y = y[size_training:n]

#Train classifier
clf = svm.SVC()
clf.fit(training_x, training_y)

#Check classifier
prediction = clf.predict(test_x)
correct = [i for i,j in zip(prediction, test_y) if i==j]
correct = len(correct)
print correct*100/len(test_x)