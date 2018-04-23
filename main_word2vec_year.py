from gensim.models import Word2Vec
import numpy as np
import time

raw_path1 = "./structured_data/thulac/CN/com_cn_main_"
raw_path2 = "./structured_data/thulac/CN/com_cn_main_uw_"
raw_path3 = "./structured_data/thulac/CN+EN/com_cn_main_"
raw_path4 = "./structured_data/thulac/CN+EN/com_cn_main_uw_"
raw_path = [raw_path1, raw_path2, raw_path3, raw_path4]

model_path1 = "./models/thulac/CN/model_"
model_path2 = "./models/thulac/CN/model_uw_"
model_path3 = "./models/thulac/CN+EN/model_"
model_path4 = "./models/thulac/CN+EN/model_uw_"
#model_path1 = "./models/thulac_groups/CN/model_"
#model_path2 = "./models/thulac_groups/CN/model_uw_"
#model_path3 = "./models/thulac_groups/CN+EN/model_"
#model_path4 = "./models/thulac_groups/CN+EN/model_uw_"


path_dict = {raw_path1: model_path1, raw_path2: model_path2, raw_path3: model_path3, raw_path4: model_path4}

for path in raw_path:
	print("For the raw_sentences stored under path:", path)
	All_Sentences = dict()
	All_Model = dict()
	null_count = dict()
	count = dict()
	for i in range(1998, 2018):
		All_Sentences[str(i)] = list()
		null_count[str(i)] = 0
		count[str(i)] = 0

	print("Starts loading sentences")
	for i in range(1998, 2018):
		with open(path+str(i)+".txt", 'r', encoding = 'UTF-8') as f:
			for sen in f:
				temp = sen.strip()
				if temp != 'null' and temp != '':
					temp = temp.split('\t')
					All_Sentences[str(i)].append(temp)
					count[str(i)] += 1
				else:
					null_count[str(i)] += 1

	
	# 1998-2003, 2004-2005, 2006, 2007, 2008, ..., 2016, 2017    14 groups
	groups = dict()
	index = 3
	for i in range(1998, 2018):
		if i <= 2003:
			groups[i] = 1
		elif i <= 2005 and i >= 2004:
			groups[i] = 2
		else:
			groups[i] = index
			index += 1

	Group_Sentences = dict()
	for i in range(1998, 2018):
		if groups[i] not in Group_Sentences:
			Group_Sentences[groups[i]] = list()
			Group_Sentences[groups[i]].extend(All_Sentences[str(i)])
		else:
			Group_Sentences[groups[i]].extend(All_Sentences[str(i)])

	TimeStart = time.time()
	print("Training starts.")
	for i in range(1998, 2018):
		All_Model[i] = Word2Vec(sentences = All_Sentences[str(i)], size = 128, window = 2)
		print("Training group", str(i), "data takes", time.time() - TimeStart, "seconds.")
		TimeStart = time.time()

	'''
	for i in range(1998, 2018):
		print("Number of articles in %d year: %d, with null main_text: %d" % (i, count[str(i)], null_count[str(i)]))
	'''

	for i in range(1998, 2018):
		print("Similarity between '分布式' and '数据库' at year %d:" % i, All_Model[i].wv.n_similarity(['分布式'], ['数据库']))
		a = All_Model[i].wv['分布式']
		b = All_Model[i].wv['数据库']
		cos = np.sum(a*b) / (np.linalg.norm(a)*np.linalg.norm(b))
		sim = float(0.5+0.5*cos)
		# print("self-caculated similarity:", sim)

	for i in range(1998, 2018):
		All_Model[i].wv.save_word2vec_format(path_dict[path]+str(i))
	print('='*100,'\n')



'''
model = Word2Vec.load_word2vec_format('/tmp/vectors.txt', binary=False)
# using gzipped/bz2 input works too, no need to unzip:
model = Word2Vec.load_word2vec_format('/tmp/vectors.bin.gz', binary=True)
'''