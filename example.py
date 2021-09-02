from gtoria import *

Information = {
	'placeholder': 'password',
	'placeholder': 'password'
}

def Align(String, Length):
	return String + str( ' ' * int( Length - len(String) ) ) + '║'

print('╔══════════╦══════════════════════════╦═══════╗')
print('║ Response ║ Username                 ║ Coins ║')
print('╠══════════╬══════════════════════════╬═══════╣')

for Username in Information:
	Response, Session = Graphictoria.User.Login_Session(Username, Information[Username])

	if Response.Code == 200:
		Graphictoria.User.Claim_Coins()
		print('║ SUCCESS  ║ ' + Align(Response.Username, 25) + ' ' + Align( Graphictoria.User.Get_Balance(), 6 ))
	else:
		print('║ ERROR    ║ ' + Align(Response.Username, 25) + ' ???   ║')

print('╚══════════╩══════════════════════════╩═══════╝')
