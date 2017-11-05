# Author - Subhajit Das
# Decision tree using ID3 algorithim 



import math

# Structure for each node with some added functions


class Node:
    def __init__(self, attri=None, connect=None):
        self.attri = attri
        self.connect = connect
        self.root = None
        self.child = []

    def printChild(self):
        for i in self.child:
            print("Attri - {0}\t Connection - {1}".format(i.attri, i.connect))

    def addRoot(self, node=None):
        self.root = node

    def addChild(self, node=None):
        self.child.append(node)

    def setAttri(self, attri=None):
        self.attri = attri

    def hasChild(self, attri):
        for i in self.child:
            if i.attri == attri:
                return True
        return False

    def getChildByAttri(self, attri):
        for i in self.child:
            if i.attri == attri:
                return i
        return None

    def getChildByConnect(self, connect):
        for i in self.child:
            if i.connect == connect:
                return i
        return None

# changing the whole file read list to column list


def convertToColList(valN, valD):
    val2 = []
    for j in range(len(valN)):
        temp = []
        for i in range(len(valD)):
            temp.append(valD[i][j])
        val2.append(temp)
    return val2

# used to get individual values of each attribute


def returnIndiVal(valD):
    temp = []
    for i in valD:
        if(i not in temp):
            temp.append(i)
    return temp

# get the sum for class P and N


def getPN(classIndiVal, classData):
    countFreq = []
    for i in classIndiVal:
        countFreq.append(classData.count(i))
    return countFreq

# get the class entropy for a dataset


def getOutputClassEntropy(resultList, indiVal):
    freqAttri = []
    for j in indiVal:
        freqAttri.append(resultList.count(j))
    resEn = 0
    for i in freqAttri:
        temp = i / (sum(freqAttri))
        if(temp == 0):
            resEn = 0
            break
        resEn += -temp * (math.log2(temp))
    return resEn

# get the individual attribute entropy for a dataset


def getAttriClassEntropy(attriDataList, resultList, attriIndiVal, classIndiVal, attriName):

    print("CALCULATION FOR\t{0}\n".format(attriName))

    # finding out index for yes or no (accodring to dataset)
    indexList = []
    for i in attriIndiVal:
        temp = []
        for j in range(len(attriDataList)):
            if attriDataList[j] == i:
                temp.append(j)

        indexList.append(temp)
        # for debugging purpose
        print(
            "\t\tIndex for attribute {0} -\t{1}".format(i, indexList[-1]))

    # finding the Pi and Ni values for attribute
    attriPNList = []
    for singAttriIndexList in indexList:
        singlDataList = []
        for option in classIndiVal:
            count = 0
            for index in singAttriIndexList:
                if resultList[index] == option:
                    count += 1
            singlDataList.append(count)
        attriPNList.append(singlDataList)

    # for debugging purpose
    print("\n\t\tP(i) & N(i) values")
    print("\t\t{0}  -  {1}".format(attriIndiVal, classIndiVal))
    print("\t\t", attriPNList)

    # finding I(Pi,Ni) for each attribute
    interAttriEntropy = []
    for singleAttriPNList in attriPNList:
        result = 0
        for i in singleAttriPNList:
            if i == 0:
                result = 0
                break
            else:
                tempDig = i / (sum(singleAttriPNList))
                result += -tempDig * (math.log2(tempDig))
                result = round(result, 3)

        interAttriEntropy.append(result)

    # for debugging purpose
    print("\n\t\tEach part result\n\t\t{0}".format(interAttriEntropy))

    # calculating the final attribute class entropy
    resultEntropy = 0
    pnSum = sum(getPN(classIndiVal, resultList))

    # for debugging purpose
    print("\t\tClass PN sum {0}".format(pnSum))
    print("\t\tPrinting final formula components")

    for i in range(len(interAttriEntropy)):
        formu1part = (sum(attriPNList[i]) / pnSum)
        formu1part = round(formu1part, 3)
        resultEntropy += formu1part * interAttriEntropy[i]
        # for debugging purpose
        print("\t\t{0}\t{1} * {2} = {3}".format(i, formu1part,
                                                interAttriEntropy[i], formu1part * interAttriEntropy[i]))

    resultEntropy = round(resultEntropy, 3)
    return resultEntropy

# printing the decision tree for visual purpose


def printTree(rootNode, space):
    print("{0}{1}  -  {2}".format(space * "\t\t",
                                  rootNode.connect, rootNode.attri))
    space += 1
    for child in rootNode.child:
        printTree(child, space)

# getting the root attribute for a given dataset


def getRootAttribute(dataList, resultList, indiVal, nameList):

    # Printing all data so that we can understand what we are working with

    # for debugging purpose
    print("\nThe dataset:-")
    for i in range(len(dataList)):
        print("{0}\t\t{1}".format(nameList[i], dataList[i]))

    print("\nThe output dataset:-")
    print("{0}\t\t{1}".format(nameList[-1], resultList))

    # for debugging purpose
    print("\nIndividual values of the dataset:-")
    for i in range(len(nameList)):
        print("{0}\t\t{1}".format(nameList[i], indiVal[i]))

    outClassEntr = getOutputClassEntropy(resultList, indiVal[-1])
    outClassEntr = round(outClassEntr, 3)

    # for debugging purpose
    print("\n\tResult Class Entropy - \t{0}".format(outClassEntr))

    # finding the gain of each attribute
    gainOfEachAttri = []
    print("\n")
    for i in range(len(nameList) - 1):
        attriEntropy = getAttriClassEntropy(
            dataList[i], resultList, indiVal[i], indiVal[-1], nameList[i])

        # for debugging purpose
        print("\t\tEntropy for {0}-\t{1}\n".format(nameList[i], attriEntropy))
        gainOfEachAttri.append(round(outClassEntr - attriEntropy, 3))

    # for debugging purpose
    print("\n\tGain of Attribute Classes\n{0}\n{1}  {2}".format(
        nameList, gainOfEachAttri, outClassEntr))

    # returning the attribute index
    # if the gain is 0 for all elements return none
    if gainOfEachAttri.count(0) == len(gainOfEachAttri):
        return None
    else:
        return gainOfEachAttri.index(max(gainOfEachAttri))

# building the decision tree


def buildingTree(rootNode, dataList, resultList, indiVal, nameList, loopCount):
    print("\t\t\nLOOP\tCOUNT \t", loopCount)
    # getting the root attribute index
    rootIndex = getRootAttribute(dataList, resultList, indiVal, nameList)

    # if the rootIndex is None that means the result set consists of a single value only
    # we make that single result set value as our output class value and add it as the end leaf node
    if rootIndex == None:
        # for debugging purpose
        print("\t\tNo Root Attribute for loop ", loopCount)
        # leaf node is added- Result Class node is added
        rootNode.attri = nameList[-1]
        node = Node(connect=resultList[0])
        node.addRoot(rootNode)
        rootNode.addChild(node)
        print("Current Node name - ", rootNode.attri)
        print("\t\tEnding node was added")
        rootNode.printChild()
        return

    # for debugging purpose
    print("\n\nRoot attribute for loop ",
          loopCount, "is   ", nameList[rootIndex])

    # attribute name is set for the existing node
    rootNode.setAttri(nameList[rootIndex])

    # branches are made from the node according to it's individual values
    # branches are called "connect" here
    for val in indiVal[rootIndex]:
        node = Node(connect=val)
        node.addRoot(rootNode)
        rootNode.addChild(node)

    # for debugging purpose
    print("\nNode created with child   - ", rootNode.attri)
    rootNode.printChild()

    # creating the new dataset for passing on to build the furthur tree
    loopCount += 1
    (newDataList, newResultList, newIndiVal, newNameList) = (
        [], [], indiVal[:], nameList[:])

    del newIndiVal[rootIndex]
    del newNameList[rootIndex]

    # building the new resultList
    indexList = []
    for child in rootNode.child:
        tempResultList = []
        tempList = []
        for i in range(len(dataList[rootIndex])):
            if dataList[rootIndex][i] == child.connect:
                tempResultList.append(resultList[i])
                tempList.append(i)
        newResultList.append(tempResultList)
        indexList.append(tempList)

    # building the new dataList
    for singleIndexList in indexList:
        tempList1 = []
        for i in range(len(dataList)):
            if i != rootIndex:
                tempList2 = []
                for j in singleIndexList:
                    tempList2.append(dataList[i][j])
                tempList1.append(tempList2)
        newDataList.append(tempList1)

    # if data has only 1 attribute then no way of finding the root attribute
    if len(dataList) != 1:
        ind = 0
        # building the tree from each child node of the root node with the modified datasets
        for child in rootNode.child:
            buildingTree(
                child, newDataList[ind], newResultList[ind], newIndiVal, newNameList, loopCount)
            ind += 1

# taking input for decision making


def getInput():
    inputIndex = []
    # displaying the options in an organized manner
    print("\n\nStart entering your input data")
    for i in range(len(nameList) - 1):
        print("Enter value for \"{0}\"".format(nameList[i]))
        for j in range(len(indiVal[i])):
            print("\tPress {0} for {1}".format(j, indiVal[i][j]))
        inp = int(input("\t\tENTER YOUR CHOICE\n"))
        if inp < 0 or inp >= len(indiVal[i]):
            print("\nSorry wrong input is not allowed please try again\n")
            return
        inputIndex.append(inp)

    return inputIndex

# printing the result according to the input given


def printOutput(rootNode, dic, className):
    if rootNode.attri == className:
        child = rootNode.child[0]
        print("{0}\t-\t{1}".format(className, child.connect))
    for i in dic:
        if rootNode.attri == i[0]:
            rootNode = rootNode.getChildByConnect(i[1])
            printOutput(rootNode, dic, className)
            break



# datasetname
# different datasets  are commented out uncomment only the one u wish to use
dataFile = open("dataset.txt", "r")
#dataFile = open("dataset2.txt", "r")
#dataFile = open("irisset.txt", "r")

# getting the attribute names
nameList = dataFile.readline().strip().split(",")

# building the dataset to a matrix
dataList = []
for i in dataFile:
    dataList.append(i.strip().split(","))
dataFile.close()

# converting list column wise matrix
dataList = convertToColList(nameList, dataList)

# getting the values for each attribute
indiVal = []
for i in dataList:
    indiVal.append(returnIndiVal(i))

resultList = dataList[-1]
dataList = dataList[0:len(dataList) - 1]  # seperating the result values


rootNode = Node(connect="root")
# for debugging purpose
loopCount = 1

# Building the decsion tree with the base dataset
buildingTree(rootNode, dataList, resultList, indiVal, nameList, loopCount)

# printing the tree for visualisation purpose
printTree(rootNode, 0)

print("\n\n\n Building the tree is done\nPlease ignore the above debug messages\n\n")

# getting the input indexes to map them to respective values
inputIndex = getInput()

# dic = [key , val] array
dic = []
for i in range(len(nameList) - 1):
    enter = []
    enter.append(nameList[i])
    enter.append(indiVal[i][inputIndex[i]])
    dic.append(enter)

# getting the result output
printOutput(rootNode, dic, nameList[-1])
