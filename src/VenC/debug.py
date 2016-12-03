#! /usr/bin/python3

def PrintCategoriesTree(tree,indentation=""):
    for node in tree:
        print(indentation+node.value, "->", node.relatedTo)
        PrintCategoriesTree(node.childs,indentation+"\t")
        
