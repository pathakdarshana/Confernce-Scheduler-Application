import os
import unittest
from app.conference import Conference
from app.conferenceTimer import Time
from app.registration import Registration

cwd = os.path.dirname(os.path.abspath(__file__))
testDataDir = cwd + "/data"

# Default value of the test input file
proposalDocumentFile = testDataDir + "/test_inputFile.txt"
startTime = { 'hour': 9,'min': 0 }
endTime = { 'hour': 17, 'min': 0 }
lunchStartTime = { 'hour': 12, 'min': 0 }
lunchEndTime = { 'hour': 13, 'min': 0 }
networkingStartTime = { 'hour': 16, 'min': 0 }

class TestConferenceMethod(unittest.TestCase):

	def test_PrintSchedule(self):
		testConference = Conference(proposalDocumentFile, startTime, endTime, lunchStartTime, lunchEndTime, networkingStartTime)

		expectedResult = [
			'Track 1:',
			'09:00AM Rails for Python Developers lightning',
			'09:05AM Clojure Ate Scala (on my project) 45min',
			'09:50AM Lua for the Masses 30min',
			'10:20AM User Interface CSS in Rails Apps 30min',
			'10:50AM Woah 30min',
			'11:20AM A World Without HackerNews 30min',
			'12:00PM Lunch',
			'01:00PM Sit Down and Write 30min',
			'01:30PM Ruby vs. Clojure for Back\xadEnd Development 30min',
			'02:00PM Programming in the Boondocks of Seattle 30min',
			'02:30PM Overdoing it in Python 45min',
			'03:15PM Ruby Errors from Mismatched Gem Versions 45min',
			'04:00PM Common Ruby Errors 45min',
			'05:00PM Networking event',
			'Track 2:',
			'09:00AM Accounting\xadDriven Development 45min',
			'09:45AM Pair Programming vs Noise 45min',
			'10:30AM Writing Fast Tests Against Enterprise Rails 60min',
			'12:00PM Lunch',
			'01:00PM Communicating Over Distance 60min',
			'02:00PM Rails Magic 60min',
			'03:00PM Ruby on Rails: Why We Should Move On 60min',
			'04:00PM Ruby on Rails Legacy App Maintenance 60min',
			'05:00PM Networking event'
		]
		result = testConference.printSchedule()
		i = 0
		while(i < len(result)):
			self.assertEqual(result[i] , expectedResult[i])
			i+=1

	# Checking if start time is equal to default value (9:00AM)
	def test_checkingStartTime(self):
		testConference = Conference(proposalDocumentFile, startTime, endTime, lunchStartTime, lunchEndTime, networkingStartTime)
		result = testConference.printSchedule()
		# Getting track's starting event from final schedules
		trackStartTime = result[1]
		hour, minute, meridem = self.__extractTime(trackStartTime)
		hour1, minute1 = Time.convertTo24Hour(hour,minute,meridem)
		message = str(hour) + ":" + str(minute) + meridem + " # " + str(hour1) + ":" + str(minute1)
		# Checking if track starts at event start time (09:00PM)
		self.assertTrue(self.__isTimeEqual(hour1, minute1, startTime['hour'], startTime['min']))

	def test_lunchTimeIsAsExpected(self):
		testConference = Conference(proposalDocumentFile, startTime, endTime, lunchStartTime, lunchEndTime, networkingStartTime)
		result = testConference.printSchedule()
		# Getting lunch event from final schedules
		lunch = result[7]
		hour, minute, meridem = self.__extractTime(lunch)
		hour1, minute1 = Time.convertTo24Hour(hour,minute,meridem)
		message = str(hour) + ":" + str(minute) + meridem + " # " + str(hour1) + ":" + str(minute1)
		# Checking if lunch starts at lunch start time (12:00PM)
		self.assertTrue(self.__isTimeEqual(hour1, minute1, lunchStartTime['hour'], lunchStartTime['min']))

	def test_networkingEventNotAfter5andNotBefore4(self):
		testConference = Conference(proposalDocumentFile, startTime, endTime, lunchStartTime, lunchEndTime, networkingStartTime)
		result = testConference.printSchedule()
		# Getting networking event from final schedules
		networkingEvent1 = result[14]
		hour, minute, meridem = self.__extractTime(networkingEvent1)
		hour1, minute1 = Time.convertTo24Hour(hour,minute,meridem)

		# Checking if not after event end time (5:00PM)
		self.assertTrue(self.__isTimeMoreOrEqual(endTime['hour'], endTime['min'], hour1, minute1,))

		# Checking if not before networking event start time (4:00PM)
		self.assertTrue(self.__isTimeMoreOrEqual(hour1, minute1, networkingStartTime['hour'], networkingStartTime['min']))

	def test_networkingEventSameInAllTracks(self):
		testConference = Conference(proposalDocumentFile, startTime, endTime, lunchStartTime, lunchEndTime, networkingStartTime)
		result = testConference.printSchedule()
		networkingEvent1 = result[14]
		networkingEvent2 = result[24]
		self.assertEqual(networkingEvent1, networkingEvent2)

	def test_signUpForRegistration(self,):
		testConference = Conference(proposalDocumentFile, startTime, endTime, lunchStartTime, lunchEndTime, networkingStartTime)
		result = testConference.signUpForRegistration('darshana','pathak@gmail.com')
			

	def __isTimeMoreOrEqual(self,hour1,min1,hour2,min2):
		timeMoreOrEqual = False
		if hour1 == hour2:
			if min1 >= min2:
				timeMoreOrEqual = True
		elif hour1 > hour2:
			timeMoreOrEqual = True
		return timeMoreOrEqual

	def __isTimeEqual(self,hour1,min1,hour2,min2):
		if hour1 == hour2 and min1 == min2:
			return True
		else:
			return False

	def __extractTime(self,input):
		time = input.split(' ')[0]
		hour = int(time[0:2])
		minute = int(time[3:5])
		meridem = time[5:]
		return hour, minute, meridem
if __name__=='__main__':
	unittest.main()
