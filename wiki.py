import wikipedia
import Bisector
import urllib
import re

#wikipedia.set_rate_limiting(True)

start = wikipedia.page('Cosmicism')
dest = wikipedia.page('Cthulhu')

def sort(links):
  linksize = {}
  for x in range(len(links)):
    try:
      page = wikipedia.page(links[x])
    except wikipedia.exceptions.WikipediaException:
      continue
    linksize[links[x]] = len(page.links)
    try:
      print("Page: %s\nLinks: %s\n" % (links[x], linksize[links[x]]))
    except UnicodeEncodeError:
      print("Page: UNDEFINED\nLinks: %s\n" % (linksize[links[x]]))



# Uses a wiki-text URL dump to generate a list of links for the given Wikipedia page
def getLinks(page, MasterList):
  urlBase = "https://en.wikipedia.org/w/index.php?action=raw&title="
  title = page.title.replace(" ", "%20")
  url = urlBase + title

  temp = urllib.request.urlopen(url)
  wikiText = str(temp.read())

  linksFix = re.search('==\s*external links\s*==', wikiText, re.I)
  if linksFix == None:
    linksFix = re.search('==\s*references\s*==', wikiText, re.I)
  if linksFix == None:
    linksFix = re.search('==\s*see also\s*==', wikiText, re.I)

  try:
    wikiText = wikiText[0:linksFix.start()]
  except:
    pass

  links = re.findall('\[\[(.+?)(\|.+?|)\]\]', wikiText)
  index = 0
  length = len(links)
  while index < length:
    links[index] = links[index][0].lower()
    if re.match('\w+?:', links[index]):
      del links[index]
      index -= 1
      length -= 1
    if links[index] in MasterList:
      del links[index]
      index -= 1
      length -= 1
    index += 1

  return links

def Comparison(ListOLinks):
  for x in range(len(ListOLinks)):
    if ListOLinks[x].lower() == dest.title.lower():
      return x
  return -1

def DeeperSearch(PreviousList):

    for x in range(len(PreviousList)):
        try:
            next = wikipedia.page(PreviousList[x])
        except wikipedia.exceptions.WikipediaException:
            continue

        CurrentList = getLinks(next, MasterList)

        if(Comparison(CurrentList) >= 0 ):
            print(next.title.lower(), "and", dest.title.lower(),
                 "are directly connected")
            return x

        for i in CurrentList:
            if i not in MasterList:
                MasterList.append(i)


MasterList = []
PreviousList = []
CurrentList = getLinks(start, MasterList)

if(Comparison(CurrentList) >= 0 ):
    print(start.title.lower(), "and",
         dest.title.lower(), "are directly connected")
else:
    PreviousList = CurrentList

    for i in PreviousList:
        if i not in MasterList:
            MasterList.append(i)

    position = DeeperSearch(PreviousList)
    print(start.title.lower(), "and", PreviousList[position].lower()
        , "are directly connected")













