from .conferenceTimer import Time
from .registration import Registration
from .volunteer import Volunteer
import os

class Conference:
	def __init__(self, proposalDocumentFile, startTime, endTime, lunchStartTime, lunchEndTime, networkingStartTime):
		self.__proposals = self.__getProposal(proposalDocumentFile)
		self.__startTime = startTime
		self.__endTime = endTime
		self.__lunchStartTime = lunchStartTime
		self.__lunchEndTime = lunchEndTime
		self.__networkingStartTime = networkingStartTime
		self.__attendees = []
		self.__volunteers = []

	def signUpForRegistration(self,name,email):
		newRegistration = Registration(name,email)
		self.__attendees.append(newRegistration)

	def listAttendees(self):
		i = 0
		length = len(self.__attendees)
		if length == 0:
			print("No Attendes yet")
		else:
			print("Name  Email")
			while(i<length):
				print(self.__attendees[i])
				i+=1
				
	def updateNameOfAttendee(self,name,changeTo):
		i = 0
		while(i < len(self.__attendees)):
			if self.__attendees[i].get() == name:
				self.__attendees[i].setName(changeTo)
				print(self.__attendees[i])
				break
			else:
				i+=1	

	def deleteAttendee(self,name,email):
		i = 0
		length = len(self.__attendees)
		while(i < length):
			name1, email1 = self.__attendees[i].getAll()
			if name1 == name and email1 == email:
				self.__attendees.remove(self.__attendees[i])
			i+=1	
	
	def signUpForVolunteer(self,name,email):
		newVolunteer = Volunteer(name,email)
		self.__volunteers.append(newVolunteer)

	def listVolunteers(self):
		i = 0
		length = len(self.__volunteers)
		if length == 0:
			print("No Volunteers yet")
		else:
			print("Name  Email")	
			while(i < length):
				print(self.__volunteers[i])
				i+=1

	def updateNameOfVolunteer(self,name,changeTo):
		i = 0
		while(i < len(self.__volunteers)):
			if self.__volunteers[i].get() == name:
				self.__volunteers[i].setName(changeTo)
				print(self.__volunteers[i])
			else:
				i+=1				

	# Prints the final schedule with track number. 
	def printSchedule(self):
		i=0
		proposals = self.__getSchedule()
		finalSchedule = []
		cLength = len(proposals)
		while(i<cLength):
			print("\n")
			track = "Track "+ str(i+1) + ":"
			finalSchedule.append(track)
			print(track)
			conlength=len(proposals[i])
			j=0
			while (j<conlength):
				print(proposals[i][j])
				finalSchedule.append(proposals[i][j])
				j+=1
			i+=1
		return finalSchedule

	#  Make a group of events whose sum of duration is less than or equal to 60
	# This is to ensure effective utilisation of time slots.

	def __searchComplementaryElements(self, proposals,remainingTimeTo60):
		result = []
		sum = 0
		proposals = list(reversed(proposals))
		for index, proposal in enumerate(proposals):
			if proposal != None:
				sum += proposal[1]
				if sum <= remainingTimeTo60:
					result.append(index)
				else:
					sum -= proposal[1]
		return result

	# It arranges proposals to fill most of slots in a track.
	# It sorts the received proposals in ascending order of duration.
	# It's complementary event with duration closest to 60 minutes is searched from the end of proposals
	# By above steps events are grouped in sets of combined total duration of 60 minutes or less.

	def __getArrangedProposals(self):
		proposals = self.__proposals
		proposals = sorted(proposals, key = lambda x: x[1])
		length = len(proposals)
		i = 0
		finalResult = []
		while(i < length):
			if proposals[i] != None:
				# Checks if the event duration is equal to maximum possible talk duration as per assumption.
				if proposals[i][1] == 60:
					finalResult.append(proposals[i])
				else:
					remainingTimeTo60 = 60 - proposals[i][1]
					finalResult.append(proposals[i])
					# Event which has been grouped is set as None to avoid duplication.
					proposals[i] = None
					indicesToMake60 = self.__searchComplementaryElements(proposals, remainingTimeTo60)
					j = 0
					while(j < len(indicesToMake60)):
						indexInMainList = length - 1 - indicesToMake60[j]
						value = proposals[indexInMainList]
						finalResult.append(value)
						proposals[indexInMainList] = None
						j += 1
			i += 1
		return finalResult

	# Read input file line by line.
	def __getProposal(self, rawProposalDocument):
		try:
			# to check if the given input file is there or not
			if not os.path.exists(rawProposalDocument):
				raise Exception("File doesn't exist")
			inputfile = ""
			time = ""
			proposals = []
			with open(rawProposalDocument) as inputfile:
				counter = 0
				# Reading input line by line
				for line in inputfile:
					title = line.strip()
					# Ignoring empty lines
					if len(title) != 0:
						# Exctracing event duration from line, in integer format. .
						time = self.__getEventDuration(title)
						proposals.append([title, time])
			return proposals
		except Exception as e:
			print(str(e))
			exit(1)

	# Returns event duration in minutes.
	# Example:
		# 60min should return 60
		# lightning should return 5
	def __getEventDuration(self,lineFromFile):
		line = lineFromFile.split(" ")
		time=line[-1]
		if time=="lightning":
			time=5
		else:
			time=int(time.strip("min"))
		return time

	# Return message in specified format.
	# Example: 09:00AM Title 1 30min
	def __getMessage(self,hour, minute, message):
		return Time.timeFormat(hour, minute) + " " + message

	# Uses outputs from __getArrangedProposals() function and assigns time slot along with lunch and networking events.
	def __getSchedule(self):
		arrangedProposals = self.__getArrangedProposals()
		length = len(arrangedProposals)
		lunchNotDone = True
		currentEventStartHour = self.__startTime['hour']
		currentEventStartMin = self.__startTime['min']
		i = 0
		trackCounter = 0
		schedule = []
		currentTrack = []
		networkingTimeHour = self.__networkingStartTime['hour']
		networkingTimeMin = self.__networkingStartTime['min']
		schedule.append([])
		currentTrack = schedule[trackCounter]
		while(i < length):
			temp = currentEventStartMin + arrangedProposals[i][1]
			potentialEventEndHour,potentialEventEndMin = Time.clock(currentEventStartHour,temp)

			# Checking if event is moving past start of lunch time (end of morning session).
			# 
			if potentialEventEndHour == self.__lunchStartTime['hour'] and potentialEventEndMin > self.__lunchStartTime['min']:
				currentTrack.append(self.__getMessage(self.__lunchStartTime['hour'],self.__lunchStartTime['min'],"Lunch"))
				currentEventStartHour = self.__lunchEndTime['hour']
				currentEventStartMin = self.__lunchEndTime['min']
				lunchNotDone = False

			# Checking if event is moving past end time of afternoon session of current Track
			# Create new track if crossing end time

			if (potentialEventEndHour > self.__endTime['hour'] and potentialEventEndMin >= self.__endTime['min']) or (potentialEventEndHour == self.__endTime['hour'] and potentialEventEndMin > self.__endTime['min']):
				currentEventStartHour = self.__startTime['hour']
				currentEventStartMin = self.__startTime['min']
				trackCounter += 1
				lunchNotDone = True
				schedule.append([])
				currentTrack = schedule[trackCounter]

			# Adding current event to final list of track
			currentTrack.append(self.__getMessage(currentEventStartHour,currentEventStartMin,arrangedProposals[i][0]))

			# Setting potential next event's start time
			currentEventStartMin = currentEventStartMin + arrangedProposals[i][1]
			currentEventStartHour, currentEventStartMin = Time.clock(currentEventStartHour,currentEventStartMin)

			# Deciding networking event time
			# Not before networking start time and not after conference end time(5:00PM)
			# Setting networking event time to the maximum time from all tracks by abiding by above convention
			if currentEventStartHour == networkingTimeHour:
				if currentEventStartMin > networkingTimeMin:
					networkingTimeMin = currentEventStartMin
			elif currentEventStartHour > networkingTimeHour:
				networkingTimeHour = currentEventStartHour
				networkingTimeMin = currentEventStartMin
			i+=1

		# Adding common networking event schedule in final track lists
		i=0
		while(i<len(schedule)-1):
			schedule[i].append(self.__getMessage(networkingTimeHour,networkingTimeMin,"Networking event"))
			i+=1

		# Scheduling lunch time for the track which ends before the lunch time
		if lunchNotDone:
			schedule[i].append(self.__getMessage(self.__lunchStartTime['hour'],self.__lunchStartTime['min'],"Lunch"))
		schedule[i].append(self.__getMessage(networkingTimeHour,networkingTimeMin,"Networking event"))

		return schedule
