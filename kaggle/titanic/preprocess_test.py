import csv as csv
import numpy as np

csv_file_object = csv.reader(open('test.csv', 'rb')) #Load in the csv file
header = csv_file_object.next() #Skip the fist line as it is a header


data=[] #Creat a variable called 'data'
for row in csv_file_object: #Skip through each row in the csv file
    data.append(row) #adding each row to the data variable
data = np.array(data) #Then convert from a list to an array

clean_data = np.delete(data,1,1) #remove name
clean_data = np.delete(clean_data,5,1) #remove ticket
clean_data = np.delete(clean_data,6,1) #remove cabin

#pclass(0),sex(1),age(2),sibsp(3),parch(4),fare(5),embarked(6)
clean_data[clean_data[:,1]=='female',1]=0 # 0 for female
clean_data[clean_data[:,1]=='male',1]=1  # 1 for male


clean_data[clean_data[:,6]=='C',6]=0 #0 for C
clean_data[clean_data[:,6]=='Q',6]=1 #1 for Q
clean_data[clean_data[:,6]=='S',6]=2 #2 for S

clean_data[clean_data[:,:]=='',:]=0
#open_file_object = csv.writer(open("clean_data.csv", "wb"))
#All the ages with no data make the median of the data
clean_data[clean_data[:,2]=='',2]=np.median(clean_data[clean_data[0::,2]!= '',2].astype(np.float))

#All missing ebmbarks just make them embark from most common place
clean_data[clean_data[0::,6] == '',6] = np.round(np.mean(clean_data[clean_data[0::,6]!= '',6].astype(np.float)))

#All the missing prices assume median of their respectice class
for i in xrange(np.size(clean_data[0::,0])):
    if clean_data[i,5] == '':
        clean_data[i,5] = np.median(clean_data[(clean_data[0::,5] != '') &\
                                             (clean_data[0::,0] == clean_data[i,0])\
            ,5].astype(np.float))

#clean_data[clean_data[:,5]=='',5]=0
#np.savetxt("clean_data.csv", clean_data, delimiter=",")

clean_data = clean_data.astype(np.float)

np.savetxt("clean_test_data.csv", clean_data, delimiter=",",fmt='%.5f')