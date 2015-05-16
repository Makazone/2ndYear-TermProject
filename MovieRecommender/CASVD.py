import numpy as np
import math
import svd

class ContextAwareSVD():
    totalUsers = 0
    totalItems = 1682

    userContextsCount = 5
    itemContextsCount = 19

    userRatings  = {}
    userContexts = []
    itemContexts = []

    users = []
    items = []

    numberOfFeatures = -1

    userFeatureMatrix = []
    itemFeatureMatrix = []

    def __init__(self, numberOfFeatures, usersDB, itemsDB, ratings):
        self.totalUsers  = len(usersDB)

        self.userRatings = dict(ratings)
        self.users = usersDB
        self.items = itemsDB

        self.numberOfFeatures = numberOfFeatures

        self.userFeatureMatrix = np.random.rand(self.totalUsers + self.itemContextsCount, self.numberOfFeatures)
        self.itemFeatureMatrix = np.random.rand(self.totalItems + self.userContextsCount, self.numberOfFeatures)

        self.addUserContext()
        self.addItemContext()

    def addUserContext(self):
        self.userContexts = np.empty([self.totalUsers, 3])
        for user in self.users:
            self.userRatings.update(user.getContextDict(self.totalItems))

    def addItemContext(self):
        self.itemContexts = np.full([19, self.totalItems], 0, dtype=np.int)
        for item in self.items:
            self.userRatings.update(item.getContextDict(self.totalUsers))

    def findDecomposition(self):
        svdSolver = svd.SVD(self.numberOfFeatures,
                            self.totalUsers+self.itemContextsCount,
                            self.totalItems+self.userContextsCount,
                            self.userRatings)

        svdSolver.findDecomposition()

        self.userFeatureMatrix = svdSolver.userFeatureMatrix[:-self.itemContextsCount]
        self.itemFeatureMatrix = svdSolver.itemFeatureMatrix[:-self.userContextsCount]
