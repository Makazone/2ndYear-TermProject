__author__ = 'makazone'

class User():

    def __init__(self, stringData):
        userData = stringData.split('|')

        self.id = int(userData[0]) - 1

        age = int(userData[1])
        if age <= 25: self.ageGroup = 0
        elif age <= 60: self.ageGroup = 1
        else: self.ageGroup = 2
        self.exactAge = age

        self.gender = userData[2]

        self.occupation = userData[3]

    def __str__(self):
        return "{id: %d, age: %d, %c}" % (self.id, self.exactAge, self.gender)

    def getContextDict(self, contextIndexOffset):
        context = {}

        if self.ageGroup == 0:
            context[(self.id, contextIndexOffset+0)] = 5
            context[(self.id, contextIndexOffset+1)] = 0
            context[(self.id, contextIndexOffset+2)] = 0
        elif self.ageGroup == 1:
            context[(self.id, contextIndexOffset+0)] = 0
            context[(self.id, contextIndexOffset+1)] = 5
            context[(self.id, contextIndexOffset+2)] = 0
        else:
            context[(self.id, contextIndexOffset+0)] = 0
            context[(self.id, contextIndexOffset+1)] = 0
            context[(self.id, contextIndexOffset+2)] = 5

        contextIndexOffset += 3

        if self.gender == 'M':
            context[(self.id, contextIndexOffset+0)] = 5
            context[(self.id, contextIndexOffset+1)] = 0
        else:
            context[(self.id, contextIndexOffset+0)] = 0
            context[(self.id, contextIndexOffset+1)] = 5

        return context
