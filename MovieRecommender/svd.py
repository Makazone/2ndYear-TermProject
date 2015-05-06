import numpy as np
import math

class SVD():
    usersCount = 0
    itemsCount = 0
    userRatings = {}
    numberOfFeatures = -1

    userFeatureMatrix = []
    itemFeatureMatrix = []

    def __init__(self, dataFileSrc, numberOfFeatures, numberOfUsers, numberOfItems):
        self.usersCount = numberOfUsers
        self.itemsCount = numberOfItems

        for entry in open(dataFileSrc):
            entryComponents = [int(x) for x in entry.split()]
            userID = entryComponents[0]-1
            itemID = entryComponents[1]-1
            rating = entryComponents[2]
            self.userRatings[(userID, itemID)] = rating

        self.numberOfFeatures = numberOfFeatures

        # self.userFeatureMatrix = np.random.rand(self.usersCount, self.numberOfFeatures)
        # self.itemFeatureMatrix = np.random.rand(self.itemsCount, self.numberOfFeatures)
        self.itemFeatureMatrix = np.full((self.itemsCount, self.numberOfFeatures), 0.1, dtype=np.float)
        self.userFeatureMatrix = np.full((self.usersCount, self.numberOfFeatures), 0.1, dtype=np.float)

    def findDecomposition(self):
        P = np.array(self.userFeatureMatrix)
        Q = np.array(self.itemFeatureMatrix)

        self.__learnFeatureWithSGD()

        # self.__classicGD()

        # print np.dot(self.userFeatureMatrix, self.itemFeatureMatrix.T)

        # R = [
        #      [5,3,0,1],
        #      [4,0,0,1],
        #      [1,1,0,5],
        #      [1,0,0,4],
        #      [0,1,5,4],
        #     ]
        #
        # R = np.array(R)
        #
        # # N = len(R)
        # # M = len(R[0])
        # K = self.numberOfFeatures
        #
        #
        # nP, nQ = self.matrix_factorization(R, P, Q, K)
        # nR = np.dot(nP, nQ.T)
        # print nR
        #
        # print 'Target RMSE = %f' % self.computeRMSE(nP, nQ)

    def __learnFeatureWithSGD(self):
        learningRate = 0.005
        genRate = 0.02


        np.seterr(all='raise')

        for f in xrange(0, self.numberOfFeatures):
            print 'Training feature #%d' % f
            for i in xrange(0, 10):
                print ' Iteration #%d/10' % i
                for (userID, itemID) in self.userRatings.iterkeys():
                    predicted = np.dot(self.userFeatureMatrix[userID, :], self.itemFeatureMatrix[itemID, :])
                    error = self.userRatings[(userID, itemID)] - predicted
                    self.userFeatureMatrix[userID, f] += learningRate * (2 * error * self.itemFeatureMatrix[itemID, f] - genRate * self.userFeatureMatrix[userID, f])
                    self.itemFeatureMatrix[itemID, f] += learningRate * (2 * error * self.userFeatureMatrix[userID, f] - genRate * self.itemFeatureMatrix[itemID, f])
                    # q_new = q + learningRate * (2 * error * p - genRate * q)
                    # p_new = p + learningRate * (2 * error * q - genRate * p)
                    # q, p = q_new, p_new
                    # print q
                    # print p
                    # self.userFeatureMatrix[f, :] = q
                    # self.itemFeatureMatrix[f, :] = p

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

    def matrix_factorization(self, R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
        Q = Q.T
        for step in xrange(steps):
            for i in xrange(len(R)):
                for j in xrange(len(R[i])):
                    if R[i][j] > 0:
                        eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                        for k in xrange(K):
                            P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                            Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
            eR = np.dot(P,Q)
            e = 0
            for i in xrange(len(R)):
                for j in xrange(len(R[i])):
                    if R[i][j] > 0:
                        e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                        for k in xrange(K):
                            e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
            if e < 0.001:
                break
        return P, Q.T
