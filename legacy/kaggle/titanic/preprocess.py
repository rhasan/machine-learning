import csv as csv
import numpy as np

csv_file_object = csv.reader(open('train.csv', 'rb')) #Load in the csv file
header = csv_file_object.next() #Skip the fist line as it is a header


data=[] #Creat a variable called 'data'
for row in csv_file_object: #Skip through each row in the csv file
    data.append(row) #adding each row to the data variable
data = np.array(data) #Then convert from a list to an array

clean_data = np.delete(data,2,1) #remove name
clean_data = np.delete(clean_data,6,1) #remove ticket
clean_data = np.delete(clean_data,7,1) #remove cabin

#survived(0),pclass(1),sex(2),age(3),sibsp(4),parch(5),fare(6),embarked(7)
clean_data[clean_data[:,2]=='female',2]=0 # 0 for female
clean_data[clean_data[:,2]=='male',2]=1  # 1 for male


clean_data[clean_data[:,7]=='C',7]=0 #0 for C
clean_data[clean_data[:,7]=='Q',7]=1 #1 for Q
clean_data[clean_data[:,7]=='S',7]=2 #2 for S

#clean_data[clean_data[:,:]=='',:]=0
#All the ages with no data make the median of the data
clean_data[clean_data[:,3]=='',3]=np.median(clean_data[clean_data[0::,3]!= '',3].astype(np.float))

#All missing ebmbarks just make them embark from most common place
clean_data[clean_data[0::,7] == '',7] = np.round(np.mean(clean_data[clean_data[0::,7]!= '',7].astype(np.float)))
#open_file_object = csv.writer(open("clean_data.csv", "wb"))

#np.savetxt("clean_data.csv", clean_data, delimiter=",")

clean_data = clean_data.astype(np.float)

np.savetxt("clean_data.csv", clean_data, delimiter=",",fmt='%.5f')