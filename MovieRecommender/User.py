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
