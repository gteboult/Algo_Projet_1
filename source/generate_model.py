import sys
import os

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

	def writeObjFunction(self):
		objFunctionString = "Minimisze\n\tobj: "
		for j in range(self.J):
			objFunctionString += "x_"+str(j+1)+ " " + str(self.fj[j])+ " + "
			for i in range(self.I):
				objFunctionString += str(self.tij[i][j]) + " " + "y_" + str(i+1) + "_" + str(j+1) + " + "

		for k in range(len(self.pk)):
			objFunctionString += "z_" + str(k+1) + " " + str(self.pk[k]) + " + "

		objFunctionString = objFunctionString[:-3]
		return objFunctionString + "\n"

	def writeBinary(self):
		binaryString = "Binary\n"
		for j in range(self.J):
			binaryString += "\tx_" +str(j+1)+"\n"

		for j in range(self.J):
			for i in range(self.I):
				binaryString += "\ty_" + str(i+1) + "_" + str(j+1)+"\n"

		for k in range(len(self.S)):
			binaryString += "\tz_" + str(k+1) + "\n"

		return binaryString

	def writeFile(self):
		file = open(self.outputFileName, "w")
		file.write(self.writeObjFunction())
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