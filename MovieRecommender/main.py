import numpy as np
import scipy as sc
from sklearn.decomposition import NMF
from time import time
import pymf
import svd
import casvd

userDB = {}
itemDB = {}
occupations = {}

print 'Populating DB'

id = 0
for occupation in open('data/u.occupation'):
    occupations[occupation[0:len(occupation)-1]] = id
    id += 1

for line in open('data/u.user'):
    userData = line.split('|')
    userID   = int(userData[0])-1

    age = int(userData[1]); ageGroup = -1
    if age <= 25: ageGroup = 0
    elif age <= 60: ageGroup = 1
    else: ageGroup = 2

    gender = -1
    if userData[2] == 'M':
        gender = 1
    else: gender = 0

    userDB[userID] = {'id':userID, 'age':ageGroup, 'gender':gender, 'occupation':occupations[userData[3]]}

for line in open('data/u.item'):
    itemData = line.split('|')
    itemID   = int(itemData[0])-1

    itemDB[itemID] = {'id':itemID, 'genres':[]}
    for genreID in xrange(0, 19):
        if itemData[5+genreID] == '1':
            itemDB[itemID]['genres'].append(genreID)

# print userDB
# print itemDB

print 'Reading data file'

dataInfo = [line.split() for line in open("data/u.info")]
dataPath = "data/u.data"

userRatings = {}
users = {}; items = {}
for entry in open(dataPath):
    entryComponents = [int(x) for x in entry.split()]
    userID = entryComponents[0]-1
    itemID = entryComponents[1]-1
    rating = entryComponents[2]
    userRatings[(userID, itemID)] = rating

    users[userID] = userDB[userID]
    items[itemID] = itemDB[itemID]

# dataSize = [user, int(dataInfo[1][0])] # [number of users, number of items]
usersList = []
for key, value in users.iteritems():
    usersList.append(value)

itemList = []
for key, value in items.iteritems():
    itemList.append(value)

# casvdModel = casvd.ContextAwareSVD(userRatings, usersList, itemList, numberOfFeatures=15)
# casvdModel.findDecomposition()
# print "Context-aware RMSE = %f" % casvdModel.computeRMSE()
# print "Context-aware MAE = %f" % casvdModel.computeMAE()

svdModel = svd.SVD(dataPath, 15, len(usersList), 1682)
svdModel.findDecomposition()

# # print np.dot(svdModel.userFeatureMatrix, svdModel.itemFeatureMatrix.T)
print "Simple RMSE = %f" % svdModel.computeRMSE(svdModel.userFeatureMatrix, svdModel.itemFeatureMatrix)
print "Simple MAE = %f" % svdModel.computeMAE(svdModel.userFeatureMatrix, svdModel.itemFeatureMatrix)

