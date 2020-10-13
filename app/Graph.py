#!/usr/local/bin/python

# Taken from: https://programmingsoup.com/find-all-paths-between-two-nodes

from Vertex import Vertex

"""
This class is a weighted directed graph that is
supposed to be able to find all paths between two nodes

* The graph sorts all the paths by weight
* The graphs vertices uses keys to allow duplicates of data
* The graphs depth first search is based on recursion
"""


class Graph(object):
    """graph used to find all paths between two nodes using DFS"""

    def __init__(self):
        self.numberOfVertices = 0
        self.vertices = {}


    def add(self, key, data):
        """adds a vertex to graph and saves vertex based on unique key"""
        if key not in self.vertices:
            self.numberOfVertices += 1
            self.vertices[key] = Vertex(key, data)
            return True

        return False


    def addEdge(self, fromVertex, toVertex, weight):
        """connects two vertices"""
        if fromVertex in self.vertices and toVertex in self.vertices:
            self.vertices[fromVertex].connect(toVertex, weight)
            return True

        return False


    def getAllPaths(self, start, end):
        return self.dfs(start, end, [], [], [])


    def getAllPathsSorted(self, start, end):
        res = self.dfs(start, end, [], [], [])
        return sorted(res, key=lambda k: k['cost'])


    def dfs(self, currVertex, destVertex, visited, path, fullPath):
        """finds all paths between two nodes, returns all paths with their respective cost"""

        # get vertex, it is now visited and should be added to path
        vertex = self.vertices[currVertex]
        visited.append(currVertex)
        path.append(vertex.data)

        # save current path if we found end
        if currVertex == destVertex:
            fullPath.append({"path": list(path), "cost": vertex.currCost})

        for i in vertex.get_connections():
            if i not in visited:
                self.vertices[i].currCost = vertex.get_cost(i) + vertex.currCost
                self.dfs(i, destVertex, visited, path, fullPath)

        # continue finding paths by popping path and visited to get accurate paths
        path.pop()
        visited.pop()

        if not path:
            return fullPath
