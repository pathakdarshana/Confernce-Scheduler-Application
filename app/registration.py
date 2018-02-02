class Registration:
	def __init__(self,name,email):
		self.__name = name
		self.__email = email

	def __setName(self,changeTo):
		self.__name = changeTo

	def __get(self):
		return self.__name

	def __getAll(self):
		return self.__name, self.__email	
	

	def __str__(self):
		s = self.__name +" "+ self.__email
		return s	