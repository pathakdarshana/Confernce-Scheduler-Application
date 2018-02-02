import sys
from app.conference import Conference

print("\nEnter full path of selected proposals with time duration: ", end="")
proposalDocumentFile = input()

startTime = { 'hour': 9,'min': 0 }
endTime = { 'hour': 17, 'min': 0 }
lunchStartTime = { 'hour': 12, 'min': 0 }
lunchEndTime = { 'hour': 13, 'min': 0 }
networkingStartTime = { 'hour': 16, 'min': 0 }


# Object creation of Conference class
currentConference = Conference(proposalDocumentFile, startTime, endTime, lunchStartTime, lunchEndTime, networkingStartTime)
entry = 'start'
while(entry != 'exit'):
	print("""
	1. Enter 1 to SignUp for the conference
	2. Enter 2 to Register as a volunteer
	3. Enter 3 to list all the Attendees
	4. Enter 4 to list all the volunteers
	5. Enter 5 to update name of attendee
	6. Enter 6 to update name of volunteer
	7. Enter 7 to delete the attendee
	8. Enter 8 to exit
	9. Enter 9 to print the schedule
	""")
	entry = input()

	if entry == '1':
		print("Enter name of attendee: ", end="")
		name = input()
		print("Enter email of attendee: ", end="")
		email = input()
		currentConference.signUpForRegistration(name,email)
	elif entry == '2':
		print("Enter the name of volunteer: ",end="")
		name = input()
		print("Enter the email of volunteer: ",end="")
		email = input()
		currentConference.signUpForVolunteer(name,email)
	elif entry == '3':
		currentConference.listAttendees()
	elif entry == '4':
		currentConference.listVolunteers()
	elif entry == '5':
		print("Enter the name of attendee")
		name = input()
		print("Enter the changed name")
		changedName = input()
		currentConference.updateNameOfAttendee(name,changedName)
	elif entry == '6':
		print("Enter the name of volunteer")
		name = input()
		print("Enter the changed name")
		changedName = input()
		currentConference.updateNameOfVolunteer(name,changedName)
	elif entry == '7':
		print("Enter the name of attendee you want to delete")
		name = input()
		print("Enter the email of the attendee you want to delete")
		email = input()
		currentConference.deleteAttendee(name, email)		
	elif entry == '8':
		exit(0)	
	elif entry == '9':
		currentConference.printSchedule()	
	else:
		print("Wrong! enter the right keyword")


