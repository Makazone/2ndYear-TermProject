__author__ = 'makazone'

class Film():

    def __init__(self, stringData):
        filmData = stringData.split('|')

        self.id      = int(filmData[0]) - 1
        self.title   = filmData[1]
        self.imdbURL = filmData[4]

        self.genre = [0 for x in xrange(0, 19)]
        for genreID in xrange(0, 19):
            if filmData[5+genreID] == '1':
                self.genre[genreID] = 5

    def __str__(self):
        return "{id: %d, title: %s}" % (self.id, self.title)

    def getContextDict(self, contextIndexOffset):
        context = {}

        for i in xrange(0, 19):
            if self.genre[i] == 5:
                context[(contextIndexOffset+i, self.id)] = 5
            else:
                context[(contextIndexOffset+i, self.id)] = 0

        return context
