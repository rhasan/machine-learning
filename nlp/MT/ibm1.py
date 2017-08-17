from collections import defaultdict
from sets import Set

"""
IBM model 1 for machine translation 
"""

TRAINING_FILE_EN = "corpus.en"
TRAINING_FILE_ES = "corpus.es"

DEV_FILE_EN = "dev.en"
DEV_FILE_ES = "dev.es"

TEST_FILE_EN = "test.en"
TEST_FILE_ES = "test.es"
EMPTY_STRING = "EMPTY_STRING"
NULL_WORD = "NULL"

T_FILE = "ibm1.t.es.en.param"

DEV_OUT = "alignment_dev.p1.out"
TEST_OUT = "alignment_test.p1.out"

#number of iteration for EM algorithm
S = 5

class IBM_Model_1:

	def __init__(self,f_lanuage_file,e_language_file,t_param_file,load_t_from_file=False):
		
		self.f_lanuage_file = f_lanuage_file
		self.e_language_file = e_language_file
		self.t_param_file = t_param_file
		
		
		self.t = defaultdict(lambda: 0.0)
		self.e = list()
		self.f = list()		
		
				
		
		if load_t_from_file==False:
			self.load_training()
			self.em_algorithm()
			self.save_t()
		else:
			self.load_t()
			


	def load_training(self):


		self.f_words = Set()

		self.e.append(EMPTY_STRING) #dummy entry for 1 based index
		self.f.append(EMPTY_STRING) #dummy entry for 1 based index

		f_file = open(self.f_lanuage_file,'r')
		e_file = open(self.e_language_file,'r')

		e_tmp = list()
		f_tmp = list()
		


		translation_possibility = dict()
		#self.original_line_number = dict()

		for line in e_file:
			#self.english.append(line)
			e_tmp.append(line)

		for line in f_file:
			#self.spanish.append(line)
			f_tmp.append(line)

		#line_num = 0
		for i in range(len(e_tmp)):
			line_e = e_tmp[i].strip()
			line_f = f_tmp[i].strip()
			if line_e and line_f:

				e_words = list()
				f_words = list()
				f_words.append(NULL_WORD)
				e_words.append(NULL_WORD)
				f_words.extend(line_f.split())
				e_words.extend(line_e.split())
				
				self.f.append(f_words)
				self.e.append(e_words)

				for e_word in e_words:
					for f_word in f_words[1:]:
						self.t[(f_word,e_word)]=0.0;
						translation_possibility.setdefault(e_word,0)
						translation_possibility[e_word] += 1;


		for (key,value) in self.t.items():
			(f_word,e_word) = key
			self.t[key] = 1.0/translation_possibility[e_word]

		self.N = len(self.e)

		f_file.close()
		e_file.close()



	def delta(self,k,i,j,normalizer):
		fi = self.f[k][i]
		ej = self.e[k][j]
		num = self.t[(fi,ej)]

		return num/normalizer
		#pass


	def get_normalizer(self,k,i):
		fi = self.f[k][i]
	
		den = 0.0
		for ejj in self.e[k]:
			den += self.t[(fi,ejj)]
		return den

	def em_algorithm(self):
		
		#t(f,e) is already inisialized during the load with value 1/n(e) 
		#where n(e) is the number of different words that occur in any translation of a sentence containing e.

		for s in range(1,S+1):
			count = defaultdict(lambda: 0)
			for k in range(1,self.N):
				for i in range(1,len(self.f[k])): #mk
					norm = self.get_normalizer(k,i)
					for j in range(len(self.e[k])): #lk
						count[(self.e[k][j],self.f[k][i])] = count[(self.e[k][j],self.f[k][i])] + self.delta(k,i,j,norm)
						count[(self.e[k][j])] = count[(self.e[k][j])] + self.delta(k,i,j,norm)
						count[(j,i,len(self.e[k]),len(self.f[k]))] = count[(j,i,len(self.e[k]),len(self.f[k]))]	 + self.delta(k,i,j,norm)
						count[(i,len(self.e[k]),len(self.f[k]))] = count[(i,len(self.e[k]),len(self.f[k]))] + self.delta(k,i,j,norm)
			
			#set t(f|e) = c(e,f)/c(e)
			for (key,value) in self.t.items():
				(f,e) = key
				self.t[(f,e)]=count[(e,f)]/count[(e)]

	def save_t(self):
		fo = open(self.t_param_file,"wb")
		
		for (key,value) in self.t.items():
			(f,e) = key
			new_line = f+" "+e+" "+str(self.t[(f,e)])
			fo.write(new_line+'\n')
		fo.close()

	def load_t(self):
		t_in_file = open(self.t_param_file,"r")
		for line in t_in_file:
			(f,e,value) = line.split()
			value = float(value)
			self.t[(f,e)] = value
		t_in_file.close()

	def align_dataset(self,f_file,e_file,out_file):
		dev_e_file = open(e_file,"r")
		dev_f_file = open(f_file,"r")
		dev_out_file = open(out_file,"wb")

		dev_e = list()
		dev_f = list()

		for line in dev_f_file:
			words = list()
			words.append(NULL_WORD)
			words.extend(line.split())
			dev_f.append(words)


		for line in dev_e_file:
			words = list()
			words.append(NULL_WORD)
			words.extend(line.split())
			dev_e.append(words)

		for i in range(len(dev_f)):
			f_sen = dev_f[i]
			e_sen = dev_e[i]
			f_words = f_sen[1:]
			fi = 1;
			for f_word in f_words:
				max_t = float('-inf')
				max_ei = 0
				ei = 0
				for e_word in e_sen:
					if max_t < self.t[(f_word,e_word)]:
						max_t = self.t[(f_word,e_word)]
						max_ei = ei
					ei+=1
				
				# print (i+1), max_ei, fi
				new_line = str(i+1)+" "+str(max_ei)+" "+str(fi)
				dev_out_file.write(new_line+'\n')
				fi+=1

		dev_out_file.close()
		dev_e_file.close()
		dev_f_file.close()


def main():
	model = IBM_Model_1(TRAINING_FILE_ES,TRAINING_FILE_EN,T_FILE,True)
	#print "English:", model.e[5]
	#print "Spanish:", model.f[5]
	print model.t[("la","the")]

	model.align_dataset(DEV_FILE_ES,DEV_FILE_EN,DEV_OUT)
	#model.align_dataset(TEST_FILE_ES,TEST_FILE_EN,TEST_OUT)

if __name__ == "__main__":
	main()
