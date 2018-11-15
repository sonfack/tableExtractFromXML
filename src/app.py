from typing import List, Any

from src.Article import Article


def main():
    file1 = '../data/PMC3968010.xml'
    file2 = '../data/PMC2515340.xml'
    file3 = '../data/PMC2474671.xml'
    file4 = '../data/PMC3077385.xml'
    file5 = '../data/PMC5137041.xml'
    file6 = '../data/PMC6115326.xml'

    myArticle = Article(file6)
    print('\n\n########################### Get article title ##########################')
    print(myArticle.title)
    print('########################################################################\n\n')

    print('#################### Search for table tag in article ###################')
    for tag in myArticle.searchTagInArticle('table', rootTag=None):
        print(tag.tag)
    print('########################################################################\n')

    #print('#################### Search for tag  Alternatives in article ###################')
    #for tag in myArticle.getArticleListOfTableWrapAlternatives():
        #print(tag)

    #print('######################## Search for table tag in article #######################')
    #for tag in myArticle.getArticleListOfTable():
        #print(tag)
    #print('################################################################################\n')

    print('\n\n\n\n##################### Search for table thead tag in article ####################')
    nbTableHead = 0
    listThead = []
 #   print("############ number of headers " + str(len(myArticle.getArticleListOfTableThead())))
    for tagHead in myArticle.getArticleListOfTableThead():
        nbTableHead = nbTableHead + 1
        print("++++++++++++ thead number  :", nbTableHead)
        print("============ number of tr : "+str(len(tagHead)))
        listTr = []
        countTr = 0
        for tr in myArticle.getArticleListOfTableTr(tagHead):
            listTd = []
            if countTr >= 1:
                copyTd = []
                for it in tr.iter():
                    if it.tag == "td":
                        td = {
                            'colspan': str(it.get('colspan')),
                            'rowspan': str(it.get('rowspan')),
                            'data': str(it.text).strip()
                        }
                        copyTd.append(td)
                    elif it.tag != "tr":
                        tdTag = copyTd.pop()
                        td = {
                            'colspan': str(it.get('colspan')),
                            'rowspan': str(it.get('rowspan')),
                            'data': tdTag['data'] + '#' + str(it.text).strip()
                        }
                        copyTd.append(td)

                prevTr = listTr[countTr - 1]

                for countTd in range(len(prevTr)):
                    if prevTr[countTd]['colspan'] != 'None' and  int(prevTr[countTd]['colspan']) >= 2:
                        for i in range(countTd, countTd + int(prevTr[countTd]['colspan'])):
                            copyTd[i] = {
                                'colspan': copyTd[i]['colspan'],
                                'rowspan': copyTd[i]['rowspan'],
                                'data': prevTr[countTd]['data'] + '@' + copyTd[i]['data']
                            }

                countTd = 0
                countMod = 0
                while countTd < len(prevTr):

                    if int(prevTr[countTd]['colspan']) >= 2:
                        countTd = countTd + 1
                        countMod = countMod + int(prevTr[countTd]['colspan']) + 1

                    elif prevTr[countTd]['data'] == 'None':
                        countTd = countTd + 1
                        countMod = countMod + 1
                    else:
                        copyTd[countMod] = {
                            'colspan': copyTd[countMod]['colspan'],
                            'rowspan': copyTd[countMod]['rowspan'],
                            'data': prevTr[countTd]['data'] + '@' + copyTd[countMod]['data']
                        }
                        countTd = countTd + 1
                        countMod = countMod + 1

                listTr.append(copyTd)
            else:
                for it in tr.iter():
                    if it.tag == "td":
                        td = {
                            'colspan': str(it.get('colspan')),
                            'rowspan': str(it.get('rowspan')),
                            'data': str(it.text).strip()
                        }
                        listTd.append(td)
                    elif it.tag != "tr":
                        tdTag = listTd.pop()
                        td = {
                            'colspan': str(it.get('colspan')),
                            'rowspan': str(it.get('rowspan')),
                            'data': tdTag['data'] + '#' + str(it.text).strip()
                        }
                        listTd.append(td)
                listTr.append(listTd)
            countTr = countTr + 1
        listThead.append(listTr)

    print(len(listThead))
    for thead in listThead:
        print("\n tr of head : "+ str(len(thead)))
        print(thead)
'''
    print('\n\n#################### Search for table tbody tag in article ###################\n\n\n\n\n')

    listTbody = []
    for tagTbody in myArticle.getArticleListOfTableTbody():
        listTr = []
        for tr in myArticle.getArticleListOfTableTr(tagTbody):
            listTd = []
            for it in tr.iter():
                if it.tag == "td":
                    listTd.append(str(it.text).strip())
                elif it.tag != "tr":
                    tdTag = listTd.pop()
                    tdTag = tdTag + '#' + str(it.text).strip()
                    listTd.append(tdTag)
            listTr.append(listTd)
        listTbody.append(listTr)


    for tbody in listTbody:
        print("\n tr of body : "+str(len(tbody)))
        print(tbody)
    print("\n\n\n\n\n\n\n")


    for i in range(len(listTbody)):
        print("\n\n")
        tbody = listTbody[i]

        for j in range(len(tbody)):
            tr = tbody[j]
            for k in range(len(tr)):
                print(" k : "+str(k))
                thead = listThead[i]
                sizeTr = len(thead)
                print(sizeTr)
                counthead = 1
                lastTr = thead[-1*counthead]
                hisHead = lastTr[k]
                print("----------------------"+hisHead+"-------------------")

                while str(hisHead) == "None" and -1*(counthead) > -1*sizeTr:
                    counthead = counthead + 1
                    lastTr = thead[-1*(counthead)]
                    print(lastTr)
                    if k < len(lastTr):
                        hisHead = lastTr[k]
                        print("Header ------------------------------ "+hisHead)

                print(hisHead+"@"+tr[k])

        print("\n\n")
'''

if __name__ == '__main__':
    main()