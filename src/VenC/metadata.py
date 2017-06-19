#! /usr/bin/python3

import datetime

class MetadataNode:
    def __init__(self, value, entry):
        self.count = 1
        self.weight = 1
        self.path = str()
        self.value = value
        self.relativeOrigin = str()
        self.relatedTo = [entry]
        self.childs = list()

def GetMetadataByName(keys, name):
    for key in keys:
        if key.value == name:
            return key
    return None


''' Might need refactorisation '''
def GetDatesList(keys, relativeOrigin, datesDirectoryName):
    output = list()
    maxWeight = 0
    for key in keys:
        if maxWeight < key.count:
            maxWeight = key.count
        output.append({"date": key.value, "count":key.count,"dateUrl":relativeOrigin+key.value})

    for key in output:
        key["weight"] = str(int((key["count"]/maxWeight)*10))

    return sorted(output, key = lambda date: datetime.datetime.strptime(date["date"], datesDirectoryName))

def GetMetadataTreeMaxWeight(metadata, maxWeight=0):
    currentMaxWeight = maxWeight
    for current in metadata:
        if current.count > currentMaxWeight:
            currentMaxWeight = current.count
        m = GetMetadataTreeMaxWeight(current.childs, maxWeight=currentMaxWeight)
        if m > currentMaxWeight:
            currentMaxWeight = m

    return currentMaxWeight

def GetMetadataTree(metadata, root=dict(), maxWeight=None):
    node = root

    if len(metadata) != 0:
        node["_nodes"] = dict()

    for current in metadata:
        node[current.value] = dict()
        node[current.value]["__categoryPath"] = current.path
        if maxWeight != None:
            node[current.value]["__count"] = current.count
            node[current.value]["__weight"] = int((current.count/maxWeight) * 10)
        if len(current.childs) != 0:
            node[current.value]["_nodes"] = dict()
            GetMetadatasTree(current.childs, node[metadata.value]["_nodes"], maxWeight)

    return node
