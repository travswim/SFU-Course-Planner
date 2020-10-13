#!/usr/local/bin/python

# Taken from: https://programmingsoup.com/find-all-paths-between-two-nodes

class Vertex:
    """The vertex used in the graph below"""

    def __init__(self, key, data):
        self.adjancencyList = {}
        self.key = key
        self.data = data
        self.currCost = 0  # stores own weight added with followers in path

    def connect(self, otherVertex, weight):
        self.adjancencyList[otherVertex] = weight

    def get_connections(self):
        return self.adjancencyList.keys()

    def get_cost(self, vertex):
        return self.adjancencyList[vertex]
