import math

class Stronghold:
	def __init__(self):
		self.name = raw_input("Please enter a name for this stronghold: ")
		self.guesses = []
		self.vectors = []
		self.lines = []
		
	def addNewVector(self):
		vx = float(raw_input("What is the X Coordinate? "))
		vy = float(raw_input("What is the Z Coordinate? "))
		vt = float(raw_input("What is the angle? "))

		
		#Assuming 0 deg = N, 90 deg = W, 180 deg = S, 270 = E
		angle = (math.pi/180.0) * ((vt + 90)%180)
		
		#Calculate slope
		if((angle == 0) or (angle == (2.0*math.pi))):
			m = 0
		else:
			m = math.tan(angle)
			
		vector = [vx,vy,vt,angle]
		self.vectors.append(vector)			

		#Calculate Y Intercept
		b = vy - (m * vx)
		line = [m,b]
		self.lines.append(line)
		
	def estimateLocation(self):
		if(len(self.lines) == 1):
			print "One more vector needed for estimation."
			return
		if(len(self.lines) == 0):
			print "Two more vectors needed for estimation."
			return
		
		for i in range (0,len(self.lines)-1):
			for j in range (i+1,len(self.lines)):
				#X Guess is:
				gx = (self.lines[i][1] - self.lines[j][1])/(self.lines[j][0] - self.lines[i][0])
				#Y Guess is
				gy = self.lines[i][0]*gx + self.lines[i][1]
				#Calculating Confidence
				#How far away from the guess where each of the sample points?
				deltaX1 = gx - self.vectors[i][0]
				deltaY1 = gy - self.vectors[i][1]
				deltaX2 = gx - self.vectors[j][0]
				deltaY2 = gy - self.vectors[j][1]
				#Check to see if the Eyes actually pointed in the direction of the guess
				wrongAim = False
				theta1 = self.vectors[i][2]
				if (theta1 > -180) and (theta1 <-90):
					if deltaX1 < 0:
						wrongAim = True
					if deltaY1 > 0:
						wrongAim = True
				elif (theta1 > -90) and (theta1 < 0):
					if deltaX1 < 0:
						wrongAim = True
					if deltaY1 < 0:
						wrongAim = True
				elif (theta1 > 0) and (theta1 < 90):
					if deltaX1 > 0:
						wrongAim = True
					if deltaY1 < 0:
						wrongAim = True
				elif (theta1 > 90) and (theta1 < 180):
					if deltaX1 > 0:
						wrongAim = True
					if deltaY1 > 0:
						wrongAim = True
			
				#Check Vector 2
				theta2 = self.vectors[j][2]
				if (theta2 > -180) and (theta2 <-90):
					if deltaX2 < 0:
						wrongAim = True
					if deltaY2 > 0:
						wrongAim = True
				elif (theta2 > -90) and (theta2 < 0):
					if deltaX2 < 0:
						wrongAim = True
					if deltaY2 < 0:
						wrongAim = True
				elif (theta2 > 0) and (theta2 < 90):
					if deltaX2 > 0:
						wrongAim = True
					if deltaY2 < 0:
						wrongAim = True
				elif (theta2 > 90) and (theta2 < 180):
					if deltaX2 > 0:
						wrongAim = True
					if deltaY2 > 0:
						wrongAim = True
						   
				if(wrongAim):
					print "WARNING! Points ",
					print self.vectors[i],
					print self.vectors[j],
					print " aim at two different strongholds."
					
				d1 = math.sqrt((deltaX1 * deltaX1) + (deltaY1 * deltaY1))
				d2 = math.sqrt((deltaX2 * deltaX2) + (deltaY2 * deltaY2))
				#Angle Variance is 0.6 degrees, taken from how much of an angle variance can be seen when looking at a thrown Eye of Ender
				#Second term comes from the angle between the vectors. If it is too tight, the value is likely wrong
				variance = 0.6 * (math.pi/180)
				SA = (4.0 * variance * variance * d1 * d2)
				AngleCompensation = math.sin(self.vectors[i][3] - self.vectors[j][3])
				confidence = abs(9.0 * AngleCompensation / SA)
				guess = [gx,gy,confidence, SA, AngleCompensation]
				self.guesses.append(guess)
		
		highPoint = self.guesses[0]
		#Find highest confidence rating
		for i in range (1,len(self.guesses)):
			print self.guesses[i]
			curPoint = self.guesses[i]
			if (curPoint[2] > highPoint[2]):
				highPoint = curPoint
		
		print "Best guess is at coordinates %.0f = X, %.0f = Z. Confidence rating: %0.2f%%. SA = %.0f, AC = %0.5f" % (highPoint[0],highPoint[1],highPoint[2],highPoint[3],highPoint[4])
			
				
def promptMode():
	good = False
	while(not(good)):
		print "Mode 1:		Begin hunt for new Stronghold"
		print "Mode 2:		Resume hunt for Stronghold"
		print "Mode 3:		List all known Strongholds"
		print "Mode 4:		Brings up the Help page."
		print "Mode 5:		Import Stronghold File"
		mode = raw_input("\n\nSelect Mode by number: ")
		if not((mode == "1") or (mode == "2") or (mode == "3") or (mode == "4") or (mode == "5")):
			print "\"%s\" is an invalid mode. Please enter a number 1 through 5."
		else:
			good = True
	return int(mode)
		
def mainDriver():
	StrongholdList = []
	print "==================================="
	print "Welcome to Stronghold Locator V4.0!"
	print "===================================\n\n",
	      #012345678901234567890123456789012345678901234567890123456789
	print "This program automates the process of finding strongholds."
	print "To utilize this tool, it is recommended to have at least two"
	print "Eyes of Ender and enough gear to go traveling around for"
	print "two Minecraft days. For best performance, try to take data"
	print "points at least a few hundred meters away from each other."
	print "\n\nFor more help, type 4 at the prompt.\n\n\n"
	
	mode = promptMode()
	if mode == 1:
		ns = Stronghold()
		findStronghold(ns)
		StrongholdList.append(ns)
	elif mode == 2:
		i = raw_input("Which Stronghold? (Enter ID #): ")
		st = StrongholdList[i]
		findStronghold(st)
	elif mode == 3:
		displayLocations(StrongholdList)
	elif mode == 4:
		help()
	elif mode == 5:
		StrongholdList = importStrongholds(StrongholdList)
		
def testDriver():
	st = Stronghold()
	while(1):
		st.addNewVector()
		st.estimateLocation()


if __name__ == '__main__':
	#mainDriver()
	testDriver()

