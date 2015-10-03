import wikipedia
import urllib
import re

#wikipedia.set_rate_limiting(True)

start = wikipedia.page('Cosmicism')
dest = wikipedia.page('Cthulhu')

ReverseAssociations = {}

# wikipedia.set_rate_limiting(True)

# UNFINISHED/DEPRECATED sorting method to figure out the most valuable links on a Wiki page
# def sort(links):
#   linksize = {}
#   for x in range(len(links)):
#     try:
#       page = wikipedia.page(links[x])
#     except wikipedia.exceptions.WikipediaException:
#       continue
#     linksize[links[x]] = len(page.links)
#     try:
#       print("Page: %s\nLinks: %s\n" % (links[x], linksize[links[x]]))
#     except UnicodeEncodeError:
#       print("Page: UNDEFINED\nLinks: %s\n" % (linksize[links[x]]))

# Uses a wiki-text URL dump to generate a list of links for the given Wikipedia page
def getLinks(page, MasterList):

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
    if re.match('\w+?:', links[index]) or links[index] in MasterList:
      del links[index]
      index -= 1
      length -= 1

    index += 1

  return links

# Checks to see if the destination page is in the passed in list
def Comparison(links):
  for x in range(len(links)):
    if links[x].lower() == dest.title.lower():
      return x
  return -1

def DeeperSearch(PreviousList):

    ToBeList = []

# Traverses links across layers of Wiki pages
def DeeperSearch(PreviousList):
    for x in range(len(PreviousList)):
        try:
            next = wikipedia.page(PreviousList[x])
        except wikipedia.exceptions.WikipediaException:
            continue

        CurrentList = getLinks(next, MasterList)

        for y in range(len(CurrentList)):
            AssociateTo(CurrentList[y],next.title)

        if(Comparison(CurrentList) >= 0 ):
            return
            path.append(next.title.lower())
            return x

        for i in CurrentList:
            if i not in MasterList:
                ToBeList.append(i)
                MasterList.append(i)

    DeeperSearch(ToBeList)

def AssociateTo (Ancestor, predecessor):
  ReverseAssociations[Ancestor] = predecessor

def CheckAndPrintAllAssociationsTo(Ancestor):
  #print(ReverseAssociations)

  for x in ReverseAssociations:
    if x.lower() == Ancestor.lower():
        print(ReverseAssociations[x], "and",
         x, "are directly connected")

        CheckAndPrintAllAssociationsTo(ReverseAssociations[x])
        return
  return




MasterList = []

###############################################################################

start = wikipedia.page('Cosmicism')
dest = wikipedia.page('Cthulhu')

MasterList = []
PreviousList = []
path = []
CurrentList = getLinks(start, MasterList)
for y in range(len(CurrentList)):
            AssociateTo(CurrentList[y],start.title)

if(Comparison(CurrentList) >= 0 ):
  path.append(dest.title.lower())
else:
    PreviousList = CurrentList

    for i in PreviousList:
        if i not in MasterList:
            MasterList.append(i)

    DeeperSearch(PreviousList)
    CheckAndPrintAllAssociationsTo(dest.title)

    position = DeeperSearch(PreviousList)
    path.append(PreviousList[position].lower())

for x in range(len(path)):
  print('%s: %s' % (x+1, path[x]))
