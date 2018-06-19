import os
from configparser import ConfigParser

PATH = "{root}/{file}"


class Config:
	def __init__(self, file):
		self.config = ConfigParser()
		self.path = PATH.format(
			root=os.path.abspath(os.path.dirname(__file__)),
			file=file
		)

		try:
			self.config.read(self.path)
			self.data = {}
			self.load()
		except Exception as e:
			print(e)
			raise e

	def load(self):
		for section in self.config.sections():
			self.data[section] = dict(self.config[section].items())

	def get(self, section, key):
		if section in self.config.sections():
			return self.config.get(section, key)
		return None
