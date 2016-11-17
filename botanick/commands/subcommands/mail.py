# -*- coding: utf-8 -*-

from botanick.core.harvester import harvest
from botanick.core.converters import tostring
from botanick.core.config import config
from botanick.core.crypto import decrypt
import time
import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailManager():
	"""Manage the mail subcommand"""

	def __init__(self, encryption_key):
		"""Constructor : Initialize all parameters"""
		self.encryption_key = encryption_key
		mail_section = "MAIL"
		self.imap = config[mail_section]["IMAP_SERVER"]
		self.smtp = config[mail_section]["SMTP_SERVER"]
		self.username = config[mail_section]["USERNAME"]
		self.password = config[mail_section]["PASSWORD"]
		self.mailbox = config[mail_section]["MAILBOX"]
		self.scanFrequency = int(config[mail_section]["SCAN_FREQUENCY"])
		self.block_size = 16

	@classmethod
	def readEmail(cls, mail, emailUID):
		"""Read an email and return the message

		:param mail: the imap mail instance
		:param emailUID: UID of the mail to read
		:return: the message
		"""
		result, data = mail.uid('fetch', emailUID, '(RFC822)')
		raw_email = str(data[0][1],'utf-8')
		return email.message_from_string(raw_email)

	@classmethod
	def prepareReply(cls, mailSubject, mailFrom, mailTo, mailID):
		"""Prepare the reply and return the message to send

		:param mailSubject: the mail subject
		:param mailFrom: the from email address
		:param mailTo: the destination email address
		:param mailID: the email ID
		:return: the message to send
		"""
		msg = MIMEMultipart()
		msg['to'] = mailFrom
		msg['from'] = mailTo
		# Fix subject
		msg['Subject'] = "RE: "+mailSubject.replace("Re: ", "").replace("RE: ", "")
		msg['In-Reply-To'] = mailID
		msg['References'] = mailID
		return msg

	def sendEmail(self, msg, decryptedPassword):
		"""Send the email

		:param msg: the message to send
		:param decryptedPassword: the decrypted password
		"""
		try:
			server = smtplib.SMTP(self.smtp, 587, None, 30)
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login(self.username, decryptedPassword)
			server.sendmail(msg['from'], [msg['to']], msg.as_string())
		except Exception as e:
			print(e)
		finally:
			server.close()

	def openImapConnection(self, decryptedPassword):
		"""Open the IMAP connection

		:param decryptedPassword: the decrypted password
		:return: the imap mail connection
		"""
		mail = imaplib.IMAP4_SSL(self.imap)
		try:
			mail.login(self.username, decryptedPassword)
			mail.select(self.mailbox)
		except imaplib.IMAP4.error as e:
			print("Login error : "+str(e))
		return mail

	def run(self):
		"""Main function of this mail manager"""
		decryptedPassword = decrypt(self.password, self.encryption_key, self.block_size)
		decryptedPassword = str(decryptedPassword,'utf-8')

		while True:
			mail = self.openImapConnection(decryptedPassword)

			result, data = mail.uid('search', None, '(UNSEEN HEADER Subject "[Search]")')
			for email_uid in data[0].split():
				email_message = self.readEmail(mail, email_uid)

				mailSubject = email_message['Subject']
				domainRequested = mailSubject.split(" ")[1]
				mailTo = email.utils.parseaddr(email_message['To'])[1]
				mailFrom = email.utils.parseaddr(email_message['From'])[1]
				mailID = email_message["Message-ID"]

				msg = self.prepareReply(mailSubject, mailFrom, mailTo, mailID)

				# Harvest requested domain mail and add results as mail body
				body = tostring(harvest(domainRequested))
				msg.attach(MIMEText(body, 'plain'))

				self.sendEmail(msg, decryptedPassword)

			mail.close()
			mail.logout()
			time.sleep(self.scanFrequency)

def mail(args):
	mailManager = MailManager(args['key'])
	mailManager.run()
