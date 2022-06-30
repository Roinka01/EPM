# import the data retrieval class
import sys
import rsa
import math


from EpigeneticPacemaker.ExampleData.DataSets import get_example_data

class DataOwner:
     def __init__(self, DO_id, tot_num_of_do,_crypto):
         if (DO_id>tot_num_of_do):
             print("Wrong DW id.")
             exit()
         if (tot_num_of_do>4):
             print("not enough data for the simulation.")
             exit()         
         # retrieve the training and testing data
         self.test_data, self.train_data = get_example_data()
         # unpack the training data
         train_samples, train_cpg_sites, train_ages, train_methylation_values = self.train_data
         
         # In order to simulate several Data owners, the data is divided among all Data Owners
         # get this DW array size
         self.trainDataArraySize = math.floor(len(train_samples)/tot_num_of_do)
         #in case few cells are missing, increase array size accordingly for the last DO
         diff=0
         if (DO_id==tot_num_of_do and self.trainDataArraySize*tot_num_of_do<len(train_samples)):
             diff=(len(train_samples)-self.trainDataArraySize)
             self.trainDataArraySize+=diff
         ind=(DO_id-1)*self.trainDataArraySize
         lastInd=DO_id*self.trainDataArraySize-1
         self.train_samples=train_samples[ind:lastInd]
         self.train_cpg_sites = train_cpg_sites[ind:lastInd]
         self.train_ages = train_ages[ind:lastInd]
         self.train_methylation_values = train_methylation_values[ind:lastInd]
         print("initializing the data of Data Owner:",DO_id)
         #Keep a reference to the Crypto server for internal communicatio in between
         # so data encryption is feasible.
         self.crypto=_crypto
         self.train_samples = train_samples
         self.train_cpg_sites = train_cpg_sites
         self.train_ages = train_ages
         self.train_methylation_values = train_methylation_values
         
     def getTrainData(self):
         return self.train_data
     def getEncryptedTrainedMethylationVals(self):
         print("Obtain encrypted data.")
         return self.train_methylation_values
         #return rsa.encrypt(self.train_methylation_values,self.crypto.getPublicKey())
         
     def getEncryptedTrainedAges(self):
         #return rsa.encrypt(self.train_ages, self.crypto.getPublicKey())
         return self.train_ages
     
     def getEncryptedTrainedSites(self):
         #return rsa.encrypt(self.train_cpg_sites, self.crypto.getPublicKey())
         return self.train_cpg_sites
     
     def getEncryptedTrainedSamples(self):
         #return rsa.encrypt(self.train_samples, self.crypto.getPublicKey())
         return self.train_samples
     
     def getEncryptedTrainData(self):
         #return rsa.encrypt(self._train_data,self.crypto.getPublicKey())
         return self.train_data
     def getTestData(self):
         return self.test_data
    



