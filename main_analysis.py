#-*- coding: utf-8 -*-

from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from gensim.models import KeyedVectors
import numpy as np
import collections
import time

font = FontProperties(fname = 'c:/windows/fonts/simsun.ttc', size = 14)


# Year
path_cn = "./models/thulac/CN/model_"
path_cn_uw = "./models/thulac/CN/model_uw_"
year = [str(x) for x in range(1998,2018)]

model_cn = dict()
model_cn_uw = dict()
for i in year:
	model_cn[i] = KeyedVectors.load_word2vec_format(path_cn+i, binary = False)
	model_cn_uw[i] = KeyedVectors.load_word2vec_format(path_cn_uw+i, binary = False)

path_en = "./models/thulac/CN+EN/model_"
path_en_uw = "./models/thulac/CN+EN/model_uw_"
year = [str(x) for x in range(1998,2018)]

model_en = dict()
model_en_uw = dict()
for i in year:
	model_en[i] = KeyedVectors.load_word2vec_format(path_en+i, binary = False)
	model_en_uw[i] = KeyedVectors.load_word2vec_format(path_en_uw+i, binary = False)

# Groups
path_cn = "./models/thulac_groups/CN/model_"
path_cn_uw = "./models/thulac_groups/CN/model_uw_"
groups = [x for x in range(1, 15)]

model_groups_cn = dict()
model_groups_cn_uw = dict()
for i in groups:
	model_groups_cn[i] = KeyedVectors.load_word2vec_format(path_cn+str(i), binary = False)
	model_groups_cn_uw[i] = KeyedVectors.load_word2vec_format(path_cn_uw+str(i), binary = False)

path_en = "./models/thulac_groups/CN+EN/model_"
path_en_uw = "./models/thulac_groups/CN+EN/model_uw_"
groups = [x for x in range(1, 15)]

model_groups_en = dict()
model_groups_en_uw = dict()
for i in groups:
	model_groups_en[i] = KeyedVectors.load_word2vec_format(path_en+str(i), binary = False)
	model_groups_en_uw[i] = KeyedVectors.load_word2vec_format(path_en_uw+str(i), binary = False)


# a and b must be lists
# n_similarity: dot(unitvec(a.mean()), unitvec(b.mean()))
def Dynamics(a, b, group = True, uw = True, en = False):
	sims = list()
	if group == False:
		switch = {0:model_cn, 1:model_en, 10:model_cn_uw, 11:model_en_uw} # 10*uw+en  
		switch_str = {0:'model_cn', 1:'model_en', 10:'model_cn_uw', 11:'model_en_uw'} # 10*uw+en
		key = 10 * uw + en
		a_bool = dict()
		b_bool = dict()
		for i in year:
			a_bool[i] = list()
			b_bool[i] = list()
			for word in a:
				if word in switch[key][i]:
					a_bool[i].append(0)
				else:
					a_bool[i].append(1)
			for word in b:
				if word in switch[key][i]:
					b_bool[i].append(0)
				else:
					b_bool[i].append(1)
			if sum(a_bool[i]) == 0:
				if sum(b_bool[i]) == 0:
					print("Similarity between %s and %s in %s_%s is: %f" % (a, b, switch_str[key], i, switch[key][i].wv.n_similarity(a, b)))
					sims.append(switch[key][i].wv.n_similarity(a, b))
				else:
					print("Some words in %s is not existed in %s_%s dictionary" % (b, switch_str[key], i))
					sims.append(0)
			else:
				if sum(b_bool[i]) == 0:
					print("Some words in %s is not existed in %s_%s dictionary" % (a, switch_str[key], i))
					sims.append(0)
				else:
					print("Both %s and %s is not existed in %s_%s dictionary" % (a, b, switch_str[key], i))
					sims.append(0)
	elif group == True:
		switch = {0:model_groups_cn, 1:model_groups_en, 10:model_groups_cn_uw, 11:model_groups_en_uw} # 10*uw+en  
		switch_str = {0:'model_groups_cn', 1:'model_groups_en', 10:'model_groups_cn_uw', 11:'model_groups_en_uw'} # 10*uw+en
		key = 10 * uw + en
		a_bool = dict()
		b_bool = dict()
		for i in groups:
			a_bool[i] = list()
			b_bool[i] = list()
			for word in a:
				if word in switch[key][i]:
					a_bool[i].append(0)
				else:
					a_bool[i].append(1)
			for word in b:
				if word in switch[key][i]:
					b_bool[i].append(0)
				else:
					b_bool[i].append(1)
			if sum(a_bool[i]) == 0:
				if sum(b_bool[i]) == 0:
					print("Similarity between %s and %s in %s_%s is: %f" % (a, b, switch_str[key], i, switch[key][i].wv.n_similarity(a, b)))
					sims.append(switch[key][i].wv.n_similarity(a, b))
				else:
					print("Some words in %s is not existed in %s_%s dictionary" % (b, switch_str[key], i))
					sims.append(0)
			else:
				if sum(b_bool[i]) == 0:
					print("Some words in %s is not existed in %s_%s dictionary" % (a, switch_str[key], i))
					sims.append(0)
				else:
					print("Both %s and %s is not existed in %s_%s dictionary" % (a, b, switch_str[key], i))
					sims.append(0)
	print("")
	return sims

def Most_Similar(a, topn = 10, group = True, uw = True, en = False):
	words = list()
	null_count = 0
	for i in groups:
		if a[0] in model_groups_cn_uw[i]:
			temp = model_groups_cn_uw[i].wv.most_similar(positive = a, topn = topn)
			for pair in temp:
				words.append(pair[0])
		else:
			null_count += 1
	print(a)
	print(collections.Counter(words))
	print("null_count:", null_count, '\n')

def Plot_Line_Chart(temp, title):
	plt.figure()
	plt.plot(range(1, len(temp)+1), temp)
	plt.title(title, fontproperties = font)
	plt.ylabel('分时相关度', fontproperties = font)
	plt.xlabel('分组编号', fontproperties = font)
	plt.axis([0.5, len(temp)+0.5, -0.1, 1.1])
	plt.show()

def Plot_Line_Chart_year(temp, title):
	ax = plt.figure().gca()
	ax.xaxis.set_major_locator(MaxNLocator(integer=True))
	plt.plot(range(1998, 2018), temp)
	plt.title(title, fontproperties = font)
	plt.ylabel('分时相关度', fontproperties = font)
	plt.xlabel('年份', fontproperties = font)
	plt.axis([1997, 2018, -0.1, 1.1])
	plt.show()




print("="*100)
print("uw?")
DL1 = Dynamics(['神经网络'], ['深度学习'], group = True, uw = True)
Plot_Line_Chart(DL1, '“神经网络”与“深度学习”间的历史相关性（有词库）')
#Dynamics(['神经网络'], ['深度学习'], group = True, uw = False) 无结果
DL2 = Dynamics(['神经', '网络'], ['深度', '学习'], group = True, uw = False)
Plot_Line_Chart(DL2, '“神经”+“网络”与“深度”+“学习”间的历史相关性（无词库）')

print("words choice?")
DL3 = Dynamics(['神经', '网络'], ['深度', '学习'], group = True, uw = True)
DL4 = Dynamics(['神经网络'], ['深度', '学习'], group = True, uw = True)
DL5 = Dynamics(['神经', '网络'], ['深度学习'], group = True, uw = True)
DL6 = Dynamics(['神经网络'], ['深度学习'], group = True, uw = True)
Plot_Line_Chart(DL3, '“神经”+“网络”与“深度”+“学习”间的历史相关性')
Plot_Line_Chart(DL4, '“神经网络”与“深度”+“学习”间的历史相关性')
Plot_Line_Chart(DL5, '“神经”+“网络”与“深度学习”间的历史相关性')
Plot_Line_Chart(DL6, '“神经网络”与“深度学习”间的历史相关性')

print("EN?")
SVM1 = Dynamics(['SVM'], ['分类'], group = True, uw = True, en = True)
Plot_Line_Chart(SVM1, '“SVM”与“分类”间的历史相关性')
SVM2 = Dynamics(['分类'], ['支持向量机'])
Plot_Line_Chart(SVM2, '“支持向量机”与“分类”间的历史相关性')

print("‘分类’于cn：")
for i in groups:
	print(model_groups_cn_uw[i].wv.most_similar(positive = ['分类'], topn = 20))
print("‘分类’于en：")
for i in groups:
	print(model_groups_en_uw[i].wv.most_similar(positive = ['分类'], topn = 20))
print("‘分类’于cn：")
Most_Similar('分类', topn = 20, group = True, uw = True, en = False)
print("‘分类’于en：")
Most_Similar('分类', topn = 20, group = True, uw = True, en = True)

print('groups?')
Y = Dynamics(['数据库'], ['分布式'], group = False)
G = Dynamics(['数据库'], ['分布式'], group = True)
Plot_Line_Chart(G, '“分布式”与“数据库”间的历史相关性')
Plot_Line_Chart_year(Y, '“分布式”与“数据库”间的历史相关性')



print("new words?")
Dynamics(['人脸识别'], ['奇异值分解'], group = True, uw = True, en = False)
Dynamics(['图像识别'], ['奇异值分解'], group = True, uw = True, en = False)
Dynamics(['语义'], ['词向量'], group = True, uw = True, en = False)
Dynamics(['语义'], ['奇异值分解'], group = True, uw = True, en = False)
Dynamics(['语义'], ['词频'], group = True, uw = True, en = False)


print("Tests:")
temp1 = Dynamics(['文本'],['语义'])
Dynamics(['文本'],['情感'])
Dynamics(['文本'],['语法'])
Dynamics(['文本'],['关键词'])

Dynamics(['词向量'],['文本'])
Dynamics(['词向量'],['自然语言处理'])


Plot_Line_Chart(temp1, '“文本”与“语义”间的相似度')

