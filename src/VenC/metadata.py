#! /usr/bin/python3

class Metadata:
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
def GetDatesList(keys, relativeOrigin):
    output = list()
    maxWeight = 0
    for key in keys:
        if maxWeight < key.count:
            maxWeight = key.count
        output.append({"date": key.value, "count":key.count,"dateUrl":relativeOrigin+key.value})

    for key in output:
        key["weight"] = str(int((key["count"]/maxWeight)*10))

    return sorted(output, key = lambda date: datetime.datetime.strptime(date["date"], blogConfiguration["path"]["dates_directory_name"]))

def GetMetadataTreeMaxWeight(metadatas, maxWeight=0):
    currentMaxWeight = maxWeight
    for metadata in metadatas:
        if metadata.count > currentMaxWeight:
            currentMaxWeight = metadata.count
        m = GetCategoriesTreeMaxWeight(metadata.childs, maxWeight=currentMaxWeight)
        if m > currentMaxWeight:
            currentMaxWeight = m

    return currentMaxWeight

def GetCategoriesTree(categories, relativeOrigin, root, maxWeight=None):
    node = root

    if len(categories) != 0:
        node["_nodes"] = dict()

    for category in categories:
        node[category.value] = dict()
        node[category.value]["__categoryPath"] = category.path
        if maxWeight != None:
            node[category.value]["__count"] = category.count
            node[category.value]["__weight"] = int((category.count/maxWeight) * 10)
        node[category.value]["__relativeOrigin"] = relativeOrigin
        if len(category.childs) != 0:
            node[category.value]["_nodes"] = dict()
            GetCategoriesTree(category.childs, relativeOrigin, node[category.value]["_nodes"], maxWeight)
    return node
