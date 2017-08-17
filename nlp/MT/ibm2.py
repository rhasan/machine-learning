from collections import defaultdict
from sets import Set
from ibm1 import IBM_Model_1

"""
IBM model 2 for machine translation
Note: initializing t(f|e) in em algorithm by t(f|e) parameter values computed by IBM mode 1 
"""

TRAINING_FILE_EN = "corpus.en"
TRAINING_FILE_ES = "corpus.es"

DEV_FILE_EN = "dev.en"
DEV_FILE_ES = "dev.es"

TEST_FILE_EN = "test.en"
TEST_FILE_ES = "test.es"
EMPTY_STRING = "EMPTY_STRING"
NULL_WORD = "NULL"

IBM1_T_FILE_es_en = "ibm1.t.es.en.param"
IBM1_T_FILE_en_es = "ibm1.t.en.es.param"

IBM2_T_FILE_es_en = "ibm2.t.es.en.param"
IBM2_T_FILE_en_es = "ibm2.t.en.es.param"

IBM2_Q_FILE_es_en = "ibm2.q.es.en.param"
IBM2_Q_FILE_en_es = "ibm2.q.en.es.param"


DEV_OUT = "alignment_dev.p2.out"
TEST_OUT = "alignment_test.p2.out"

#number of iteration for EM algorithm
S = 5

class IBM_Model_2:

	#def __init__(self,f_lanuage_file,e_language_file,ibm1_t_param_f_e_file,ibm1_t_param_e_f_file,load_ibm1_t_from_file=False):
	def __init__(self,f_lanuage_file,e_language_file,ibm1_t_param_file,ibm2_t_param_file,ibm2_q_param_file,ibm2_load_params_from_file=True):	
		self.f_lanuage_file = f_lanuage_file
		self.e_language_file = e_language_file
		self.ibm1_t_param_f_e_file = ibm1_t_param_file
		self.t_param_file = ibm2_t_param_file
		self.q_param_file = ibm2_q_param_file
		#self.ibm1_t_param_e_f_file = ibm1_t_param_e_f_file
		
		#self.load_training()
		
		self.ibm1_f_e = IBM_Model_1(self.f_lanuage_file,self.e_language_file,self.ibm1_t_param_f_e_file,True)
		#self.ibm1_e_f = IBM_Model_1(self.e_language_file,self.f_lanuage_file,self.ibm1_t_param_e_f_file,load_ibm1_t_from_file)
		
		self.t = defaultdict(lambda: 0.0)
		self.t = self.ibm1_f_e.t.copy()

		#using the load functions defined in ibm1
		self.ibm1_f_e.load_training()
		
		self.N = self.ibm1_f_e.N
		
		
		self.e = self.ibm1_f_e.e
		self.f = self.ibm1_f_e.f
		#self.m = list()
		#self.l = list()
		self.q = defaultdict(lambda: 0.0)
		#self.q = dict()
		# for fi in range(1,len(self.f)):
		# 	self.m.append(len(self.f[fi]))
		# for ei in range(1,len(self.e)):
		# 	self.l.append(len(self.e[ei]))

		if ibm2_load_params_from_file==False:		
			self.calculate_t_and_q()
			self.save_t()
			self.save_q()

		else:
			self.load_t_and_q()
	

	def load_t_and_q(self):
		
		t_in_file = open(self.t_param_file,"r")
		for line in t_in_file:
			(f,e,value) = line.split()
			value = float(value)
			self.t[(f,e)] = value
		t_in_file.close()


		q_in_file = open(self.q_param_file,"r")
		qc=0
		for line in q_in_file:
			(j,i,l,m,value) = line.split()
			value = float(value)
			self.q[(int(j),int(i),int(l),int(m))] = value
			qc+=1
		print "q count:",qc
		q_in_file.close()

	def calculate_t_and_q(self):
		for k in range(1,self.N):
			l = len(self.e[k])
			m = len(self.f[k])
			for i in range(1,len(self.f[k])): #mk
				for j in range(len(self.e[k])): #lk

					key = (j,i,l,m)
					self.q[key] = 1.0/float(l+1)
	
		self.em_algorithm()


	def delta(self,k,i,j,normalizer):
		fi = self.f[k][i]
		ej = self.e[k][j]
		
		mk = len(self.f[k])
		lk = len(self.e[k])


		num = self.t[(fi,ej)] * self.q[(j,i,lk,mk)]

		return num/normalizer
		#pass


	def get_normalizer(self,k,i):
		fi = self.f[k][i]
		mk = len(self.f[k])
	
		den = 0.0
		j = 0
		for ejj in self.e[k]:
			lk = len(self.e[k])
			den += (self.t[(fi,ejj)]*self.q[(j,i,lk,mk)])
			j += 1
		return den

	def em_algorithm(self):
		
		#t(f,e) is already inisialized during the load with value 1/n(e) 
		#where n(e) is the number of different words that occur in any translation of a sentence containing e.

		for s in range(1,S+1):
			count = defaultdict(lambda: 0)
			#count = dict()
			for k in range(1,self.N):
				lk = len(self.e[k])
				mk = len(self.f[k])
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
			
			for k in range(1,self.N):
				l = len(self.e[k])
				m = len(self.f[k])
				for i in range(1,len(self.f[k])): #mk
					for j in range(len(self.e[k])): #lk
						key = (j,i,l,m)
						self.q[key] = count[(j,i,l,m)]/count[(i,l,m)]
		
	def save_t(self):
		fo = open(self.t_param_file,"wb")
		
		for (key,value) in self.t.items():
			(f,e) = key
			new_line = f+" "+e+" "+str(self.t[(f,e)])
			fo.write(new_line+'\n')
		fo.close()

	def save_q(self):
		fo = open(self.q_param_file,"wb")
		
		for (key,value) in self.q.items():
			(j,i,l,m) = key
			new_line = str(j)+" "+str(i)+" "+" "+str(l)+" "+str(m)+" "+str(value)
			fo.write(new_line+'\n')
		fo.close()

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
			m = len(f_sen)
			l = len(e_sen)

			f_words = f_sen[1:]
			fi = 1;
			for f_word in f_words:
				max_t = float('-inf')
				max_ej = 0
				ej = 0
				for e_word in e_sen:
					val = self.t[(f_word,e_word)] * self.q[(ej,fi,l,m)]
					if max_t < val:
						max_t = val
						max_ej = ej
					ej+=1
				
				# print (i+1), max_ej, fi
				new_line = str(i+1)+" "+str(max_ej)+" "+str(fi)
				dev_out_file.write(new_line+'\n')
				fi+=1

		dev_out_file.close()
		dev_e_file.close()
		dev_f_file.close()
		
def main():
	model = IBM_Model_2(TRAINING_FILE_ES,TRAINING_FILE_EN,IBM1_T_FILE_es_en,IBM2_T_FILE_es_en,IBM2_Q_FILE_es_en,True)
	

	#model = IBM_Model_2(TRAINING_FILE_ES,TRAINING_FILE_EN,IBM1_T_FILE_es_en,IBM1_T_FILE_en_es,True)
	print "f=la e=the", model.t[("la","the")]
	#model.align_dataset(DEV_FILE_ES,DEV_FILE_EN,DEV_OUT)
	#model.align_dataset(TEST_FILE_ES,TEST_FILE_EN,TEST_OUT)

	model = IBM_Model_2(TRAINING_FILE_EN,TRAINING_FILE_ES,IBM1_T_FILE_en_es,IBM2_T_FILE_en_es,IBM2_Q_FILE_en_es,True)
	print "f=the e=la", model.t[("the","la")]
	#model.align_dataset(DEV_FILE_EN,DEV_FILE_ES,DEV_OUT)

if __name__ == "__main__":
	main()
