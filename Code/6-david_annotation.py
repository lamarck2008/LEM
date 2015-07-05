#!python
# by courtesy of HuangYi @ 20110424

import sys

def DAVIDenrich(listF, idType, bgF='', resF='', bgName = 'Background1',listName='List1', category = '', thd=0.1, ct=2):
    from suds.client import Client
    import os
   
    if len(listF) > 0 and os.path.exists(listF):
        inputListIds = ','.join(open(listF).read().split('\n'))
        print 'List loaded.'        
        print inputListIds
    else:
        print 'No list loaded.'
        raise

    flagBg = False
    if len(bgF) > 0 and os.path.exists(bgF):
        inputBgIds = ','.join(open(bgF).read().split('\n'))
        flagBg = True
        print 'Use file background.'
    else:
        print 'Use default background.'

    client = Client('http://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl')
    print 'User Authentication:',client.service.authenticate('yantan@broadinstitute.org')

    listType = 0
    print 'Percentage mapped(list):', client.service.addList(inputListIds,idType,listName,listType)
    if flagBg:
        listType = 1
        print 'Percentage mapped(background):', client.service.addList(inputBgIds,idType,bgName,listType)

    print category
    print 'Use categories:', client.service.setCategories(category)
    chartReport = client.service.getChartReport(thd,ct)
    chartRow = len(chartReport)
    print 'Total chart records:',chartRow
    
    if len(resF) == 0 or not os.path.exists(resF):
        if flagBg:
            resF = listF + '.withBG.chartReport'
        else:
            resF = listF + '.chartReport'
    with open(resF, 'w') as fOut:
        fOut.write('Category\tTerm\tCount\t%\tPvalue\tGenes\tList Total\tPop Hits\tPop Total\tFold Enrichment\tBonferroni\tBenjamini\tFDR\n')
        for row in chartReport:
            rowDict = dict(row)
            categoryName = str(rowDict['categoryName'])
            termName = str(rowDict['termName'])
            listHits = str(rowDict['listHits'])
            percent = str(rowDict['percent'])
            ease = str(rowDict['ease'])
            Genes = str(rowDict['geneIds'])
            listTotals = str(rowDict['listTotals'])
            popHits = str(rowDict['popHits'])
            popTotals = str(rowDict['popTotals'])
            foldEnrichment = str(rowDict['foldEnrichment'])
            bonferroni = str(rowDict['bonferroni'])
            benjamini = str(rowDict['benjamini'])
            FDR = str(rowDict['afdr'])
            rowList = [categoryName,termName,listHits,percent,ease,Genes,listTotals,popHits,popTotals,foldEnrichment,bonferroni,benjamini,FDR]
            fOut.write('\t'.join(rowList)+'\n')
        print 'write file:', resF, 'finished!'

if __name__ == '__main__':
    file_name = sys.argv[1]
    DAVIDenrich(listF = file_name, idType = 'ENTREZ_GENE_ID', listName = 'mylist', category = 'GOTERM_BP_ALL,GOTERM_MF_ALL,BBID,BIOCARTA,KEGG_PATHWAY') 
