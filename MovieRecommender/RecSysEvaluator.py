import numpy as np
import math

__author__ = 'makazone'

class RecSysEvaluator():
    def __init__(self, userFeatures, itemFeatures, knownRatings):
        self.userFeatures = userFeatures
        self.itemFeatures = itemFeatures
        self.knownRatings = knownRatings

    def __computeRMSE(self, ratings):
        error = 0
        for (userID, itemID) in ratings.keys():
            predicted = np.dot(self.userFeatures[userID, :], self.itemFeatures[itemID, :].T)
            error += math.pow(ratings[(userID, itemID)] - predicted, 2)
        error /= len(ratings.keys())
        return error

    def __computeMAE(self, ratings):
        error = 0
        for (userID, itemID) in ratings.keys():
            predicted = np.dot(self.userFeatures[userID, :], self.itemFeatures[itemID, :].T)
            error += abs(ratings[(userID, itemID)] - predicted)
        error /= len(ratings.keys())
        return error

    def __extractNewRatings(self, testFile):
        newRatings = {}
        for entry in open(testFile):
            entryComponents = [int(x) for x in entry.split()]
            userID = entryComponents[0]-1
            itemID = entryComponents[1]-1
            rating = entryComponents[2]

            "Only new ratings added"
            if not (userID, itemID) in self.knownRatings:
                newRatings[(userID, itemID)] = rating

        print 'Total new ratings = %d' % len(newRatings.keys())
        return newRatings

    def newRatingsRMSE(self, testFile):
        newRatings = self.__extractNewRatings(testFile)
        error = self.__computeRMSE(newRatings)
        print 'RMSE on new ratings = %f' % error

    def newRatingsMAE(self, testFile):
        newRatings = self.__extractNewRatings(testFile)
        error = self.__computeMAE(newRatings)
        print 'MAE on new ratings = %f' % error

    def reconstructionRMSE(self):
        error = self.__computeRMSE(self.knownRatings)
        print 'reconstruction RMSE = %f' % error

    def reconstructionMAE(self):
        error = self.__computeMAE(self.knownRatings)
        print 'reconstruction MAE = %f' % error
