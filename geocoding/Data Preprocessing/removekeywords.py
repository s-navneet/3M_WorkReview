import pandas as pd
import os
import re
fp=os.getcwd()
keyword_fp=fp+'/keywords.txt'

#read the keyword file which you want to remove from data
def file_read(fname):
        with open(fname) as f:
                #Content_list is the list that contains the read lines.     
                content_list = f.readlines()
                #print(content_list)
        return content_list

#convert keyword file into list of keywords
#remove the white space from left and right and convert into lower case
keywords=file_read(keyword_fp)
def cleanKeywords(keywords):
    for i,val in enumerate(keywords):
        keywords[i]=keywords[i].strip().lower()
    return keywords
#print(keywords)

#read the dataset
data_fp=fp+'/testdata.xlsx'
dataf=pd.read_excel(data_fp)
#dataf.head()

#getting the column in which you want to remove the keyword
cus_addr_l=dataf['Customer Address'].str.lower().tolist()
#print(cus_addr_l)
def removeKeyword(dataf):
    temp=[]
    #testkey=['ANUPAM', 'NAGAR','society', 'behind','vrajbhumi','amrutnagar']
    key=cleanKeywords(keywords)
    for x in cus_addr_l:
        x=str(x)
        x=x.split()
        resultwords  = [word for word in x if word not in key]
        result = ' '.join(resultwords)
        temp.append(result)
    s=pd.Series(temp)
    dataf['Customer Address']=s
    #dataf['Customer Address']`
    return dataf

dataf=removeKeyword(dataf)
#create a file of csv after remove the keyword
dataf.to_csv(fp+'/afterRemoveKeywords.csv')