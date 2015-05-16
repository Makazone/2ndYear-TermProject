import svd
import User
import Film
import casvd
import RecSysEvaluator as rseval

userDB = {}
itemDB = {}
occupations = {}

print 'Populating DB'

id = 0
for occupation in open('data/u.occupation'):
    occupations[occupation[0:len(occupation)-1]] = id
    id += 1

for line in open('data/u.user'):
    user = User.User(line)
    userDB[user.id] = user

for line in open('data/u.item'):
    item = Film.Film(line)
    itemDB[item.id] = item

# print userDB[0]
# print itemDB[0]

print 'Reading ratings file'

dataInfo = [line.split() for line in open("data/u.info")]
dataPath = "data/u1.base"

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

# # casvdModel = casvd.ContextAwareSVD(userRatings, usersList, itemList, numberOfFeatures=15)
# # casvdModel.findDecomposition()
# # print "Context-aware RMSE = %f" % casvdModel.computeRMSE()
# # print "Context-aware MAE = %f" % casvdModel.computeMAE()

svdModel = svd.SVD(15, dataSize[0], dataSize[1], userRatings)
svdModel.findDecomposition()

# # # print np.dot(svdModel.userFeatureMatrix, svdModel.itemFeatureMatrix.T)

evaluator = rseval.RecSysEvaluator(svdModel.userFeatureMatrix, svdModel.itemFeatureMatrix, userRatings)
evaluator.reconstructionMAE()
evaluator.newRatingsMAE("data/u1.test")
