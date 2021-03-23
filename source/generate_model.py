import sys

class GenerateModel:

	def __init__(self , penalty):
		self.penalty = penalty
		self.I = 0
		self.J = 0
		self.K = 0

		self.fj = []
		self.di = []
		self.cj = []

		self.tij = []
		self.Sk = []

	def printData(self):
		print("I= " , self.I , "J= ", self.J,"K= " , self.K)

		print("fj " , self.fj)
		print("di " , self.di)
		print("cj " , self.cj)

		for i in range(len(self.tij)):
			print("tij ", self.tij[i])
		for k in range(len(self.Sk)):
			print("Sk " , self.Sk[k])

	def parseFile(self , fileName):
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
				self.Sk.append(fd.readline().strip("\n").split(" "))



if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Erreur, il n'y a pas tout les arguments")
		sys.exit(1) 
	else:
		model = GenerateModel(int(sys.argv[2]))
		model.parseFile(sys.argv[1])
		model.printData()