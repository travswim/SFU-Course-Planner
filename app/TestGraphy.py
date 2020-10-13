#!/usr/local/bin/python

# Taken from: https://programmingsoup.com/find-all-paths-between-two-nodes

import unittest
from Graph import Graph


class GraphTest(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

    def tearDown(self):
        self.graph = None

    # Should return all paths sorted by cost
    def test_FindAllPathsSorted(self):

        ## Add vertices
        self.graph.add("A", "A")
        self.graph.add("B", "B")
        self.graph.add("C", "C")
        self.graph.add("D", "D")
        self.graph.add("E", "E")
        self.graph.add("F", "F")

        # Add edges for path 1
        self.graph.addEdge("A", "B", 1)
        self.graph.addEdge("B", "E", 1)
        self.graph.addEdge("E", "F", 0.5)

        # Add edges for path 2
        self.graph.addEdge("B", "F", 2)

        # Add edges for path 3
        self.graph.addEdge("A", "C", 1)
        self.graph.addEdge("C", "F", 3)

        # Add edges for path 4
        self.graph.addEdge("A", "D", 1)
        self.graph.addEdge("D", "F", 4)

        # Get all the paths sorted
        res = self.graph.getAllPathsSorted("A", "F")

        self.assertEqual(res[0]["path"], ['A', 'B', 'E', 'F'])
        self.assertEqual(res[0]["cost"], 2.5)

        self.assertEqual(res[1]["path"], ['A', 'B', 'F'])
        self.assertEqual(res[2]["path"], ['A', 'C', 'F'])
        self.assertEqual(res[3]["path"], ['A', 'D', 'F'])
        # print(res)

if __name__ == '__main__':
    unittest.main()
