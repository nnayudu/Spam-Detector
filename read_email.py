import sys
import os
import codecs
import email

path = "datasets/easy_ham"

for filename in os.listdir(path):
	if filename == ".DS_Store":
		continue
	f = open("datasets/easy_ham/"+filename, 'r')
	content = email.message_from_file(f)
	if content.is_multipart():
		for payload in content.get_payload():
			# if payload.is_multipart(): ...
			print payload.get_payload()
	else:
		print content.get_payload()
	break
