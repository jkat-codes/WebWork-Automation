import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

class CheckForWork:
	def __init__(self): 
		self.url: str = os.environ.get("URL")
		self.username: str = os.environ.get("USERNAME")
		self.password: str = os.environ.get("PASSWORD") 
		if self.username is None or self.password is None: 
			print("username or password is not properly initialized!")
			raise ValueError("Username or password is not properly initialized!")
		
		self.session = requests.Session()
		self.login_data: dict = {'user': self.username, 'passwd': self.password}
	
	def login(self): 
		try: 
			print("Fetching initial cookies")
			response = self.session.get(self.url)	
			
			print("Logging in")
			response = self.session.post(self.url, data=self.login_data)

			if response.status_code != 200: 
				print(f"Login failed! Error code: {response.status_code}")
				return
			else: 	
				print("Login successfull!")
				try: 
					response.json()
				except Exception as e: 
					print("Page is not in JSON format!")
				try: 
					response.text
				except Exception as e: 
					print("Page is not in text format!")
				return response
		except Exception as e: 
			print(f"Login failed! Error: {str(e)}")
			return None
	def parse_response(self, response): 
		if response is None: 
			return
		try: 
			webworks_to_complete = []
			html = response.content
			soup = BeautifulSoup(html, 'html.parser')

			table = soup.find("tbody", class_="table-group-divider")
			tr = table.find_all('tr')
			for t in tr: 
				td = t.find_all('td')
				status = (str(td[1].contents))
				if "Open" in status: 
					title = td[0].a.contents
					title.replace("[", "")
					title.replace("]", "")
					title.replace("'", "")
					webworks_to_complete.append(title)
			if len(webworks_to_complete) > 0: 
				print("You need to do a webwork!\n")
				for assignment in webworks_to_complete: 
					print(assignment + "\n")
				return
			else: 
				print("\n ----- Nothing due! ----- \n")
				return
							
		except Exception as e: 
			print(f'Failed to parse with BS4! {str(e)}')
			return

	def main(self): 
		response = self.login()
		self.parse_response(response)
		
			
		
if __name__ == "__main__": 
	test = CheckForWork()
	test.main()

