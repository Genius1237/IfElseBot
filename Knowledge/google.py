import requests
from bs4 import BeautifulSoup

class Search():

	base_url = "https://www.google.co.in/search"

	def make_request(q):
		p={
			'q':q
		}
		url=Search.base_url
		try:
			r=requests.get(url,params=p)
		except requests.exceptions.RequestException:
			return {
					'success':False,
					'message':'Error getting response'
				}	
		if r.status_code==200:
			s=BeautifulSoup(r.text,'html5lib')
			#print(s.prettify())
			if len(s.find_all(class_="_tXc")) == 0:
				return {
					'success':False,
					'message':'No simple description'
				}
			else:
				t=s.find_all(class_="_tXc")[0].text
				return {
					'success':True,
					'd':t
				}
		else:
			return {
					'success':False,
					'message':'Network problem'
				}

	def get_simple_description(q):
		return Search.make_request(q)	

def main():
	s=input()
	n=Search.get_simple_description(s)
	print(n)

if __name__ == '__main__':
	main()