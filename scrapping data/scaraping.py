import pandas as pd
import urllib.request
import sys
from pathlib import Path
Path.cwd()
import requests

website_url = requests.get('http://www.calcuttayellowpages.com/busroute.html').text
from bs4 import BeautifulSoup
soup = BeautifulSoup(website_url,'lxml')
print(soup.prettify())
My_table = soup.find('tbody')
My_table
My_row = soup.find('tr')
My_row 
links = My_row.findAll('td')
links
Countries = []
for link in links:
    Countries.append(link.get('Rout'))
    
#print(Countries)

import pandas as pd
df = pd.DataFrame()
df['Country'] = Countries
from bs4 import BeautifulSoup
import requests
import os
import codecs
wiki = "http://www.calcuttayellowpages.com/busroute.html"
header = {
    'User-Agent': 'Mozilla/5.0'
}  # Needed to prevent 403 error on Wikipedia
page = requests.get(wiki, headers=header)
soup = BeautifulSoup(page.content)

tables = soup.findAll("tbody")

# show tables
for i, table in enumerate(tables):
    print("#"*10 + "Table {}".format(i) + '#'*10)
    print(table.text[:100])
    print('.'*80)
print("#"*80)

for tn, table in enumerate(tables):

    # preinit list of lists
    rows = table.findAll("tr")
    row_lengths = [len(r.findAll(['th', 'td'])) for r in rows]
    ncols = max(row_lengths)
    nrows = len(rows)
    data = []
    for i in range(nrows):
        rowD = []
        for j in range(ncols):
            rowD.append('')
        data.append(rowD)

    # process html
    for i in range(len(rows)):
        row = rows[i]
        rowD = []
        cells = row.findAll(["td", "th"])
        for j in range(len(cells)):
            cell = cells[j]
            print(cell)
            #lots of cells span cols and rows so lets deal with that
            cspan = int(cell.get('colspan', 1))
            rspan = int(cell.get('rowspan', 1))
            l = 0
            for k in range(rspan):
                # Shifts to the first empty cell of this row
                while data[i + k][j + l]:
                    l += 1
                for m in range(cspan):
                    cell_n = j + l + m
                    row_n = i + k
                    # in some cases the colspan can overflow the table, in those cases just get the last item
                    cell_n = min(cell_n, len(data[row_n])-1)
                    data[row_n][cell_n] += cell.text
                    print(cell.text)

        data.append(rowD)

  from bs4 import BeautifulSoup
import requests
import os
import codecs
wiki = "http://www.calcuttayellowpages.com/busroute.html"
header = {
    'User-Agent': 'Mozilla/5.0'
}  # Needed to prevent 403 error on Wikipedia
page = requests.get(wiki, headers=header)
soup = BeautifulSoup(page.content)

tables = soup.findAll("tbody")
# show tables
lis=[]
lis1=[]
for i, table in enumerate(tables):
    #print("#"*10 + "Table {}".format(i) + '#'*10)
    #print(table.text[:])
    lis.append(str(table.text[:]))
    #print('.'*80)
#print("#"*80)

#print(lis)

for i in lis:
    i=i.replace('\r','')
    i=i.replace('\n','')
    i=i.replace('\r\n','')
    i=i.replace('-','')
    lis1.append(str(i).strip())
    #print(i)
    
#print(lis1)
#df2=pd.DataFrame(lis1)
#df2.to_csv('C:/Users/Navneet/Music/allr.csv')
lis2=[]
import re
for i in lis1:
    str(i)
    i=re.split(r'\t+',i)
    lis2.append(i)
lis2

for tn, table in enumerate(tables):

    # preinit list of lists
    rows = table.findAll("tr")
    row_lengths = [len(r.findAll(['th', 'td'])) for r in rows]
    ncols = max(row_lengths)
    nrows = len(rows)
    data = []
    for i in range(nrows):
        rowD = []
        for j in range(ncols):
            rowD.append('')
        data.append(rowD)

    # process html
    for i in range(len(rows)):
        row = rows[i]
        rowD = []
        cells = row.findAll(["td", "th"])
        for j in range(len(cells)):
            cell = cells[j]
            #print(cell)
            #lots of cells span cols and rows so lets deal with that
            cspan = int(cell.get('colspan', 1))
            rspan = int(cell.get('rowspan', 1))
            l = 0
            for k in range(rspan):
                # Shifts to the first empty cell of this row
                while data[i + k][j + l]:
                    l += 1
                for m in range(cspan):
                    cell_n = j + l + m
                    row_n = i + k
                    # in some cases the colspan can overflow the table, in those cases just get the last item
                    cell_n = min(cell_n, len(data[row_n])-1)
                    data[row_n][cell_n] += cell.text
                    #print(cell.text)

data.append(rowD)
print(data)

import pandas as pd
df=pd.DataFrame(data[:])
df.head()

addlist=df[1].tolist()
addlist

addlist = [str(x).replace("\r\n",'') for x  in addlist]
addlist = addlist[:110]
df1=pd.DataFrame(addlist)
#df1.to_csv('C:/Users/Navneet/Music/rout.csv')
df1

  # write data out to tab seperated format
    page = os.path.split(wiki)[1]
    fname = 'output_{}_t{}.csv'.format(page, tn)
    f = codecs.open(fname, 'w')
    for i in range(nrows):
        rowStr = '\t'.join(data[i])
        rowStr = rowStr.replace('\n', '')
        print(rowStr)
        f.write(rowStr + '\n')

    f.close()
    
print(data)