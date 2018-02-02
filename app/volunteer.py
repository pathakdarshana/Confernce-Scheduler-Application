class Volunteer:
	def __init__(self,name,email):
		self.__name = name
		self.__email = email

	def get(self):
		return self.__name

	def setName(self,changeTo):
		self.__name = changeTo		


	def __str__(self):
		s = '1.) Name of the Volunteer: '+ self.__name +" "+ "2.) Email of the Volunteer: "+self.__email
		return s