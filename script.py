import argparse
import json
import urllib.request
import traceback
import mailer

filename = "pwnedTimes.json"
 
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def checkHaveIBeenPwned(email):
	fileContent = {}
	with open(filename, "r") as f:
		try:
			fileContent = json.load(f)
		except:
			fileContent = {}
			fileContent[email] = {}
			fileContent[email]["pwnedTimes"] = 0
			fileContent[email]["pwnedList"] = []

	url = "https://haveibeenpwned.com/unifiedsearch/"+email
	siteContent = {}
	try:
		request=urllib.request.Request(url,None,hdr) #The assembled request
		response = urllib.request.urlopen(request)
		siteContent = json.load(response) # The data u need
	except urllib.error.HTTPError as e:
		if e.code == 404:
			print("You have never been powned")
		else:
			print("error requesting " + url)
			traceback.print_exc()
		quit()

	newBreach = []
	if len(siteContent["Breaches"]) != fileContent[email]["pwnedTimes"] :
		for breach in siteContent["Breaches"]:
			newlyBreached = True
			for inList in fileContent[email]["pwnedList"]:
				if breach["Name"] in inList["Name"] and breach["BreachDate"] in inList["BreachDate"]:
					newlyBreached = False
			if newlyBreached:
				print("New breach came out the {} on {}".format(breach["BreachDate"], breach["Name"]))
				tmp = {}
				tmp["Name"] = breach["Name"]
				tmp["BreachDate"] = breach["BreachDate"]
				newBreach.append(tmp)

	if len(newBreach) > 0:
		fileContent[email]["pwnedTimes"] += len(newBreach)
		fileContent[email]["pwnedList"].extend(newBreach)
		mailer.send_mail(newBreach, email)
	
	with open(filename, "w") as f:
		try:
			json.dump(fileContent, f)
		except:
			print("error writting to file {}".format(filename))
			traceback.print_exc()

def main(email):
	checkHaveIBeenPwned(email)
	

def parseArgs():
	parser = argparse.ArgumentParser(usage = "%(prog)s <email>",
						description="check if email has newly been powned",
						epilog="python3 someone@gmail.com")
	parser.add_argument("email", type=str, help="email you want to check")
	args = parser.parse_args()
	
	if " " in args.email:
		parser.error("There cannot be whitespace in the email")

	return args.email

if __name__ == "__main__":
	main(parseArgs())