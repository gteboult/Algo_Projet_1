import sys
import os

TAB = "    "

class GenerateModel:


	def __init__(self , penalty , fileName):

		self.penalty = penalty
		self.fileToParse = fileName;
		self.instanceNumber = fileName[:-4][-1]

		self.outputFileName = ""

		self.I = 0
		self.J = 0
		self.K = 0

		self.fj = []
		self.di = []
		self.cj = []

		self.tij = []
		self.S = []
		self.pk = []


	def startGenerating(self):
		self.parseFile();
		self.createPenalty();
		self.createFile();
		self.writeFile();

	def parseFile(self):

		fileName = self.fileToParse;
		with open(fileName) as fd:
			line = fd.readline().split(" ")
			self.I = int(line[0])
			self.J = int(line[1])
			self.K = int(line[2])

			self.fj = fd.readline().strip("\n").split(" ")
			self.di = fd.readline().strip("\n").split(" ")
			self.cj = fd.readline().strip("\n").split(" ")

			for i in range(self.I):
				self.tij.append(fd.readline().strip("\n").split(" "))

			for k in range(self.K):
				self.S.append(fd.readline().strip("\n").split(" "))

	def createPenalty(self):
		for k in range(len(self.S)):
			self.pk.append(self.S[k][-1])
			self.S[k] = self.S[k][:-1]

	def createFile(self):
		self.outputFileName = "model" + "_" + str(self.penalty) + "_" +str(self.I) +"_" + str(self.J) + "_" +self.instanceNumber + ".lp"
		if not os.path.exists(self.outputFileName):
			os.mknod(self.outputFileName)

	def writeOneFamilyOneCenterConstraint(self):
		constraintString = "Subject To\n"

		for i in range(self.I):

			cFamily = TAB + "c_family_" + str(i+1) + ": "
			for j in range(self.J):
				cFamily += "y_" + str(i+1) + "_" + str(j+1) + " + "
			cFamily = cFamily[:-3]
			cFamily += " = 1\n"

			constraintString += cFamily
		return constraintString

	def writeCapacityConstraint(self):
		constraintString = ""

		for j in range(self.J):
			cCapacity = TAB + "c_capacity_" + str(j+1) + ": "

			for i in range(self.I):
				cCapacity += str(self.di[i])  + "y_" + str(i+1) + "_" + str(j+1) + " + "
			cCapacity = cCapacity[:-3]
			cCapacity += " - " + str(self.cj[j]) + "x_" + str(j+1) + " <= 0\n"
			constraintString+= cCapacity

		return constraintString

	def writePenaltyConstraint(self):
		constraintString = ""

		for k in range(self.K):
			for lk_1 in range(len(self.S[k])):
				for lk_2 in range(len(self.S[k])):

					if not(lk_1 == lk_2):
						constraintString += TAB + "c_z" + str(k+1)+"_"+str(self.S[k][lk_1-1])+"_"+str(self.S[k][lk_2-1])+": z_" + str(k+1) + " - " + "x_" + str(self.S[k][lk_1-1])+ " - " + "x_" + str(self.S[k][lk_2-1]) + " >= -1\n"
						
		return constraintString

	def writeObjFunction(self):
		objFunctionString = "Minimize\n" + TAB+ "obj: "
		for j in range(self.J):
			objFunctionString += str(self.fj[j]) +"x_"+str(j+1)+ " + "
			for i in range(self.I):
				objFunctionString += str(self.tij[i][j]) + "y_" + str(i+1) + "_" + str(j+1) + " + "

		if(self.penalty == 1):
			for k in range(len(self.pk)):
				objFunctionString += str(self.pk[k]) + "z_" + str(k+1) + " + "

		objFunctionString = objFunctionString[:-3]
		return objFunctionString + "\n"

	def writeBinary(self):
		binaryString = "Binary\n"
		for j in range(self.J):
			binaryString += TAB +"x_" +str(j+1)+"\n"

		for j in range(self.J):
			for i in range(self.I):
				binaryString += TAB + "y_" + str(i+1) + "_" + str(j+1)+"\n"

		if(self.penalty == 1):
			for k in range(len(self.S)):
				binaryString += TAB + "z_" + str(k+1) + "\n"

		return binaryString

	def writeFile(self):
		file = open(self.outputFileName, "w")
		file.write(self.writeObjFunction())
		file.write(self.writeOneFamilyOneCenterConstraint())
		file.write(self.writeCapacityConstraint())
		if self.penalty == 1:
			file.write(self.writePenaltyConstraint())
		file.write(self.writeBinary())
		file.write("END")
		file.close()


	def printData(self):
		print("I= " , self.I , "J= ", self.J,"K= " , self.K)

		print("fj " , self.fj)
		print("di " , self.di)
		print("cj " , self.cj)

		for i in range(len(self.tij)):
			print("tij ", self.tij[i])
		for k in range(len(self.S)):
			print("S " , k , " " , self.S[k])

		print("pk " , self.pk)


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Erreur, il n'y a pas tout les arguments")
		sys.exit(1) 
	else:
		model = GenerateModel(int(sys.argv[2]) , sys.argv[1])
		model.startGenerating()