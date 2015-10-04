import wikipedia
import urllib
import re

# Uses a wiki-text URL dump to generate a list of links for the given Wikipedia page
def getLinks(page, masterList):

  # URL from which you can pull raw wiki-text from any page, given the title
  urlBase = "https://en.wikipedia.org/w/index.php?action=raw&title="
  title = page.title.replace(" ", "%20")
  url = urlBase + title

  temp = urllib.request.urlopen(url)
  wikiText = str(temp.read())


  # Avoid category links at the end of large articles by cutting off at one of these sections
  # Regex pulls either the 'external links', 'references', or 'see also' headers
  #   ==\s*  --> section headers are enclosed in '==', and generally have a space between the header and '=='
  linksFix = re.search('==\s*external links\s*==', wikiText, re.I)
  if linksFix == None:
    linksFix = re.search('==\s*references\s*==', wikiText, re.I)
  if linksFix == None:
    linksFix = re.search('==\s*see also\s*==', wikiText, re.I)

  # Truncate the raw wiki-text before we extract links
  try:
    wikiText = wikiText[0:linksFix.start()]
  except:
    pass

  # Regex extracts links into the first capturing group:
  #   \[\[     --> matches 2 '[' characters
  #   (.+?)    --> pulls all the characters up to the next group and captures it
  #   (/|.+?|) --> matches either a '|' character and then everything until the next thing, or nothing
  #   \]\]     --> matches 2 ']' characters
  links = re.findall('\[\[(.+?)(\|.+?|)\]\]', wikiText)
  index = 0
  length = len(links)
  while index < length:
    links[index] = links[index][0].lower()

    # Use Regex to find and remove 'XXXX: xxxx' links (i.e. 'Category: ' and 'File: ' links)
    # Also removes any links that have already been found elsewhere
    if re.match('\w+?:', links[index]) or links[index] in masterList:
      del links[index]
      index -= 1
      length -= 1

    index += 1

  return links

###############################################################################

# Checks to see if the destination page is in the passed in list
def findDest(links):
  for x in range(len(links)):
    if links[x].lower() == dest.title.lower():
      return x
  return -1

###############################################################################

# Traverses links across layers of Wiki pages
def layerSearch(previousList, counter):
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

        if(findDest(currentList) >= 0 ):
            return counter

        for i in currentList:
            if i not in masterList:
                toBeList.append(i)
                masterList.append(i)

    layerSearch(toBeList)

###############################################################################

def associateTo(ancestor, predecessor):
  reverseAssociations[ancestor] = predecessor

###############################################################################

def PrintAllAssociations(ancestor,counter):

  for x in reverseAssociations:
    if x.lower() == ancestor.lower() and counter != 0:
        print(reverseAssociations[x], "and",
         x, "are directly connected")
        counter = counter - 1
        checkAndPrintAllAssociationsTo(reverseAssociations[x], counter)
        return
  return

###############################################################################

def main(begin, end)

  start = wikipedia.page(begin)
  dest = wikipedia.page(end)
  
  previousList = []
  currentList = getLinks(start, masterList)
  masterList = []
  result = 1;
  
  for y in range(len(currentList)):
    associateTo(currentList[y],start.title)
    


  if(findDest(currentList) >= 0 ):
    PrintAllAssociations(dest.title, result)
    
  else:
    previousList =currentList

    for i in previousList:
        if i not in masterList:
            masterList.append(i)

    result = layerSearch(previousList, result)
    PrintAllAssociationsT(dest.title, result)
    
###############################################################################
# Globals

reverseAssociations = {}

