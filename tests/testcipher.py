from ctypescrypto.oid import Oid
from ctypescrypto import cipher
import unittest
import sys


class TestCipherType(unittest.TestCase):
	def test_ciphdescbc(self):
		ct=cipher.CipherType("des-cbc")
		self.assertEqual(ct.block_size(),8)
		self.assertEqual(ct.key_length(),8)
		self.assertEqual(ct.iv_length(),8)
		self.assertEqual(ct.oid().shortname(),"DES-CBC")
		self.assertEqual(ct.mode(),"CBC")
	def test_ciphaesofb(self):
		ct=cipher.CipherType("aes-256-ofb")
		self.assertEqual(ct.block_size(),1)
		self.assertEqual(ct.key_length(),32)
		self.assertEqual(ct.iv_length(),16)
		self.assertEqual(ct.oid().shortname(),"AES-256-OFB")
		self.assertEqual(ct.mode(),"OFB")

class TestEncryptDecrypt(unittest.TestCase):
	def test_blockcipher(self):
		data="sdfdsddf"
		key='abcdabcd'
		c=cipher.new("DES-CBC",key)
		enc=c.update(data)+c.finish()
		# See if padding is added by default
		self.assertEqual(len(enc),16)
		d=cipher.new("DES-CBC",key,encrypt=False)
		dec=d.update(enc)+d.finish()
		self.assertEqual(data,dec)
	def test_blockcipher_nopadding(self):
		data="sdfdsddf"
		key='abcdabcd'
		c=cipher.new("DES-CBC",key)
		c.padding(False)
		enc=c.update(data)+c.finish()
		# See if padding is added by default
		self.assertEqual(len(enc),8)
		d=cipher.new("DES-CBC",key,encrypt=False)
		d.padding(False)
		dec=d.update(enc)+d.finish()
		self.assertEqual(data,dec)
	def test_ofb_cipher(self):
		data="sdfdsddfxx"
		key='abcdabcd'
		iv='abcdabcd'
		c=cipher.new("DES-OFB",key,iv=iv)
		enc=c.update(data)+c.finish()
		# See if padding is added by default
		self.assertEqual(len(enc),len(data))
		d=cipher.new("DES-OFB",key,encrypt=False,iv=iv)
		dec=d.update(enc)+d.finish()
		self.assertEqual(data,dec)

	def test_ofb_noiv(self):
		data="sdfdsddfxx"
		encryptkey='abcdabcd'*4
		decryptkey=encryptkey[0:5]+encryptkey[5:]


		c=cipher.new("AES-256-OFB",encryptkey)
		enc=c.update(data)+c.finish()
		# See if padding is added by default
		self.assertEqual(len(enc),len(data))
		d=cipher.new("AES-256-OFB",decryptkey,encrypt=False)
		dec=d.update(enc)+d.finish()
		self.assertEqual(data,dec)
	def test_wrong_keylength(self):
		data="sdfsdfxxx"
		key="abcdabcd"
		with self.assertRaises(ValueError):
			c=cipher.new("AES-128-OFB",key)
	def test_wrong_ivlength(self):
		key="abcdabcdabcdabcd"
		iv="xxxxx"
		with self.assertRaises(ValueError):
			c=cipher.new("AES-128-OFB",key,iv=iv)
	def test_variable_keylength(self):
		encryptkey="abcdefabcdef"
		data="asdfsdfsdfsdfsdfsdfsdfsdf"
		iv="abcdefgh"
		c=cipher.new("bf-ofb",encryptkey,iv=iv)
		ciphertext=c.update(data)+c.finish()
		decryptkey=encryptkey[0:5]+encryptkey[5:]
		with open("cipher.txt","w") as f:
			f.write(repr(ciphertext)+"\n")
		d=cipher.new("bf-ofb",decryptkey,encrypt=False,iv=iv)
		deciph=d.update(ciphertext)+d.finish()
		self.assertEqual(deciph,data)
if __name__ == '__main__':
	unittest.main()
