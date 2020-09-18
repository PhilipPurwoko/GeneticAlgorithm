class Individu():
	panjangGen = 5
	genRange = (0,100)
	def generate(self):
		return [random.randint(self.genRange[0],self.genRange[1]) for i in range(self.panjangGen)]

class Generasi():
	def __init__(self,individu,jumlahIndividu):
		self.generasi = [individu() for i in range(jumlahIndividu)]
	def lihat(self):
		print(f'{len(self.generasi)} individu')
		for individu in self.generasi:
			print(individu)

class Evolusi():
	def __init__(self,generasi):
		self.target = 250
		self.selection = 0.6
		self.getUpChance = 0.3
		self.mutateChance = 0.7
		self.fitness = self.fitnessGen(generasi)
		self.limit = int(self.selection * len(self.fitness))
	def lihat(self):
		print(f'Target : {self.target}')
		print('{:<10} {:<10}'.format('Fitness','Gen individu'))
		for individu in self.fitness:
			print(individu)
	def fitnessInd(self,individu):
		return abs(sum(individu) - self.target)
	def fitnessGen(self,generasi):
		fitness = []
		for individu in generasi:
			fitness.append((self.fitnessInd(individu),individu))
		return fitness
	def mutate(self,individu):
		individu_baru = individu[1]
		if random.random() < self.mutateChance:
			individu_baru[random.randint(0,len(individu)-1)] = random.randint(min(individu[1]),max(individu[1]))
		return [(self.fitnessInd(individu_baru)),individu_baru]
	def eliminate(self):
		generasi = sorted(self.fitness)
		top_generasi = generasi[:self.limit]
		return top_generasi
	def bottomChance(self):
		generasi = sorted(self.fitness)
		bottom_generasi = generasi[self.limit:]
		getUp = list()
		for individu in bottom_generasi:
			if random.random() < self.getUpChance:
				getUp.append(individu)
		return getUp
	def generateParrent(self):
		parrent = self.eliminate()
		getUped = self.bottomChance()
		if len(getUped) > 0:
			for selected in getUped:
				parrent.append(selected)
		for index,individu in enumerate(parrent):
			parrent[index] = self.mutate(individu)
		return parrent
	def crossOver(self):
		total_individu = 10
		generasi = self.generateParrent()
		parrent = generasi.copy()
		half_len = len(parrent[0])//2
		while len(generasi) < 10:
			father = random.randint(0,len(parrent)-1)
			mother = random.randint(0,len(parrent)-1)
			if father != mother:
				individu_baru = parrent[father][1][:half_len] + parrent[mother][1][half_len:]
				individu_baru = [(self.fitnessInd(individu_baru)),individu_baru]
				generasi.append(individu_baru)
		return sorted(generasi)
	def evolve(self):
		for i in range(100):
			print(f'Evolving generation {i+1}')
			self.fitness = self.crossOver()
	def bestIndividu(self):
		return self.fitness[0][1]

#----------------------------------------------------------------------------------------

def main():
	individu = Individu()
	generasi = Generasi(individu.generate,10)
	evolusi = Evolusi(generasi.generasi)
	
	for i in range(5):
		evolusi.evolve()
		if evolusi.fitness[0][0] > 5:
			continue
		else:
			break

	evolusi.lihat()
	print(f'\nBest individu : \n{evolusi.bestIndividu()}')

if __name__ == '__main__':
	import random
	main()