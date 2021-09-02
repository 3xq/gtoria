import requests, random, re, os

Main_Session = None;

Information = {}

Temp_Friends = []

def Set_Main_Session(Object):
	global Main_Session

	Main_Session = Object

def Get_Proxies():
	Proxies = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all').text.strip().split('\n')

	return Proxies

def Get_CSRF(Url = 'https://gtoria.net/'):
	try:
		Session = requests.Session()
		Session.cookies['a_id'] = 'deleted'
		Session.cookies['auth_uid'] = 'deleted'

		Response = Session.get(Url).text

		CSRF = Response.split('<meta name="csrf-token" content="')[1].split('">')[0]

		return CSRF
	except Exception as E:
		Response = input('Interal code errored, please restart. Yes/No/Exception (Y/N/E):')
		if Response.lower() == 'y':
			os.system('exit')
		elif Response.lower() == 'n':
			return Get_CSRF(Url)
		elif Response.lower() == 'e':
			print(E)
			return 'deleted'
			

def Login(Username_Actual, Password, CSRF, Proxies):
	Form_Data = {
		"username": Username_Actual,
		"passwd": Password,
		"csrf": CSRF
	}

	Session = requests.Session()
	Session.cookies['a_id'] = 'deleted'
	Session.cookies['auth_uid'] = 'deleted'

	Response = Session.post(
		'https://gtoria.net/core/func/api/auth/login.php',
		data = Form_Data,
		proxies = {
			'http': 'http://' + random.choices(
				Proxies
			)[0].replace(
				'\r',
				''
			)
		}
	)
	
	Session.cookies['a_id'] = Response.headers["set-cookie"].split('a_id')[-1].split('=')[1].split(';')[0]
	Session.cookies['auth_uid'] = Response.headers["set-cookie"].split('auth_uid')[-1].split('=')[1].split(';')[0]

	Information['a_id'] = Response.headers["set-cookie"].split('a_id')[-1].split('=')[1].split(';')[0]
	Information['auth_uid'] = Response.headers["set-cookie"].split('auth_uid')[-1].split('=')[1].split(';')[0]

	if Response.text == 'success':
		class Response:
			Code = 200
			Text = '[SUCCESS]'
			Username = Username_Actual

		return Response(), Session
	elif Response.text == 'error':
		class Response:
			Code = 500
			Text = '[ERROR]'
			Username = Username_Actual
			
		return Response(), None
	elif Response.text == 'rate-limit':
		class Response:
			Code = 429
			Text = '[LIMIT]'
			Username = Username_Actual
			
		return Response(), None
	elif Response.text == 'incorrect-password':
		class Response:
			Code = 429
			Text = '[WRONG]'
			Username = Username_Actual
			
		return Response(), None
	else:
		return Response.text, None

class Graphictoria:
	class User:
		def Login_Session(Username, Password):
			CSRF = Get_CSRF()
			Response, Returned_Session = Login(Username, Password, CSRF, Get_Proxies())

			Set_Main_Session(Returned_Session)

			Information['Username'] = Username
			Information['Password'] = Password 

			return Response, Returned_Session

		def Claim_Coins():
			Main_Session.get('https://gtoria.net/user/profile/' + Information['Username'])

		def Get_Balance():
			Response = Main_Session.get('https://gtoria.net/').text
			Balance = Response.split('<span id="userCoins">')[1].split('</span>')[0]
			
			return Balance

		def Get_Description():
			Response = Main_Session.get(f'https://gtoria.net/user/profile/' + Information['Username']).text

			if 'This user has not configured anything to display here.' not in Response:
				Description = Response.split('<span style="word-wrap:break-word;">')[1].split('</span>')[0]

				return Description
			else:
				return ''

		def Get_Headshot():
			return 'https://www.gtoria.net/avatar-headshot/' + Information['Username']

		def Get_Forum_Amount():
			Response = Main_Session.get(f'https://gtoria.net/core/func/api/forum/getMiniProfile.php?id=' + Information['Username']).text

			Amount = Response.split('s</b>: ')[1].split('<')[0]

			return Amount

		class Friends:
			def Load_Friendslist_Page(User_ID, Page):
				Response = requests.get(f'https://gtoria.net/core/func/api/friends/get/showFriends.php?userid={ User_ID }&page={ Page }').text

				return Response

			def Regex_Friendslist_Page(Response):
				Friends = re.findall(r'\/user\/profile\/[A-Za-z\d\._]+', Response)

				return Friends

			def Get_Friends_Table(User_ID, Page, Output_Table):
				Response = Graphictoria.User.Friends.Load_Friendslist_Page(User_ID, Page)
				Friends = Graphictoria.User.Friends.Regex_Friendslist_Page(Response)

				if len(Friends) != 0:
					for Friend in Friends:
						Output_Table.append(Friend.split('/user/profile/')[1])

					Graphictoria.User.Friends.Get_Friends_Table(User_ID, Page + 1, Output_Table)

			def Get_Friends():
				Temp_Friends.clear()

				Graphictoria.User.Friends.Get_Friends_Table(Information['auth_uid'], 0, Temp_Friends)

				return Temp_Friends

	class Users:
		def Username_To_User_ID(Username = '404'):
			Response = Main_Session.get(f'https://gtoria.net/user/profile/{ Username }').text

			User_ID = Response.split('<script>var userId="')[1].split('";</script>')[0]

			return int(User_ID)

		def Get_Description(Username = '404'):
			Response = Main_Session.get(f'https://gtoria.net/user/profile/' + Username).text

			if 'This user has not configured anything to display here.' not in Response:
				Description = Response.split('<span style="word-wrap:break-word;">')[1].split('</span>')[0]

				return Description
			else:
				return ''

		def Get_Headshot(Username = '404'):
			return 'https://www.gtoria.net/avatar-headshot/' + Username

		def Get_Forum_Amount(Username):
			Response = Main_Session.get(f'https://gtoria.net/core/func/api/forum/getMiniProfile.php?id={Username}').text

			Amount = Response.split('s</b>: ')[1].split('<')[0]

			return Amount

		class Friends:
			def Load_Friendslist_Page(User_ID, Page):
				Response = requests.get(f'https://gtoria.net/core/func/api/friends/get/showFriends.php?userid={ User_ID }&page={ Page }').text

				return Response

			def Regex_Friendslist_Page(Response):
				Friends = re.findall(r'\/user\/profile\/[A-Za-z\d\._]+', Response)

				return Friends

			def Get_Friends_Table(User_ID, Page, Output_Table):
				Response = Graphictoria.User.Friends.Load_Friendslist_Page(User_ID, Page)
				Friends = Graphictoria.User.Friends.Regex_Friendslist_Page(Response)

				if len(Friends) != 0:
					for Friend in Friends:
						Output_Table.append(Friend.split('/user/profile/')[1])

					Graphictoria.User.Friends.Get_Friends_Table(User_ID, Page + 1, Output_Table)

			def Get_Friends(User_ID):
				Temp_Friends.clear()

				Graphictoria.User.Friends.Get_Friends_Table(int(User_ID), 0, Temp_Friends)
				
				return Temp_Friends

	class Catalog:
		def Buy_Item(Item_ID):
			Response = Main_Session.post(
				'https://gtoria.net/core/func/api/catalog/post/buyItem.php',
				data = {
					'csrf': Get_CSRF(f'https://gtoria.net/catalog/'),
					'itemId': str(Item_ID)
				}
			)

			return Response.text
