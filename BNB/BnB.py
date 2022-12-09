import pandas as pd
import numpy as np
import math
import time

global nne
nne = 0

global growthRate
growthRate = 0

global level
level = 0


def initateData(inputData):
    f = open(inputData, "r")
    n = int(f.readline())

    visited = set()
    myGraph = {}
    pathValue = np.ones([n,n])* np.inf
    for x in range(n):
        currentList = f.readline().split(" ")
        myGraph[x] = np.array(currentList, dtype = np.float32)
        for y in range(n):
            if x != y:
                pathValue[x,y] = currentList[y]
    return pathValue, n

def firstMin(pathValue, n):
    #print("Original matrix: \n{}".format(pathValue))
    subtract1 = [min(pathValue[i,:]) for i in range(n)]
    #print(subtract1)
    pathValue1 = np.array(pathValue) - np.array(subtract1).reshape(-1,1)
    #print(pathValue1)
    subtract2 = [min(pathValue1[:,i]) for i in range(n)]
    #print(subtract2)
    pathValue2 = np.array(pathValue1) - np.array(subtract2).reshape(-1,1).T
    #print("Original matrix after original clean: \n{}".format(pathValue2))
    #print("Subtract1: {}, Subtract2: {}, cost: {}".format(subtract1, subtract2, sum(subtract1 + subtract2)))
    return pathValue2, sum(subtract1 + subtract2)

def secondPlusMin(pathValue, inNode, outNode, g, n):
    #print("Tracking matrix update from {} -> {}".format(inNode, outNode))
    pathValue1 = np.copy(pathValue)
    #print("Input matrix: \n{}".format(pathValue1))
    pathValue1[inNode,:] = np.inf
    #print("Input matrix Update Rows: {}".format(pathValue1))
    pathValue1[:,outNode] = np.inf
    #print("Input matrix Update Cols: {}".format(pathValue1))
    pathValue1[outNode,inNode] = np.inf
    #print("Matrix for current level: {}".format(pathValue1))
    subtract1 = np.array([min(pathValue1[:,i]) for i in range(n)])
    subtract1[subtract1 == np.inf] = 0
    #print(subtract1)
    pathValue2 = np.array(pathValue1) - subtract1.reshape(-1,1).T
    #print("Matrix after row update: \n{}".format(pathValue2))
    subtract2 = np.array([min(pathValue2[i,:]) for i in range(n)])
    subtract2[subtract2 == np.inf] = 0

    pathValue2 = np.array(pathValue2) - subtract2.reshape(-1,1)
    #print("Matrix after col update: \n{}".format(pathValue2))

    #print("Subtract1: {}, Subtract2: {}, cost: {}".format(subtract1, subtract2, sum(subtract1 + subtract2)+ g +pathValue[inNode][outNode]))
    return pathValue2, sum(subtract1 + subtract2) + g + pathValue[inNode][outNode]


def BnB(pathMatrix, startNode, n):
    # get the start time
    st = time.time()
    pathMatrixNew, startCost = firstMin(np.copy(pathMatrix), n)
    global nne
    nne = 1
    global level
    level = 0
    levelValue = [np.inf for i in range(n)]
    def dfs(pathMatrix, currentNode, cost, upperBound, path):
        global level
        global nne
        level += 1
        localOrder = sorted(zip(range(n), np.copy(pathMatrix[currentNode,:])), key = lambda x: x[1])
        if level == n-1:
            level -= 1
            return cost, " -> {}".format(currentNode)
        myMatrices = []
        for k in range(max(math.floor(math.sqrt(n)/5), 1)):
            for i,_ in localOrder[k:k+min(5,n)]:
                #print("Original matrix prior to function: {}".format(pathMatrix))
                pathMatrixNew, costNew = secondPlusMin(np.copy(pathMatrix), currentNode, i, cost, n)
                myMatrices.append((pathMatrixNew, costNew, i))
            sortedList = sorted(myMatrices, key = lambda x: x[1])
            localMin = sortedList[0][1]
            #print("Local min: {}, past level min: {}".format(localMin,levelValue[level-1]))
            if localMin <= (levelValue[min([level+1,n-1])] + levelValue[min([level+2,n-1])])/2:
                levelValue[level] = min([localMin, levelValue[level]])
                for pathMatrixNew, cost, node in sortedList:
                    #print("upperBound: {}, f: {}".format(upperBound, cost))
                    if cost < upperBound and time.time()-st < 600:
                        #print("{} -> {}".format(currentNode, node))
                        nne +=1

                        result, path = dfs(np.copy(pathMatrixNew), node, cost, upperBound, path)
                        #print("{} <- {}".format(currentNode, node))
                        if result < upperBound:
                            upperBound = result
                            if level == n-2:
                                path = "{}".format(currentNode) + path
                            else:
                                path = " -> {}".format(currentNode) + path
                    else:
                        break
                        #print("{} -> {} was pruned with an estimated cost of {}".format(currentNode, node, cost))
            else:
                break
        level -= 1
        return upperBound, path
    cost, path = dfs(np.copy(pathMatrixNew), startNode, startCost, np.inf, "")
    et = time.time()
    return cost, nne, path, et-st

def main():
    source = input("Enter your source location: ")
    dataSource, n = initateData(source)
    costs = []
    nodesExp = []
    timeSpend = []
    
    version = input("Automate problem estimates? y/n: ")
    
    if version == "y":
        for i in range(min([n, 10])):
            cost, nodes, path, time = BnB(dataSource,i, n)
            costs.append(cost)
            nodesExp.append(nodes)
            timeSpend.append(time)

        print("Statistics: ")
        print()
        print("Mean Cost: {}".format(np.mean(costs)))
        print("Min Cost: {}".format(np.min(costs)))
        print("STD Cost: {}".format(np.std(costs)))
        print()
        print("Mean Nodes Expanded: {}".format(np.mean(nodesExp)))
        print("STD Nodes Expanded: {}".format(np.std(nodesExp)))
        print()
        print("Mean Time Spend: {}".format(np.mean(timeSpend)))
        print("STD Time Spend: {}".format(np.std(timeSpend)))
    else:
        while True:
            val = input("Enter your starting city (Cities available are from 0-{}), Enter q to quit: ".format(n-1))
            if val == "q":
                return
            cost, nodes, path, time = BnB(dataSource,int(val), n)
            print("Current run took {} seconds".format(time))
            print("Expanded {} nodes".format(nne))
            
            print("Final cost is {} and the path was {}".format(cost, path + " -> {}".format(int(val))))
if __name__ == '__main__':
    main()
