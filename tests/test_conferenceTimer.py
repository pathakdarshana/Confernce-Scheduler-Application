import unittest


from conferenceTimer import Time

class testTimer(unittest.TestCase):
	# test for the conferenceTimer.py
	def test_checkIfValueIsPM(self):
		# is the value of meridem successfully returned as PM
		result=Time.getMeridem(23)
		self.assertEqual(result,"PM")

	def test_chechIfValueIsAM(self):
		#is the value of meridem successfully returned as AM
		result=Time.getMeridem(9)
		self.assertEqual(result,"AM")
	def test_checkTheReturnedTime(self):
	 	# is the hour changed if minute is 60 or more
		resulthour,resultMin=Time.clock(2,69)
		self.assertEqual(resulthour,3)
		self.assertEqual(resultMin,9)
	def test_checkTheFormatPM(self):
		#the 12 hour format in which time is to be displayed
		resultantFormat=Time.timeFormat(23,50)
		self.assertEqual(resultantFormat,"11:50PM")
	def test_checkTheFormatAM(self):
		#the 12 hour format in which time is to be displayed
		resultantFormat=Time.timeFormat(0,50)
		self.assertEqual(resultantFormat,"00:50AM")


if __name__=='__main__':
	unittest.main()
