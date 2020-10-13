# Testing on my own to see how this could work

from Graph import Graph

graph = Graph()

graph.add("CMPT 120", "CMPT 120")
graph.add("CMPT 106", "CMPT 106")
graph.add("CMPT 125", "CMPT 125")

graph.addEdge("CMPT 120", "CMPT 125", 1)
graph.addEdge("CMPT 120", "CMPT 106", 1)
graph.addEdge("CMPT 106", "CMPT 125", 1)

print(graph.getAllPaths("CMPT 120", "CMPT 125"))