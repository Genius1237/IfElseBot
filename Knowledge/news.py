import requests

class News():

	apikey = "8a6b8c7a93c04c969ee984d8dc2d196f"
	base_url = "https://newsapi.org/v2/"

	def make_request(url,q="",country=""):
		p={
			'apiKey':News.apikey,
		}
		if country!="":
			p['country']=country
		if q!="":
			p['q']=q
		try:
			r=requests.get(url,params=p)
		except requests.exceptions.RequestException:
			return {
					'success':False,
					'message':'Error getting response'
				}
		j=r.json()
		if r.status_code == '401':
			return {
					'success':False,
					'message':'Key limit exceeded'
				}
		elif r.status_code==200:
			return {
				'success':True,
				'j':j
			}
		else:
			return {
					'success':False,
					'message':'Network problem'
				}

	def process_query(url,q="",country=""):
		j=News.make_request(url,q,country)
		
		if j['success']:
			j=j['j']
			a=[]
			try:
				for article in j['articles']:
					title=article['title']
					description=article['description']
					url=article['url']
					a.append({
						'title':title,
						'url':url,
						'description':description
						})
				return{
					'success':True,
					'a':a
				}
			except ValueError:
				return {
					'success':False,
					'message':'Error getting response'
				}
			except KeyError:
				return {
					'success':False,
					'message':'Error getting response'
				}
		else:
			return j

	#DO NOT USE THIS
	def get_news(q):
		return News.process_query("{}everything".format(News.base_url),q)

	def get_world_top_headlines(q=""):
		return News.process_query("{}top-headlines".format(News.base_url),q)
	
	def get_india_top_headlines(q=""):
		return News.process_query("{}top-headlines".format(News.base_url),q,'in')	

def main():
	s=input()
	n=News.get_india_top_headlines(s)
	if n['success']:
		for article in n['a']:
			print(article)
			input()

if __name__ == '__main__':
	main()