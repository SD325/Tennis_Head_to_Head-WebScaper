from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re


def tab(tr):
    count = 0
    row_ = []
    for td in tr:
        if td == '\n':
            continue
        count += 1
        if count == 2:
            row_.append(td.a.text.strip())
        elif count == 3:
            row_.append(td.span.text.strip())
        elif count == 5:
            row_.append(td.a.text.strip())
        elif count != 6:
            row_.append(td.text.strip())
    return row_


# By-pass "403 : Forbidden" Error
site = "https://www.atptour.com/en/players/fedex-head-2-head/roger-federer-vs-rafael-nadal/F324/N409"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site, headers=hdr)
page = urlopen(req)
bs = BeautifulSoup(page, features='lxml')

data = []
############################################################################################
first = bs.find('table', {'class': 'modal-event-breakdown-table'}).tbody.tr
data.append(tab(first))
for tr1 in bs.find('table', {'class': 'modal-event-breakdown-table'}).tbody.tr.next_siblings:
    if tr1 == '\n':
        continue
    curr = []
    for td1 in tr1:
        if td1 == '\n':
            continue
        curr = tab(tr1)
    data.append(curr)
############################################################################################

# 0: Year
# 1: Tournament Name
# 2: Surface
# 3: Round
# 4: Winner

c = 0
for row in data:
    l = ''
    c += 1
    for x in row:
        l += x + ' || '
    print(l)

print('*' * 75)
print('Total Games:', c)
rf = 0
rn = 0
# search using regex
for row in data:
    if re.search('O.+Grass', row[2]):
        if row[4] == 'Rafael Nadal':
            rn += 1
        elif row[4] == 'Roger Federer':
            rf += 1

print('Record on Grass Court:')
print('rf:', rf)  # Roger Federer
print('rn:', rn)  # Rafael Nadal
