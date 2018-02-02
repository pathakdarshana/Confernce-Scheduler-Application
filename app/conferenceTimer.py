class Time:
	def __init__(self):
		pass
	@classmethod
	def getMeridem(self,hour):
		if hour < 12:
			return "AM"
		else:
			return "PM"
	@classmethod
	def clock(self,hour,min):
		if min>=60:
			hour+=1
		hour=hour%24
		minNew=min%60
		return hour,minNew
	@classmethod
	def timeFormat(self,hour,min):
		meridem = self.getMeridem(hour)
		if hour>12:
			hour=hour%12
		return '{0:02d}:{1:02d}{2:s}'.format(hour,min,meridem)
	@classmethod
	def convertTo24Hour(self,hour,minute,meridem):
		if meridem == "PM" and hour < 12:
			hour = hour + 12
		return hour, minute
