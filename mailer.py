import smtplib
from string import Template
import getpass 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

def read_template(filename):

	with open(filename, 'r', encoding='utf-8') as template_file:
		template_file_content = template_file.read()
	return Template(template_file_content)

def getMail():
	with open("automation_mail.json", 'r', encoding='utf-8') as json_file:
		mailAccount = json.load(json_file)
	return mailAccount["mail"], mailAccount["password"]

def send_mail(breach, address):

	sender, password = getMail()
	s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
	s.starttls()
	
	s.login(sender, password)

	message_template = read_template('message.txt')
	msg = MIMEMultipart()
	message = message_template.substitute(TIME=len(breach), URL="https://haveibeenpwned.com/")
	print(message)

	msg['From']=sender
	msg['To']=address
	msg['Subject']="You have been powned"

	msg.attach(MIMEText(message, 'plain'))

	s.send_message(msg)
	del msg
	s.quit()