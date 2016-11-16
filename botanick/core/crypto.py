# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto import Random
import base64

def encrypt(s,encryption_key):
	"""Function used to encrypt a string

	:param s: the string to encrypt
	:param encryption_key: the encryption key
	:return the encrypted string
	"""
	s = pad(s)
	iv = Random.new().read( AES.block_size )
	cipher = AES.new( encryption_key, AES.MODE_CBC, iv )
	return base64.b64encode( iv + cipher.encrypt( s ) )

def decrypt(s, encryption_key, block_size):
	"""Function used to decrypt a string

	:param s: the string to decrypt
	:param encryption_key: the encryption key
	:param block_size: the block size used to unpad
	:return the decrypted string
	"""
	enc = base64.b64decode(s)
	iv = enc[:block_size]
	cipher = AES.new(encryption_key, AES.MODE_CBC, iv )
	return unpad(cipher.decrypt( enc[block_size:] ))

def pad(s, block_size):
	"""Pad a string

	:param s: the string to pad
	:param block_size: the block size used to pad
	:return: the padded string
	"""
	return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)

def unpad(s):
	"""Unpad a string

	:param s: the string to unpad
	:return: the unpaded string
	"""
	return s[:-ord(s[len(s)-1:])]