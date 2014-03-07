#-------------------------------------------------------------------------------
# Name:        fetch-with-mechanize
# Purpose:
# The gist is that www.legislature.ca.gov/port-bilinfo.html has a form,
# and this automates submitting the form and crawling the response for the
# sections called "analysis", from which this extracts the URLs for the
# actual analyses.  The plan is to inject the data from those replies into
# a db (probably hadoop) and query for patterns that prove or disprove that
# financial analysis scoped to too-short a timeframe is suboptimal
# Author:      Jim
#
# Created:     29/10/2013
# Copyright:   (c) Jim Whitfield 2013
# Licence:     MIT
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()


import mechanize
from bs4 import BeautifulSoup

url= "http://www.legislature.ca.gov/port-bilinfo.html"
#url = "http://www.legislature.ca.gov/cgi-bin/port-postquery"
br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots
br.open(url)
br.select_form(nr=0)
br["sess"] = ["CUR"] # Current session
br["house"] = ["S"]  # Senate
br["hits"] = ["All"]
br["searchby"] = ["leginfo_bnumber"]
br["searchfor"] = "320"   # ultimately, all, for dev, this one
#br["submit"] ="Search"
br.find_control("bnumber").readonly = False
br["bnumber"] = "320"
#br["member"]=""
#br["search_term"] =""
res = br.submit()
content = res.read()
soup = BeautifulSoup(content)
#print(soup.prettify())

an = soup.find(text="Analyses")
print(an.parent.prettify())
an1 = an.parent.findNext('td').findNext('b').findNext('a').get('href')
print(an1)

analyses_urls = []
h3_list = soup.find_all('h3')
#print("found h3 count " + str(len(h3_list)))
for i in range(len(h3_list)):
    #print(i.prettify())
    if "Analyses" in h3_list[i]:
        #print ("found Analyses at " + str(i))
        node = h3_list[i].next_sibling
        while node != h3_list[i+1]:
            print type(node)
            if type(node) == 'bs4.element.Tag':
                record = node.findNext('td').findNext('b').findNext('a').get('href')
                print ("record:" , record)
                if 'http' in record:
                    analyses_urls.append(record)

            # now call another program on that url to populate the db
            node = node.next_sibling
#        refs = i.find_next_siblings()
#        t = refs.find('table')
#        td = refs.find('td')
#        print "==>" + td.prettify()
    i += 1

for i in analyses_urls:
    print analyses_urls[i]
