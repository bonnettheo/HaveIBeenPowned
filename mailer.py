import smtplib
from string import Template
import getpass 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def read_template(filename):

	with open(filename, 'r', encoding='utf-8') as template_file:
		template_file_content = template_file.read()
	return Template(template_file_content)

def send_mail(breach, address):
	s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
	s.starttls()

	login = False
	i=0
	while i < 5 and not login:
		i += 1
		try:
			p = getpass.getpass()
			s.login(address, p)
			login = True
		except:
			pass
	if not login:
		print("powned but cannot send email")
		s.quit()
		quit()

	message_template = read_template('message.txt')
	msg = MIMEMultipart()       # create a message
	message = message_template.substitute(TIME=len(breach), URL="https://haveibeenpwned.com/")
	print(message)

	msg['From']=address
	msg['To']=address
	msg['Subject']="I have been powned"

	msg.attach(MIMEText(message, 'plain'))

	s.send_message(msg)
	del msg
	s.quit()