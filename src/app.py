from typing import List, Any
import os
from src.Article import Article
from src.ArticleTable import ArticleTable

def writeTableInFile(listTables, fileName, testFolder= "../test"):
    filename, file_extension = os.path.splitext(fileName)
    filePath = os.path.join(testFolder, filename)


    print('==========================================================================================')
    print(len(listTables))
    if len(listTables) > 0:
        f = open(filePath, "w+")
        for tab in listTables:
            f.write(" ".join(tab.caption))
            f.write("\n\n")
            for head in tab.tableHead:
                for tr in head:
                    f.write("\n")
                    f.write(str(tr))
            f.write("\n\n")
            for body in tab.tableBody:
                for tr in body:
                    f.write("\n")
                    f.write(str(tr))
            f.write("\n================================================================================\n\n\n")
        f.close()



def createTest(datasetFolder= "../data", testFolder="../test"):
    files = os.listdir(datasetFolder)
    print("Number of XML files  : " + str(len(files)))

    # Create target Directory if don't exist
    if not os.path.exists(testFolder) and not os.path.exists(testFolder):
        os.mkdir(testFolder)
        print("Directory ", testFolder, " Created ")
    else:
        print("Directories ", testFolder, "  already exists")

    listOfTables = []
    for file in files:

        myArticle = Article(os.path.join(datasetFolder,file))

        print('\n\n########################### Get article title ##########################')
        print(myArticle.title)
        print('########################################################################\n\n')


        print('#################### Search for table tag in article ###################')
        for tag in myArticle.searchTagInArticle('table-wrap', rootTag=None):
            print(tag.tag)

            myTable = ArticleTable(file)
            captions = myArticle.searchTagInArticle('caption', tag)
            print(len(captions))
            theCaption = []
            myArticle.getTextOfAGivenTag(captions[0], theCaption)
            myTable.setTableCaption(theCaption)

            tables = myArticle.searchTagInArticle('table', tag)
            if len(tables) > 0:
                nbTableHead = 0
                listThead = []
                for tagHead in myArticle.searchTagInArticle('thead', tables[0]):
                    nbTableHead = nbTableHead + 1
                    print("++++++++++++ thead :", nbTableHead)
                    print("========= tr : " + str(len(tagHead)))
                    listTr = []
                    countTr = 0
                    for tr in myArticle.searchTagInArticle('tr', tagHead):
                        listTd = []
                        if countTr >= 1:
                            copyTd = []
                            for it in tr.iter():
                                if it.tag == "td" or it.tag == "th":
                                    listTdData = []
                                    myArticle.getTextOfAGivenTag(it, listTdData)
                                    if len(str(it.get('colspan')).strip()) == 0 or str(it.get('colspan')) == 'None':
                                        cols = 1
                                    else:
                                        cols = int(str(it.get('colspan')))

                                    if len(str(it.get('rowspan')).strip()) == 0 or str(it.get('rowspan')) == 'None':
                                        rows = 1
                                    else:
                                        rows = int(str(it.get('rowspan')))
                                    td = {
                                        'colspan': str(it.get('colspan')),
                                        'rowspan': str(it.get('rowspan')),
                                        'data': '#'.join(listTdData)
                                    }
                                    copyTd.append(td)

                            prevTr = listTr[countTr - 1]
                            counttd = 0
                            for countTd in range(len(prevTr)):
                                if prevTr[countTd]['colspan'] != 'None' and int(prevTr[countTd]['colspan']) >= 2:
                                    for i in range(countTd, countTd + int(prevTr[countTd]['colspan'])):

                                        if counttd < len(copyTd):
                                            copyTd[i] = {
                                                'colspan': copyTd[i]['colspan'],
                                                'rowspan': copyTd[i]['rowspan'],
                                                'data': prevTr[countTd]['data'] + '@' + copyTd[i]['data']
                                            }
                                            counttd = counttd + 1
                                else:
                                    if counttd < len(copyTd):
                                        copyTd[counttd] = {
                                            'colspan': copyTd[counttd]['colspan'],
                                            'rowspan': copyTd[counttd]['rowspan'],
                                            'data': prevTr[countTd]['data'] + '@' + copyTd[counttd]['data']
                                        }
                                        counttd = counttd + 1

                            listTr.append(copyTd)
                        else:
                            for it in tr.iter():
                                if it.tag == "td" or it.tag == "th":
                                    listTdData = []
                                    myArticle.getTextOfAGivenTag(it, listTdData)
                                    if len(str(it.get('colspan')).strip()) == 0 or str(it.get('colspan')) == 'None':
                                        cols = 1
                                    else:
                                        cols = int(str(it.get('colspan')))

                                    if len(str(it.get('rowspan')).strip()) == 0 or str(it.get('rowspan')) == 'None':
                                        rows = 1
                                    else:
                                        rows = int(str(it.get('rowspan')))
                                    td = {
                                        'colspan': cols,
                                        'rowspan': rows,
                                        'data': '#'.join(listTdData)
                                    }
                                    listTd.append(td)
                            listTr.append(listTd)
                        countTr = countTr + 1

                    listThead.append(listTr)
                print(listThead)
                myTable.setTableHead(listThead)
                dataTbody = []
                for tbody in myArticle.searchTagInArticle('tbody', tables[0]):
                    trData = []
                    for tr in myArticle.searchTagInArticle('tr', tbody):
                        tdData = []
                        for td in tr.getchildren():
                            listTdData = []
                            myArticle.getTextOfAGivenTag(td, listTdData)
                            tdData.append("#".join(listTdData))
                        trData.append(tdData)
                    dataTbody.append(trData)
                myTable.setTableBody(dataTbody)
            listOfTables.append(myTable)
        print(len(listOfTables))
        writeTableInFile(listOfTables, file)
        listOfTables.clear()

'''
    count = 1
    dataset = os.path.dirname(datasetFolder) + "/" + os.path.basename(datasetFolder)
    for file in files:
        if count % 2 == 0:
            shutil.copy(dataset + '/' + file, test)
        else:
            shutil.copy(dataset + '/' + file, training)

        count = count + 1

    print("Total files copied : " + str(count))
    '''



def main():
    createTest()
    '''
    exit(0)
    file1 = '../data/PMC3968010.xml'
    file2 = '../data/PMC2515340.xml'
    file3 = '../data/PMC2474671.xml'
    file4 = '../data/PMC3077385.xml'
    file5 = '../data/PMC5137041.xml'
    file6 = '../data/PMC6115326.xml'

    myArticle = Article(file2)
    print('\n\n########################### Get article title ##########################')
    print(myArticle.title)
    print('########################################################################\n\n')

    listOfTables = []
    print('#################### Search for table tag in article ###################')
    for tag in myArticle.searchTagInArticle('table-wrap', rootTag=None):
        print(tag.tag)

        myTable = ArticleTable()
        captions = myArticle.searchTagInArticle('caption', tag)
        print(len(captions))
        theCaption = []
        myArticle.getTextOfAGivenTag(captions[0], theCaption)
        myTable.setTableCaption(theCaption)

        tables = myArticle.searchTagInArticle('table', tag)
        print(len(tables))
        nbTableHead = 0
        listThead = []
        for tagHead in myArticle.searchTagInArticle('thead', tables[0]):
            nbTableHead = nbTableHead + 1
            print("++++++++++++ thead :", nbTableHead)
            print("========= tr : " + str(len(tagHead)))
            listTr = []
            countTr = 0
            for tr in myArticle.searchTagInArticle('tr', tagHead):
                listTd = []
                if countTr >= 1:
                    copyTd = []
                    for it in tr.iter():
                        if it.tag == "td":
                            listTdData = []
                            myArticle.getTextOfAGivenTag(it, listTdData)
                            if len(str(it.get('colspan')).strip()) == 0 or str(it.get('colspan')) == 'None':
                                cols = 1
                            else:
                                cols = int(str(it.get('colspan')))

                            if len(str(it.get('rowspan')).strip()) == 0 or str(it.get('rowspan')) == 'None':
                                rows = 1
                            else:
                                rows = int(str(it.get('rowspan')))
                            td = {
                                'colspan': str(it.get('colspan')),
                                'rowspan': str(it.get('rowspan')),
                                'data':  '#'.join(listTdData)
                            }
                            copyTd.append(td)

                    prevTr = listTr[countTr - 1]
                    counttd = 0
                    for countTd in range(len(prevTr)):
                        if prevTr[countTd]['colspan'] != 'None' and int(prevTr[countTd]['colspan']) >= 2:
                            for i in range(countTd, countTd + int(prevTr[countTd]['colspan'])):

                                if counttd < len(copyTd):

                                    copyTd[i] = {
                                        'colspan': copyTd[i]['colspan'],
                                        'rowspan': copyTd[i]['rowspan'],
                                        'data': prevTr[countTd]['data'] + '@' + copyTd[i]['data']
                                    }
                                    counttd = counttd + 1
                        else:
                            if counttd < len(copyTd):
                                copyTd[counttd] = {
                                    'colspan': copyTd[counttd]['colspan'],
                                    'rowspan': copyTd[counttd]['rowspan'],
                                    'data': prevTr[countTd]['data'] + '@' + copyTd[counttd]['data']
                                }
                                counttd = counttd + 1

                    listTr.append(copyTd)
                else:
                    for it in tr.iter():
                        if it.tag == "td":
                            listTdData = []
                            myArticle.getTextOfAGivenTag(it, listTdData)
                            if len(str(it.get('colspan')).strip()) == 0 or str(it.get('colspan')) == 'None':
                                cols = 1
                            else:
                                cols = int(str(it.get('colspan')))

                            if len(str(it.get('rowspan')).strip()) == 0 or str(it.get('rowspan')) == 'None':
                                rows = 1
                            else:
                                rows = int(str(it.get('rowspan')))
                            td = {
                                'colspan': cols,
                                'rowspan': rows,
                                'data': '#'.join(listTdData)
                            }
                            listTd.append(td)
                    listTr.append(listTd)
                countTr = countTr + 1

            listThead.append(listTr)
            myTable.setTableHead(listThead)
            dataTbody = []
            for tbody in myArticle.searchTagInArticle('tbody', tables[0]):
                trData = []
                for tr in myArticle.searchTagInArticle('tr', tbody):
                    tdData = []
                    for td in tr.getchildren():
                        listTdData = []
                        myArticle.getTextOfAGivenTag(td, listTdData)
                        tdData.append("#".join(listTdData))
                    trData.append(tdData)
                dataTbody.append(trData)
            myTable.setTableBody(dataTbody)
        listOfTables.append(myTable)
    return listOfTables

    print('#####################################################################################################################\n')

    for tab in listOfTables:
        print(tab.caption)
        print("\n\n")
        for tr in tab.tableHead:
            for td in tr:
                print(td)
        print("\n\n")
        for tr in tab.tableBody:
            for td in tr:
                print(td)
        print("#################################\n\n\n\n")

    '''


    '''
     exit(0)
    
    print('#################### Search for table tag in article ###################')
    for tag in myArticle.searchTagInArticle('thead', rootTag=None):
        print(tag)
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