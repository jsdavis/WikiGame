import wikipedia
from linkFinder import *

# Checks to see if the destination page is in the passed in list
def findLink(links, wantedLink):
  for x in range(len(links)):
    if links[x].lower() == wantedLink.title.lower():
      return x
  return -1

###############################################################################

# Traverses links across layers of Wiki pages
def layerSearch(previousList, counter, dest):
    global masterList
    toBeList = []
    counter += 1
    for x in range(len(previousList)):
        try:
            nextElem = wikipedia.page(previousList[x])
        except wikipedia.exceptions.WikipediaException:
            continue

        currentList = getLinks(nextElem, masterList)

        for y in range(len(currentList)):
            associateTo(currentList[y],nextElem.title)

        if(findLink(currentList, dest) >= 0 ):
            return counter

        for i in currentList:
            if i not in masterList:
                toBeList.append(i)
                masterList.append(i)

    layerSearch(toBeList, counter, dest)

###############################################################################

def associateTo(ancestor, predecessor):
  reverseAssociations[ancestor] = predecessor

###############################################################################

def acquireAllAssociations(ancestor,counter, listStrings):

  for x in reverseAssociations:
    if x.lower() == ancestor.lower() and counter != 0:
        listStrings = listStrings + [reverseAssociations[x]]
        counter = counter - 1
        return acquireAllAssociations(reverseAssociations[x], counter, listStrings)
        
  return listStrings

###############################################################################

def main(begin, end):

  try:
    start = wikipedia.page(begin)
  except wikipedia.exceptions.PageError: 
      return ("\nSorry the start page %s doesn't exist" %begin)
  try:
    dest = wikipedia.page(end)
  except wikipedia.exceptions.PageError: 
      return ("\nSorry the ending page %s doesn't exist" %end)
  
  previousList = []
  listOfConnections = []
  
  currentList = getLinks(start, masterList)
  result = 1;
  
  for y in range(len(currentList)):
    associateTo(currentList[y],start.title)
    


  if(findLink(currentList, dest) >= 0 ):
    listOfConnections = acquireAllAssociations(dest.title,
       result, listOfConnections)
    
  else:
    previousList = currentList

    for i in previousList:
        if i not in masterList:
            masterList.append(i)

    result = layerSearch(previousList, result, dest)
    listOfConnections = acquireAllAssociations(dest.title, 
        result, listOfConnections)

  return [dest.title] + listOfConnections 
    
###############################################################################
# Globals

masterList = []
reverseAssociations = {}
