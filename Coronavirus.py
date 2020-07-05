from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import requests
import time
import re

width = 0.25

matplotlib.rcParams['font.family'] = 'SimHei'
url = "https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0"
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

def get_soup(url, header):
    response = requests.get(url, header)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2), 
                    textcoords="offset points",
                    ha='center', va='bottom')

def plot(list1, list2):
	#fig, ax = plt.subplots(2, 1)
	x = np.arange(len(cities))
	t = time.strftime('%m/%d %H:%M:%S',time.localtime(time.time()))
	rects1 = plt.bar(x - width/2, list1, width, label='确诊人数')
	rects2 = plt.bar(x + width/2, list2, width, label='疑似感染人数')

	plt.title('各省疫情统计直方图(北京时间:' + t + ')')
	plt.ylabel('人数')
	plt.xticks(x, cities)
	plt.legend()

	autolabel(rects1)
	autolabel(rects2)

	plt.ion()
	plt.pause(1)
	plt.cla()

while True:
	soup = get_soup(url, header)
	target_div = soup.find('div', attrs={'class':'descBox___3dfIo'})
	content = target_div.find_all('p', attrs={'class': 'descList___3iOuI'})

	data_list = list()
	for i in content:
		data = dict()
		city = re.findall(r'</i>(.+?)<span>', str(i))
		certain = re.findall(r'确诊 <span style="color: #4169e2">(.+?)</span>', str(i))
		uncertain = re.findall(r'疑似 <span style="color: #4169e2">(.+?)</span>', str(i))
		recover = re.findall(r'治愈 <span style="color: #4169e2">(.+?)</span>', str(i))
		death = re.findall(r'死亡 <span style="color: #4169e2">(.+?)</span>', str(i))
		data['city'] = city[0]
		try:
			data['certain'] = certain[0]
		except IndexError:
			data['certain'] = 0
		try:
			data['uncertain'] = uncertain[0]
		except IndexError:
			data['uncertain'] = 0		
		# try:
		# 	data['recover'] = recover[0]
		# except IndexError:
		# 	data['recover'] = 0
		# try:
		# 	data['death'] = death[0]
		# except IndexError:
		# 	data['death'] = 0
		data_list.append(data)

	cities = list()
	persons_certain = list()
	persons_uncertain = list()
	for i in data_list:
		if i['city'] == '湖北 ' or i['city'] == '香港 ':
			continue
		cities.append(i['city'])
		persons_certain.append(int(i['certain']))
		persons_uncertain.append(int(i['uncertain']))

	plot(persons_certain, persons_uncertain)

