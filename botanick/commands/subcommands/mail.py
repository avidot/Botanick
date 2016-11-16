# -*- coding: utf-8 -*-
import os
from botanick.core.harvester import harvest
from botanick.core.converters import tostring
from botanick.core.config import config
from botanick.const import BASE_PATH
from botanick.const import VERSION
from Crypto.Cipher import AES
from Crypto import Random
import base64
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

	def encrypt( self, password ):
		"""Function used to encrypt a password

		:param password: the password to encrypt
		:return the encrypted password
		"""
		password = self.pad(password)
		iv = Random.new().read( AES.block_size )
		cipher = AES.new( self.encryption_key, AES.MODE_CBC, iv )
		return base64.b64encode( iv + cipher.encrypt( password ) )

	def decryptPassword(self):
		"""Function used to decrypt a password"""
		enc = base64.b64decode(self.password)
		iv = enc[:self.block_size]
		cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv )
		return self.unpad(cipher.decrypt( enc[self.block_size:] ))

	def pad(self, s):
		"""Pad a string

		:param s: the string to pad
		:return: the padded string
		"""
		return s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)

	def unpad(self, s):
		"""Unpad a string

		:param s: the string to unpad
		:return: the unpaded string
		"""
		return s[:-ord(s[len(s)-1:])]

	def readEmail(self, mail, emailUID):
		"""Read an email and return the message

		:param mail: the imap mail instance
		:param emailUID: UID of the mail to read
		:return: the message
		"""
		result, data = mail.uid('fetch', emailUID, '(RFC822)')
		raw_email = str(data[0][1],'utf-8')
		return email.message_from_string(raw_email)

	def prepareReply(self, mailSubject, mailFrom, mailTo, mailID):
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

	def run(self):
		"""Main function of this mail manager"""
		decryptedPassword = self.decryptPassword()
		decryptedPassword = str(decryptedPassword,'utf-8')

		mail = imaplib.IMAP4_SSL(self.imap)

		try:
			mail.login(self.username, decryptedPassword)
			mail.select(self.mailbox)
		except:
			print("Login error")

		while True:

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
			 
			time.sleep(self.scanFrequency)

def mail(args):
	mailManager = MailManager(args['key'])
	mailManager.run()
	
