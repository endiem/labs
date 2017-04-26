import urllib.request
import urllib.parse
import pandas as pd
import fnmatch, os
import os.path
from datetime import datetime


def province_ABC_line(c):
    matrix = [24, 25, 5, 6, 27, 23, 26, 7, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 8, 9, 10, 1, 3, 2, 4]
    return matrix[c]


def download(provinceID):
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID=" + str(
        province_ABC_line(provinceID - 1)) + "&year1=1981&year2=2017&type=Mean"
    vhi_url = urllib.request.urlopen(url)
    csvn = 'id_' + str(provinceID) + ".csv" #+ str(datetime.now().strftime("%d%m%Y%I:%M%p")) не работпет
    out = open(csvn, 'wb')
    out.write(vhi_url.read())
    out.close()
    f = open(csvn, 'r')
    s = f.read()
    s = s.replace(s[0:s.find('\n')], 'year,week,SMN,SMT,VCI,TCI,VHI')
    s = s.replace("</pre></tt>", '')
    ns = ''
    j = 0
    while j + 3 < len(s):
        ns += s[j]
        if s[j].isdigit() and ((s[j + 1] == ' ' and s[j + 2].isdigit() and not (s[j + 3] == '\n')) or (
                            s[j + 1] == ' ' and s[j + 2] == ' ' and s[j + 3].isdigit())):
            ns += ','
        j += 1
    ns += s[j]
    ns += s[j + 1]
    ns += s[j + 2]
    s = ns
    s = s.replace(' ', '')
    f.close()
    fo = open(csvn, 'w')
    fo.write(s)
    fo.close()

#i = 1
#while i < 26:
#    download(i)
#    i += 1


def locVHI(id):
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, 'id_' + str(id) + '*.csv'):
            df = pd.read_csv(file, index_col=False, header=0)
            # print df
            com = input('find max and min? y/n: ')
            if com == 'y':
                year = int(input('year: '))
                pf = df[df['year'] == year]
                print(pf[pf['VHI'] == pf['VHI'].max()])
                print(pf[pf['VHI'] == pf['VHI'].min()])
            com = input('find drought years? y/n: ')
            if com == 'y':
                perc = int(input('%>: '))
                print(df[df['VCI'] < (100 - perc)])
                # print pf[pf['VHI']==pf['VHI'].max()]
                # print pf[pf['VHI']==pf['VHI'].min()]
            break


com = input('command: ')
if com == 'locVHI':
    loc = input('location id: ')
    locVHI(loc)
