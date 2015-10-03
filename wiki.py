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
  ReverseAssociations[ancestor] = predecessor

###############################################################################

def checkAndPrintAllAssociationsTo(ancestor,Counter):
  #print(ReverseAssociations)

  for x in ReverseAssociations:
    if x.lower() == ancestor.lower() and Counter != 0:
        print(ReverseAssociations[x], "and",
         x, "are directly connected")
        Counter = Counter - 1
        checkAndPrintAllAssociationsTo(ReverseAssociations[x], Counter)
        return
  return

###############################################################################

masterList = []

start = wikipedia.page('Jesus')
dest = wikipedia.page('Hitler')


ReverseAssociations = {}
masterList = []
previousList = []

currentList = getLinks(start, masterList)
for y in range(len(currentList)):
  associateTo(currentList[y],start.title)
counter = 1;

if(findDest(currentList) >= 0 ):
  checkAndPrintAllAssociationsTo(dest.title, counter)
  #path.append(dest.title.lower())
else:
    previousList =currentList

    for i in previousList:
        if i not in masterList:
            masterList.append(i)

    counter = layerSearch(previousList, counter)
    checkAndPrintAllAssociationsTo(dest.title, counter)

    #path.append(previousList[position].lower())

#for x in range(len(path)):
#  print('%s: %s' % (x+1, path[x]))
