import rsa
import random
import numpy as np
from datetime import datetime

class CryptoServer:
    def __init__(self):
        beginTime=datetime.now()
        print("Initializing the Crypto server.")
        print("Crypto - Creating a public and a private key. Start:",beginTime.strftime("%H:%M:%S"))
        (pk,sk) = rsa.newkeys(1000)
        self.pubkey=pk
        self.privkey=sk
        endTime = datetime.now()
        print("Keys created. End:",endTime.strftime("%H:%M:%S"))
        print("Encryption keys generation duration:",endTime-beginTime )

    def getPublicKey(self):
        return self.pubkey
            

    def pearson_correlation(self,meth_matrix: np.array, phenotype: np.array) -> np.array:
        """calculate pearson correlation coefficient between rows of input matrix and phenotype"""
        # calculate mean for each row and phenotype mean
        matrix_means = np.mean(meth_matrix, axis=1)
        phenotype_mean = np.mean(phenotype)

        # subtract means from observed values
        transformed_matrix = meth_matrix - matrix_means.reshape([-1, 1])
        transformed_phenotype = phenotype - phenotype_mean

        # calculate covariance
        covariance = np.sum(transformed_matrix * transformed_phenotype, axis=1)
        variance_meth = np.sqrt(np.sum(transformed_matrix ** 2, axis=1))
        variance_phenotype = np.sqrt(np.sum(transformed_phenotype ** 2))

        return covariance / (variance_meth * variance_phenotype)

    def trainTheModel(self, encr_train_methylation_values, encr_train_ages):
        print("Crypto server - Decrypting the data.")
        #train_methylation_values=rsa.decrypt(encr_train_methylation_values, self.privkey)
        #train_ages = rsa.decrypt(encr_train_ages, self.privkey)
        train_methylation_values=encr_train_methylation_values
        train_ages = encr_train_ages
        abs_pcc_coefficients = abs(self.pearson_correlation(train_methylation_values, train_ages))

        # return list of site indices with a high absolute correlation coefficient
        training_sites = np.where(abs_pcc_coefficients > .85)[0]

        from EpigeneticPacemaker.EpigeneticPacemaker import EpigeneticPacemaker

        # initialize the EPM model
        epm = EpigeneticPacemaker(iter_limit=100, error_tolerance=0.00001)

        # fit the model using the training data
        print("Crypto server - trainning the model.")
        epm.fit(train_methylation_values[training_sites,:], train_ages)
        return epm ,training_sites     #return the trained model

    def predictModel(self,epm, encr_test_methylation_values, training_sites):
        print("Crypto server - obtaining predicted epigenetic ages.")
        # generate predicted ages using the test data
        test_predict = epm.predict(encr_test_methylation_values[training_sites, :])
        return test_predict
 




