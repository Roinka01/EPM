from DataOwner import DataOwner
from CryptoServer import CryptoServer

import numpy as np

# A MLE object will hold the Data Owners
class MLEngion:
    def __init__(self, noOfDataOwners):
       print("Initializing the MLE server.")
       self.crpt=CryptoServer()
       self.DOArray=[]
       self.appendedMethylationVals = []
       self.appendedAges = []
       self.appendedSites = []
       self.appendedsamples = []
       i=0
       #Following loop creates the list (array) of Data Owners
       while (i<noOfDataOwners):
           print("Initializing Data Owner: ", i+1)
           self.DOArray.append(DataOwner(i + 1, noOfDataOwners, self.crpt))
           i+=1
       self.noOfDataOwners=noOfDataOwners

    # Following method appends all Data Owners (train) data into one appended data list
    # (for every data set part)
    def appendData(self):
        print("Merge encrypted data from all Data Owners.")
        i = 0
        while (i < self.noOfDataOwners):
            self.appendedMethylationVals.append(self.DOArray[i].getEncryptedTrainedMethylationVals())
            self.appendedAges.append(self.DOArray[i].getEncryptedTrainedAges())
            self.appendedSites.append(self.DOArray[i].getEncryptedTrainedSites())
            self.appendedsamples.append(self.DOArray[i].getEncryptedTrainedSamples())
            print("Append data from Data Owner:",i+1)
            i+=1
        # self.appendedsamples, self.appendedSites, self.appendedAges, self.appendedMethylationVals=self.DOArray[0].getEncryptedTrainData()
        # self.appendedMethylationVals = self.DOArray[0].getEncryptedTrainedMethylationVals()
        # self.appendedAges = self.DOArray[0].getEncryptedTrainedAges()
        self.appendedsamples, self.appendedSites, self.appendedAges, self.appendedMethylationVals = self.DOArray[0].getTrainData()

    def getTrainData(self):
        self.appendedSamples, self.appendedSites, self.appendedAges, self.appendedMethylationVals = self.DOArray[0].getEncryptedTrainData()
        return self.appendedSamples, self.appendedSites, self.appendedAges, self.appendedMethylationVals

    def maskData(self):
        return
    # Train the model, using the combined data from all Data Owners
    def modelTraining(self):
        self.maskData()
        print("Train the model.")
        return self.crpt.trainTheModel(self.appendedMethylationVals, self.appendedAges)

    def predictTest(self,epm ,training_sites):
        test_samples, test_cpg_sites, test_ages, test_methylation_values = self.DOArray[0].getTestData()
        return self.crpt.predictModel(epm, test_methylation_values, training_sites)

#Main Algorithem
# Create the following entities:
# 1. a MLE server
# 2. a Crypto Server (contained inside the MLE)
# 3. Data Owners that will return their encrypted data to the MLE
mle=MLEngion(4)
#Append data from all Data Owners
mle.appendData()
#MLE will invoke the algorythem using the Crypto server and return the trained model
epm ,training_sites=mle.modelTraining()
# epm,decr_training_sites = crpt.trainTheModel(self, encr_train_methylation_values, encr_train_ages)
#get predicted results using the trained model
test_predict=mle.predictTest(epm ,training_sites)
print("The predicted Methylation values are: " ,test_predict)
