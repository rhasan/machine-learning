from collections import defaultdict
from ibm2 import IBM_Model_2


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


DEV_OUT = "alignment_dev.p3.out"
TEST_OUT = "alignment_test.p3.out"

class Growing_Alignment:
	def __init__(self):
		self.load_f_e()
		self.load_e_f()

	def load_f_e(self):
		self.ibm2_f_e = IBM_Model_2(TRAINING_FILE_ES,TRAINING_FILE_EN,IBM1_T_FILE_es_en,IBM2_T_FILE_es_en,IBM2_Q_FILE_es_en,True)

	def load_e_f(self):
		self.ibm2_e_f = IBM_Model_2(TRAINING_FILE_EN,TRAINING_FILE_ES,IBM1_T_FILE_en_es,IBM2_T_FILE_en_es,IBM2_Q_FILE_en_es,True)
	
	def align_dataset(self,f_file,e_file,out_file):
		unseen_e_file = open(e_file,"r")
		unseen_f_file = open(f_file,"r")
		unseen_out_file = open(out_file,"wb")

		unseen_e = list()
		unseen_f = list()

		unseen_e.append(EMPTY_STRING)
		unseen_f.append(EMPTY_STRING)


		for line in unseen_f_file:
			words = list()
			words.append(NULL_WORD)
			words.extend(line.split())
			unseen_f.append(words)


		for line in unseen_e_file:
			words = list()
			words.append(NULL_WORD)
			words.extend(line.split())
			unseen_e.append(words)

		unseen_count = len(unseen_f)
		
		
		alignment_f_e = defaultdict(lambda: list())
		alignment_e_f = defaultdict(lambda: list())

		for i in range(1,len(unseen_f)):
			f_sen = unseen_f[i]
			e_sen = unseen_e[i]
			
			#argmax p(f|e)
			m = len(f_sen)
			l = len(e_sen)

			f_words = f_sen[1:]
			fi = 1
			for f_word in f_words:
				max_t = float('-inf')
				max_ej = 0
				ej = 0
				for e_word in e_sen:
					val = self.ibm2_f_e.t[(f_word,e_word)] * self.ibm2_f_e.q[(ej,fi,l,m)]
					if max_t < val:
						max_t = val
						max_ej = ej
					ej+=1
				al_tupple = (fi,max_ej)
				alignment_f_e[i].append(al_tupple)

				fi+=1

			#argmax p(e|f)
			m = len(e_sen)
			l = len(f_sen)

			f_words = e_sen[1:]
			fi = 1
			for f_word in f_words:
				max_t = float('-inf')
				max_ej = 0
				ej = 0
				for e_word in f_sen:
					val = self.ibm2_e_f.t[(f_word,e_word)] * self.ibm2_e_f.q[(ej,fi,l,m)]
					if max_t < val:
						max_t = val
						max_ej = ej
					ej+=1
				al_tupple = (fi,max_ej)
				alignment_e_f[i].append(al_tupple)

				fi+=1

		for i in range(1,unseen_count):
			al_e_f_list = alignment_e_f[i]
			al_f_e_list = alignment_f_e[i]
			
			al_matrix_e_f = defaultdict(lambda: 0)

			for (ei,fi) in al_e_f_list:
				al_matrix_e_f[(ei,fi)] += 1
				#print "(",ei,",",fi,") "
			
			for (fi,ei) in al_f_e_list:
				al_matrix_e_f[(ei,fi)] += 1
				#print "(",ei,",",fi,") "

			for (key,val) in al_matrix_e_f.items():
				(ei,fi) = key
				if(val>1):
					new_line = str(i)+" "+str(ei)+" "+str(fi)
					unseen_out_file.write(new_line+'\n')
			#print "\n"

		unseen_out_file.close()
		unseen_e_file.close()
		unseen_f_file.close()
def main():
	al = Growing_Alignment()
	#al.align_dataset(DEV_FILE_ES,DEV_FILE_EN,DEV_OUT)
	al.align_dataset(TEST_FILE_ES,TEST_FILE_EN,TEST_OUT)

if __name__ == "__main__":
	main()
