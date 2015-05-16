import numpy as np
import math

class SVD():
    usersCount = 0
    itemsCount = 0
    userRatings = {}
    numberOfFeatures = -1

    userFeatureMatrix = []
    itemFeatureMatrix = []

    def __init__(self, numberOfFeatures, numberOfUsers, numberOfItems, ratings):
        self.usersCount = numberOfUsers
        self.itemsCount = numberOfItems

        self.userRatings = ratings
        self.numberOfFeatures = numberOfFeatures

        # self.userFeatureMatrix = np.random.rand(self.usersCount, self.numberOfFeatures)
        # self.itemFeatureMatrix = np.random.rand(self.itemsCount, self.numberOfFeatures)
        self.itemFeatureMatrix = np.full((self.itemsCount, self.numberOfFeatures), 0.1, dtype=np.float)
        self.userFeatureMatrix = np.full((self.usersCount, self.numberOfFeatures), 0.1, dtype=np.float)

    def findDecomposition(self):
        self.__learnFeatureWithSGD()

    def __learnFeatureWithSGD(self):
        learningRate = 0.005
        genRate = 0.02

        "Forces numpy to raise exceptions on warnings"
        np.seterr(all='raise')

        "Learn each feature separately"
        for f in xrange(0, self.numberOfFeatures):
            print 'Training feature #%d' % f

            "Number of iterations until convergence"
            for i in xrange(0, 10):
                print ' Iteration #%d/10' % i

                "For each known rating"
                for (userID, itemID) in self.userRatings.iterkeys():
                    predicted = np.dot(self.userFeatureMatrix[userID, :], self.itemFeatureMatrix[itemID, :])
                    error = self.userRatings[(userID, itemID)] - predicted

                    "Update rules"
                    self.userFeatureMatrix[userID, f] += learningRate * (2 * error * self.itemFeatureMatrix[itemID, f] - genRate * self.userFeatureMatrix[userID, f])
                    self.itemFeatureMatrix[itemID, f] += learningRate * (2 * error * self.userFeatureMatrix[userID, f] - genRate * self.itemFeatureMatrix[itemID, f])


    def computeRMSE(self, userFeatures, itemFeatures):
        error = 0
        for (userID, itemID) in self.userRatings.keys():
            predicted = np.dot(userFeatures[userID, :], itemFeatures[itemID, :].T)
            error += math.pow(self.userRatings[(userID, itemID)] - predicted, 2)
        error /= len(self.userRatings.keys())
        return math.sqrt(error)

    def computeMAE(self, userFeatures, itemFeatures):
        error = 0
        for (userID, itemID) in self.userRatings.keys():
            predicted = np.dot(userFeatures[userID, :], itemFeatures[itemID, :].T)
            error += abs(self.userRatings[(userID, itemID)] - predicted)
        error /= len(self.userRatings.keys())
        return error
