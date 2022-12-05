# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    n = int(input('Input: '))
    print("The input was: ", n)
    dic = {}
    for i in range(0, n):
        line = input()
        data = line.split(":")
        dic[data[0]] = int(data[1])
    myString = ""
    subString = ""
    import pandas as pd
    import numpy as np
    import math
    def initateData(inputData):
        f = open(inputData, "r")
        n = int(f.readline())

        visited = set()
        myGraph = {}
        pathValue = np.ones([n, n]) * np.inf
        for x in range(n):
            currentList = f.readline().split(" ")
            myGraph[x] = np.array(currentList, dtype=np.float32)
            for y in range(n):
                if x != y:
                    pathValue[x, y] = currentList[y]
        return pathValue

    def firstMin(pathValue):
        print("Original matrix: \n{}".format(pathValue))
        subtract1 = [min(pathValue[i, :]) for i in range(n)]
        # print(subtract1)
        pathValue1 = np.array(pathValue) - np.array(subtract1).reshape(-1, 1)
        # print(pathValue1)
        subtract2 = [min(pathValue1[:, i]) for i in range(n)]
        # print(subtract2)
        pathValue2 = np.array(pathValue1) - np.array(subtract2).reshape(-1, 1).T
        # print("Original matrix after original clean: \n{}".format(pathValue2))
        print("Subtract1: {}, Subtract2: {}, cost: {}".format(subtract1, subtract2, sum(subtract1 + subtract2)))
        return pathValue2, sum(subtract1 + subtract2)

    def secondPlusMin(pathValue, inNode, outNode, g):
        print("Tracking matrix update from {} -> {}".format(inNode, outNode))
        pathValue1 = np.copy(pathValue)
        print("Input matrix: \n{}".format(pathValue1))
        pathValue1[inNode, :] = np.inf
        # print("Input matrix Update Rows: {}".format(pathValue1))
        pathValue1[:, outNode] = np.inf
        # print("Input matrix Update Cols: {}".format(pathValue1))
        pathValue1[outNode, inNode] = np.inf
        # print("Matrix for current level: {}".format(pathValue1))
        subtract1 = np.array([min(pathValue1[:, i]) for i in range(n)])
        subtract1[subtract1 == np.inf] = 0
        # print(subtract1)
        pathValue2 = np.array(pathValue1) - subtract1.reshape(-1, 1).T
        # print("Matrix after row update: \n{}".format(pathValue2))
        subtract2 = np.array([min(pathValue2[i, :]) for i in range(n)])
        subtract2[subtract2 == np.inf] = 0

        pathValue2 = np.array(pathValue2) - subtract2.reshape(-1, 1)
        # print("Matrix after col update: \n{}".format(pathValue2))

        print("Subtract1: {}, Subtract2: {}, cost: {}".format(subtract1, subtract2,
                                                              sum(subtract1 + subtract2) + g + pathValue[inNode][
                                                                  outNode]))
        return pathValue2, sum(subtract1 + subtract2) + g + pathValue[inNode][outNode]

    def BnB(pathMatrix, startNode):
        pathMatrixNew, cost = firstMin(np.copy(pathValue))
        visited = set()

        def dfs(pathMatrix, currentNode, cost, upperBound, path):
            visited.add(currentNode)
            if len(visited) == n:
                return cost, " -> {}".format(currentNode)
            myMatrices = []
            for i in range(n):
                if i not in visited:
                    # print("Original matrix prior to function: {}".format(pathMatrix))
                    pathMatrixNew, costNew = secondPlusMin(np.copy(pathMatrix), currentNode, i, cost)
                    myMatrices.append((pathMatrixNew, costNew, i))
            sortedList = sorted(myMatrices, key=lambda x: x[1])
            # print(sortedList)
            for pathMatrixNew, cost, node in sortedList:
                if cost < upperBound:
                    print("{} -> {}".format(currentNode, node))
                    result, path = dfs(np.copy(pathMatrixNew), node, cost, upperBound, path)
                    visited.remove(node)
                    print("{} <- {}".format(currentNode, node))
                    if result < upperBound:
                        upperBound = result
                        if len(visited) == 1:
                            path = "{}".format(currentNode) + path
                        else:
                            path = " -> {}".format(currentNode) + path
                else:
                    print("{} -> {} was pruned with an estimated cost of {}".format(currentNode, node, cost))

            return upperBound, path

        cost, path = dfs(np.copy(pathMatrixNew), startNode, cost, np.inf, "")
        print("Final cost is {} and the path was {}".format(cost, path + " -> {}".format(startNode)))

    def main():
        source = input("Enter your source location (5_0.0_10.0.out): ")
        dataSource = initateData(source)
        while True:
            val = input("Enter your starting city (Cities available are from 0-{}), Enter q to quit: ".format(n - 1))
            if val == "q":
                return
            BnB(dataSource, int(val))

    if __name__ == '__main__':
        main()
