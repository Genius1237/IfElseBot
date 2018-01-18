import requests

class Weather():

	apikey = "7b1785ce5309792837108887e334107c"
	base_url = "https://api.openweathermap.org/data/2.5/"

	def make_request(url,city='Secunderabad'):
		p={
			'units':'metric',
			'q':city,
			'APPID':Weather.apikey
		}
		r=requests.get(url,params=p)
		try:
			j=r.json()
		except ValueError:
			return {
					'success':False,
					'message':'Error getting response'
				}
		if j['cod'] =='404':
			if j['message'] =='city not found':
				return {
					'success':False,
					'message':'city not found'
				}
			else:
				return {
					'success':False,
					'message':'Network Problem'
				}
		elif j['cod'] == '401':
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

	def get_current_weather(city='Secunderabad'):
		j=Weather.make_request("{}weather".format(Weather.base_url),city)
		
		if j['success']:
			j=j['j']
			try:
				category = j['weather'][0]['main']
				desc = j['weather'][0]['description']
				temp = int(j['main']['temp'])
				humidity = float(j['main']['humidity'])
				temp_min = int(j['main']['temp_min'])
				temp_max = int(j['main']['temp_max'])
				place="{}, {}".format(j['name'],j['sys']['country'])
				return {
					'success':True,
					'category':category,
					'desc':desc,
					'temp':temp,
					'humidity':humidity,
					'temp_min':temp_min,
					'temp_max':temp_max,
					'place':place
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

	def get_5_day_forecast(city='Secunderabad'):
		j=Weather.make_request("{}forecast".format(Weather.base_url),city)
		w=[]
		if j['success']:
			j=j['j']
			try:
				for i in range(0,j['cnt'],8):
					dt=j['list'][i]['dt_txt']
					category = j['list'][i]['weather'][0]['main']
					desc = j['list'][i]['weather'][0]['description']
					temp = int(j['list'][i]['main']['temp'])
					humidity = float(j['list'][i]['main']['humidity'])
					temp_min = int(j['list'][i]['main']['temp_min'])
					temp_max = int(j['list'][i]['main']['temp_max'])
					w.append({
						'category':category,
						'desc':desc,
						'temp':temp,
						'humidity':humidity,
						'temp_min':temp_min,
						'temp_max':temp_max,
						'date':dt
					})
				place="{}, {}".format(j['city']['name'],j['city']['country'])
				return {
					'success':True,
					'w':w,
					'place':place
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

def main():
	s=input()
	print(Weather.get_5_day_forecast(s))
	#print(w.get_current_weather())

if __name__ == '__main__':
	main()