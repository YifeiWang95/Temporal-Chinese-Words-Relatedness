import thulac
import time
import re

TimeStart = time.time()
TempTime = TimeStart

raw_cn = "./com_cn.txt"
## There are 20 different years, from 1998 to 2017.
All_Dict = dict()
for i in range(1998,2018):
	All_Dict['title_' + str(i)] = list()
	All_Dict['main1_' + str(i)] = list()
	All_Dict['main2_' + str(i)] = list()
	All_Dict['year_' + str(i)] = list()

user_dict = "./_reference/thulac/THUOCL_it.txt"
thulac1 = thulac.thulac(user_dict = None, seg_only = True)
thulac2 = thulac.thulac(user_dict = user_dict, seg_only = True)
count = 0
unstructured = list()
with open(raw_cn, 'r', encoding = 'UTF-8') as raw:
	for line in raw:
		temp = line.split('\t')
		if len(temp) == 3:
			current_year = str(temp[2].strip())
			All_Dict['title_' + current_year].append(temp[0])
			All_Dict['year_' + current_year].append(current_year)
			temp1 = thulac1.cut(temp[1], text = True)  # Ignore the space between any words
			#temp1 = re.sub('[^\u4e00-\u9fa5 ]', '', temp1)   # delete non-Chinese characters
			temp1 = re.sub('[^\u4e00-\u9fa5 ^a-z^A-Z]', '', temp1)   # delete non-Chinese and non-English characters
			temp1 = temp1.split()
			All_Dict['main1_' + current_year].append(temp1)
			temp2 = thulac2.cut(temp[1], text = True)  # Ignore the space between any words
			#temp2 = re.sub('[^\u4e00-\u9fa5 ]', '', temp2)   # delete non-Chinese characters
			temp2 = re.sub('[^\u4e00-\u9fa5 ^a-z^A-Z]', '', temp2)   # delete non-Chinese and non-English characters
			temp2 = temp2.split()
			All_Dict['main2_' + current_year].append(temp2)
		else:
			unstructured.append(count)
		count += 1

		if count % 10000 == 0:
			print("Time for 10000 sentences: %.2f" % (time.time()-TempTime))
			TempTime = time.time()


print("unstructured sample:")
print(unstructured)

for i in range(1998,2018):
	with open('./structured_data/thulac/CN+EN/com_cn_title_'+str(i)+'.txt', 'w', encoding = 'UTF-8') as f:
		for item in All_Dict['title_' + str(i)]:
			f.write(item)
			f.write('\n')
	with open('./structured_data/thulac/CN+EN/com_cn_main_'+str(i)+'.txt', 'w', encoding = 'UTF-8') as f:
		for sen in All_Dict['main1_' + str(i)]:
			for item in sen:
				f.write(item)
				f.write('\t')
			f.write('\n')
	with open('./structured_data/thulac/CN+EN/com_cn_main_uw_'+str(i)+'.txt', 'w', encoding = 'UTF-8') as f:
		for sen in All_Dict['main2_' + str(i)]:
			for item in sen:
				f.write(item)
				f.write('\t')
			f.write('\n')

print("Program takes:", time.time() - TimeStart, "seconds.")


