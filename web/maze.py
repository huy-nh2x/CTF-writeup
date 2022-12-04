import requests

url = "https://hyper-maze.tuctf.com/pages/page_"
page = "uncriticizable"
count = 95
while count>1:
	while True:
		try:
			r = requests.get(url + page + str(count) + ".html")
		except:
			continue
		if(r.status_code==200):
			break
	count = count-1
	page = r.text[r.text.find("href=\"page_")+11:r.text.find(str(count) + ".html")]
	print(str(count) + ": " + page)

