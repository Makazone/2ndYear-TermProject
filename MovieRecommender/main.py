import svd
import User
import Film
import casvd
import RecSysEvaluator as rseval

userDB = {}
itemDB = {}
occupations = {}

print 'Populating DB'

# Process user occupation data
id = 0
for occupation in open('data/u.occupation'):
    occupations[occupation[0:len(occupation)-1]] = id
    id += 1

# Process user data
for line in open('data/u.user'):
    user = User.User(line)
    userDB[user.id] = user

# Process item data
for line in open('data/u.item'):
    item = Film.Film(line)
    itemDB[item.id] = item

print 'Reading ratings file'

# Number users, ratings and items
dataInfo = [line.split() for line in open("data/u.info")]

# Data set with ratings
dataPath = "data/u1.base"

# Construct dict [(userID, itemID): rating_of_user_to_item]
userRatings = {}
usersUsed = {}
for entry in open(dataPath):
    entryComponents = [int(x) for x in entry.split()]
    userID = entryComponents[0]-1
    itemID = entryComponents[1]-1
    rating = entryComponents[2]

    userRatings[(userID, itemID)] = rating
    usersUsed[userID] = userID

dataSize = [len(usersUsed.keys()), int(dataInfo[1][0])] # [number of users, number of items]

usersList = []
for uid in usersUsed.keys():
    usersList.append(userDB[uid])

# Compute simple SVD using stochastic gradient descend (aka FunkSVD)
svdModel = svd.SVD(15, dataSize[0], dataSize[1], userRatings)
svdModel.findDecomposition()

print 'Evaluating simple SVD'
simpleSVDEvaluator = rseval.RecSysEvaluator(svdModel.userFeatureMatrix, svdModel.itemFeatureMatrix, userRatings)
simpleSVDEvaluator.reconstructionMAE()
simpleSVDEvaluator.newRatingsMAE("data/u1.test")
simpleSVDEvaluator.newRatingsRMSE("data/u1.test")

# Context aware system
# This part incorporates different context info into user-rating matrix
# and computes similar (FunkSVD) decomposition

# itemsList = []
# for iid in itemDB.keys():
#     itemsList.append(itemDB[iid])

# casvdModel = casvd.ContextAwareSVD(15, usersList, itemsList, userRatings)
# casvdModel.findDecomposition()

# print 'Evaluating Context Aware SVD'
# casvdEvaluator = rseval.RecSysEvaluator(casvdModel.userFeatureMatrix, casvdModel.itemFeatureMatrix, userRatings)
# casvdEvaluator.reconstructionMAE()
# casvdEvaluator.newRatingsMAE("data/u1.test")
# casvdEvaluator.newRatingsRMSE("data/u1.test")
#
# print '\n'

