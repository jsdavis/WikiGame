import urllib
import re

# Uses a wiki-text URL dump to generate a list of links for the given Wikipedia page (using the title)
def getLinks(page, masterList):

  print("\n\n\n%s\n" % str(page.encode('utf-8')))

  # URL from which you can pull raw wiki-text from any page, given the title
  urlBase = "https://en.wikipedia.org/w/index.php?action=raw&title="
  title = page.replace(" ", "%20")
  url = urlBase + title

  print("%s" % str(url.encode('utf-8')))

  urlPage = None
  while urlPage == None:
    try:
      urlPage = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
      # For whatever reason, some things in () must be lowercase to avoid 404
      index = url.rfind("(")
      if index != -1:
        url = url[:index] + url[index:].lower()
    except UnicodeEncodeError:
      # Fix for foreign characters in Wiki articles
      url = str(url.encode('utf-8'))

  wikiText = str(urlPage.read())


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
    wikiText = wikiText[:linksFix.start()]
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