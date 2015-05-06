import numpy as np
import math

# User contexts {age: 0-25, 25-60, 60+; gender; occupation}
# Item contexts {genre x 19}
class ContextAwareSVD():
    totalUsers = 0
    totalItems = 1682

    userContextsCount = 3
    itemContextsCount = 19

    userRatings  = {}
    userContexts = []
    itemContexts = []

    users = []
    items = []

    numberOfFeatures = -1

    userFeatureMatrix = []
    itemFeatureMatrix = []

    def __init__(self, userRatings, usersDB, itemsDB, numberOfFeatures = 10):
        self.totalUsers  = len(usersDB)

        self.userRatings = userRatings
        self.users = usersDB
        self.items = itemsDB

        self.numberOfFeatures = numberOfFeatures

        self.userFeatureMatrix = np.random.rand(self.totalUsers + self.userContextsCount, self.numberOfFeatures)
        self.itemFeatureMatrix = np.random.rand(self.totalItems + self.itemContextsCount, self.numberOfFeatures)

        self.fillUserContextMatrix()
        self.fillItemContextMatrix()

    def fillUserContextMatrix(self):
        self.userContexts = np.empty([self.totalUsers, 3])
        for user in self.users:
            uid = user['id']
            self.userContexts[uid][0] = user['age']
            self.userContexts[uid][1] = user['gender']
            self.userContexts[uid][2] = user['occupation']

    def fillItemContextMatrix(self):
        self.itemContexts = np.full([19, self.totalItems], 0, dtype=np.int)
        for item in self.items:
            itemID = item['id']
            for genreID in item['genres']:
                self.itemContexts[genreID][itemID] = 1

    def findDecomposition(self):
        i = 1; totalSamples = len(self.userRatings.keys())
        for (userID, itemID) in self.userRatings.keys():
            # print "%d/%d" % (i, totalSamples)
            self.__learnFeatureWithSGD(userID, itemID, self.userRatings[(userID, itemID)])
            i += 1

        it = np.nditer(self.userContexts, flags=['multi_index'])
        while not it.finished:
             # print "%d <%d, %d>" % (it[0], it.multi_index[0], it.multi_index[1]),
             userID = it.multi_index[0]
             itemID = it.multi_index[1]+self.totalItems
             self.__learnFeatureWithSGD(userID, itemID, it.value)
             it.iternext()

        it = np.nditer(self.itemContexts, flags=['multi_index'])
        while not it.finished:
            # print "%d <%d, %d>" % (it[0], it.multi_index[0], it.multi_index[1]),
            userID = it.multi_index[0]
            itemID = it.multi_index[1]
            self.__learnFeatureWithSGD(userID, itemID, it.value)
            it.iternext()


    def __learnFeatureWithSGD(self, userID, itemID, r):
        learningRate = 0.005
        genRate = 0.02

        q = self.userFeatureMatrix[userID, :]
        p = self.itemFeatureMatrix[itemID, :]

        error = r - np.dot(q, p)
        q_new = q + learningRate * (2 * error * p - genRate * q)
        p_new = p + learningRate * (2 * error * q - genRate * p)
        q, p = q_new, p_new

        self.userFeatureMatrix[userID, :] = q
        self.itemFeatureMatrix[itemID, :] = p

    def __classicGD(self):
        learningRate = 0.0002
        genRate = 0.02

        iters = 5000
        for i in xrange(1, iters+1):
            print 'Iter %d out of %d' % (i, iters)
            for (userID, itemID) in self.userRatings.keys():
                q = self.userFeatureMatrix[userID, :]
                p = self.itemFeatureMatrix[itemID, :]

                error = self.userRatings[(userID, itemID)] - np.dot(q, p)
                q_new = q + learningRate * (2 * error * p - genRate * q)
                p_new = p + learningRate * (2 * error * q - genRate * p)
                # q_new = q + 2 * learningRate * error * p
                # p_new = q + 2 * learningRate * error * q
                q, p = q_new, p_new

                self.userFeatureMatrix[userID, :] = q
                self.itemFeatureMatrix[itemID, :] = p

    def computeRMSE(self):
        error = 0
        for (userID, itemID) in self.userRatings.keys():
            predicted = np.dot(self.userFeatureMatrix[userID, :], self.itemFeatureMatrix[itemID, :].T)
            error += math.pow(self.userRatings[(userID, itemID)] - predicted, 2)
        error /= len(self.userRatings.keys())
        return math.sqrt(error)

    def computeMAE(self):
        error = 0
        for (userID, itemID) in self.userRatings.keys():
            predicted = np.dot(self.userFeatureMatrix[userID, :], self.itemFeatureMatrix[itemID, :].T)
            error += abs(self.userRatings[(userID, itemID)] - predicted)
        error /= len(self.userRatings.keys())
        return error
