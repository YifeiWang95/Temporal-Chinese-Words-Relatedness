import fool
import time

TimeStart = time.time()
TempTime = TimeStart

raw_cn = "./com_cn.txt"
## There are 20 different years, from 1998 to 2017.
All_Dict = dict()
for i in range(1998,2018):
	All_Dict['title_' + str(i)] = list()
	#All_Dict['main1_' + str(i)] = list()
	All_Dict['main2_' + str(i)] = list()
	All_Dict['year_' + str(i)] = list()

user_dict = "./_reference/thulac/THUOCL_it_space.txt"
fool.load_userdict(user_dict)
count = 0
unstructured = list()
with open(raw_cn, 'r', encoding = 'UTF-8') as raw:
	for line in raw:
		temp = line.split('\t')
		if len(temp) == 3:
			current_year = str(temp[2].strip())
			All_Dict['title_' + current_year].append(temp[0])
			All_Dict['year_' + current_year].append(current_year)
			#All_Dict['main1_' + current_year].extend(fool.cut(temp[1]))
			All_Dict['main2_' + current_year].extend(fool.cut(temp[1]))
		else:
			unstructured.append(count)
		count += 1

		if count % 1000 == 0:
			print("Time for 1000 sentences: %.2f" % (time.time()-TempTime))
			TempTime = time.time()

print("unstructured sample:")
print(unstructured)

for i in range(1998,2018):
	with open('./structured_data/fool/com_cn_title_'+str(i)+'.txt', 'w', encoding = 'UTF-8') as f:
		for item in All_Dict['title_' + str(i)]:
			f.write(item)
			f.write('\n')
	'''
	with open('./structured_data/com_cn_main_'+str(i)+'.txt', 'w', encoding = 'UTF-8') as f:
		for sen in All_Dict['main1_' + str(i)]:
			for item in sen:
				f.write(item)
				f.write('\t')
			f.write('\n')
	'''
	with open('./structured_data/fool/com_cn_main_uw_'+str(i)+'.txt', 'w', encoding = 'UTF-8') as f:
		for sen in All_Dict['main2_' + str(i)]:
			for item in sen:
				f.write(item)
				f.write('\t')
			f.write('\n')

print("Program takes:", time.time() - TimeStart, "seconds.")


