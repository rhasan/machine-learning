#! /usr/bin/python
import json
import subprocess
from collections import defaultdict
from sets import Set

"""
Implementation of probablisitic context free grammer
	CKY algorithm: learning parse tree
"""

INITIAL_TRAINING_FILE = "parse_train.dat"
INITIAL_COUNT_FILE = "cfg.counts"

TRAINING_FILE_WITH_RARE_CLASS = "parse_train_rare.dat"
COUNT_FILE_WITH_RARE_CLASS = "parse_train.counts.out"
RARE = "_RARE_"
RARE_TH = 5


class PCFG:
	
	def __init__(self):
		self.non_terminals = Set()
		self.rules = Set()
		self.binary_rules = Set()
		self.unary_rules = Set()

		self.word_count = defaultdict(lambda: 0)
		self.words = Set()
		self.pi = dict()
		self.bp = dict()
		self.head_tail_non_terminals = dict()


	def clear_all(self):
		self.non_terminals.clear()
		self.rules.clear()
		self.binary_rules.clear()
		self.unary_rules.clear()
		self.word_count.clear()
		self.words.clear()


	def load(self,file_name):
		self.count_file = open(file_name)
		self.counts = defaultdict(lambda: 0)

		for line in self.count_file:
			vals = line.split();
			count_val = int(vals[0])
			if vals[1] == "NONTERMINAL":
				self.counts[vals[2]] = count_val
				self.non_terminals.add(vals[2])
			elif vals[1] == "BINARYRULE":
				self.counts[(vals[2],vals[3],vals[4])] = count_val
				self.rules.add((vals[2],vals[3],vals[4]))
				self.binary_rules.add((vals[2],vals[3],vals[4]))
			elif vals[1] == "UNARYRULE":
				key = (vals[2],vals[3])

				self.counts[key] = count_val
				self.rules.add(key)
				self.unary_rules.add(key)

		for tt in self.unary_rules:
			(term1,term2) = tt
			self.words.add(term2)
			self.word_count.setdefault(term2, 0)
			self.word_count[term2] += self.counts[tt]


		for X in self.non_terminals:
			for nt in self.binary_rules:
				(head,tail1,tail2) = nt
				if head == X:
					self.head_tail_non_terminals.setdefault(head, list())
					self.head_tail_non_terminals[head].append((tail1,tail2))

	def count(self,X,Y1=None,Y2=None):
		if (X!=None and Y1==None and Y2==None):
			return int(self.counts[X])
		elif (X!=None and Y1!=None and Y2!=None):
			return int(self.counts[(X,Y1,Y2)])
		return int(self.counts[(X,Y1)])

	def qml(self,X,Y1=None,Y2=None):
		numerator = 0.0
		denominator = self.count(X)
		if denominator==0:
			return 0.0

		if (X!=None and Y1!=None and Y2!=None):
			numerator = self.count(X,Y1,Y2)
			return float(numerator)/float(denominator)
		
		#for the unary rules, a unary rule always has a word in its tail	
		numerator = self.count(X,Y1)	
		return float(numerator)/float(denominator)
		
		



	def replaceRare(self,old_training_file,new_training_file):
		fo = open(new_training_file, "wb")
		old_file = open(old_training_file)
		for line in old_file:
			try:
				tree = json.loads(line)
				new_tree = self.getNewTree(tree)
				new_line = json.dumps(tree)
				fo.write(new_line+'\n')
			except ValueError:
				print 'ValueError in line:', line
		fo.close()

			
	def getNewTree(self,tree):
		if isinstance(tree, basestring): return

		if len(tree)==2:
			#this is a word because the tree is
			#in Chomsky normal form.
			n_word = self.getReplacedWord(tree[0],tree[1])
			tree[1] = n_word
		elif len(tree)==3:
			self.getNewTree(tree[1])
			self.getNewTree(tree[2])

	def getReplacedWord(self,non_terminal,word):
		if(word not in self.words):
			return RARE
		if self.word_count[word]<RARE_TH:
			return RARE
		else:
			return word
		

	def test(self):
		print self.word_count['.']
		print self.counts[('.','.')]

	def generate_counts(self,training_file, count_file):
		cmd = 'python count_cfg_freq.py '+training_file
		outfile = open(count_file,"w")
		p = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=outfile)
		ret_code = p.wait()
		outfile.flush()
		outfile.close()
		return ret_code		



	def cky_algorithm(self,sentence,start_terminal):
		#print "start cky"
		x = sentence.split()
		n = len(x)
		self.pi.clear()
		self.bp.clear()
		for i in range(1,n+1):
			for X in self.non_terminals:
				key = (i,i,X)
				xi = x[i-1]
				xi_rare = self.getReplacedWord(X,xi)
				rule_key = (X,xi_rare)
				if rule_key in self.rules:
					self.pi[key] = self.qml(X,xi_rare)
					self.bp[key] = xi
				else:
					self.pi[key] = 0.0;

		non_zero_qml_binary_rules = dict()
		
		for X in self.non_terminals:
			if self.head_tail_non_terminals.has_key(X):
				yz_list = self.head_tail_non_terminals[X]
				for (Y,Z) in yz_list:
					qml_val = self.qml(X,Y,Z)
					if qml_val > 0.0:
						non_zero_qml_binary_rules[(X,Y,Z)] = qml_val

		for l in range(1, n):
			for i in range(1, n-l+1):
				j = i + l
				for X in self.non_terminals:
					max_qml = float('-inf')
					max_args = list()
					if self.head_tail_non_terminals.has_key(X):
						yz_list = self.head_tail_non_terminals[X]
						for (Y,Z) in yz_list:
							if non_zero_qml_binary_rules.has_key((X,Y,Z)):
								for s in range(i,j):
									val = non_zero_qml_binary_rules[(X,Y,Z)] * self.pi[(i,s,Y)] * self.pi[(s+1,j,Z)]
									if max_qml < val:
										max_qml = val
										max_args = (Y,Z,s)
					
					if max_qml == float('-inf'): max_qml = 0.0
					self.pi[(i,j,X)] = max_qml
					self.bp[(i,j,X)] = max_args
	
		tree_string = self.generate_tree(1,n,start_terminal)
		return tree_string

	def generate_tree(self,i,j,start_terminal):
		start_json = '["'+start_terminal+'"]'
		tree = json.loads(start_json)
		self.trace_bp(i,j,start_terminal,tree)
		return json.dumps(tree)

	def trace_bp(self,i,j,X,tree):
		bp_val = self.bp[(i,j,X)]
		if isinstance(bp_val, basestring):
			tree.append(bp_val)
			return

		(Y,Z,s) = bp_val

		tree.append([Y])
		self.trace_bp(i,s,Y,tree[1])

		tree.append([Z])
		self.trace_bp(s+1,j,Z,tree[2])


	def cky_test(self):
		self.preprocess()

		out_file = open("parse_dev.out",'w')
		in_file = open("parse_dev.dat")
		#out_file = open("parse_test.p2.out",'w')
		#in_file = open("parse_test.dat")
		
		for line in in_file:
			new_line = self.cky_algorithm(line,"SBARQ")
			out_file.write(new_line+'\n')
		out_file.close()
		in_file.close()
	
	def preprocess(self):
		self.load(INITIAL_COUNT_FILE)
		self.replaceRare(INITIAL_TRAINING_FILE,TRAINING_FILE_WITH_RARE_CLASS)
		self.clear_all()
		code = self.generate_counts(TRAINING_FILE_WITH_RARE_CLASS,COUNT_FILE_WITH_RARE_CLASS)
		self.load(COUNT_FILE_WITH_RARE_CLASS)

	def cky_test_markovization(self):
		self.preprocess_markovization()

		#out_file = open("parse_dev.out",'w')
		#in_file = open("parse_dev.dat")
		out_file = open("parse_test.p3.out",'w')
		in_file = open("parse_test.dat")
		
		for line in in_file:
			new_line = self.cky_algorithm(line,"SBARQ")
			out_file.write(new_line+'\n')
		out_file.close()
		in_file.close()
	
	def preprocess_markovization(self):
		code = self.generate_counts("parse_train_vert.dat","cfg.markov.counts")
		self.load("cfg.markov.counts")
		self.replaceRare("parse_train_vert.dat","parse_train_vert_rare.dat")
		self.clear_all()
		code = self.generate_counts("parse_train_vert_rare.dat","cfg.markov.rare.counts")
		self.load("cfg.markov.rare.counts")


	def get_markovized_parse_tree(self,string,start):
		self.preprocess_markovization()
		return self.cky_algorithm(string,start)

		

#isinstance(obj, basestring):			
def main():
	pcfg = PCFG()
	
	#pcfg.cky_test()
	#print pcfg.cky_algorithm("What was the monetary value of the Nobel Peace Prize in 1989 ?","SBARQ")
	
	pcfg.cky_test_markovization()
	#print pcfg.get_markovized_parse_tree("What was the monetary value of the Nobel Peace Prize in 1989 ?","SBARQ")


if __name__ == "__main__":
	main()
