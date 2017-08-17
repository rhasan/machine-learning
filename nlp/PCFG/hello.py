import json
from collections import defaultdict


def traverse(tree):
	if(len(tree)==2):
		#this is a word because the tree is
		#in Chomsky normal form.
		print tree[1]
		tree[1] = "word"
	elif(len(tree)==3):
		traverse(tree[1])
		traverse(tree[2])


old_training_file = "pa2\\tree.example.fmt"

old_file = open(old_training_file)

#for line in old_file:

#	print line
#	tree = json.loads(old_file.readline())
line = old_file.readline()
print line
tree = json.loads(line)
#print tree[2][1][1][1]
#print "node:", tree[2]
print "len:", len(tree)
traverse(tree)

print json.dumps(tree)