#Data pre-processing data cleaning

import pandas as pd   #handle the dataframe
import re #used for regular expression
from pathlib import Path
print(Path.cwd())  #to show the current working directory


#load csv file
new_csv_file_path="/home/navneet/Documents/companyTask/preprocessing/finalcode"
file_path ="/home/navneet/Documents/companyTask/preprocessing/finalcode/test.csv"
dataf = pd.read_csv(file_path)

#  FUNCTION TO REPLACE VILLAGE OR POST KEYWORD WITH SPACE
def replaceKeywordsWithSpace(dataf):
    for col in dataf:
        dataf[col]= dataf[col].replace('village', " ")
        dataf[col]= dataf[col].replace('post', " ")
        dataf[col]= dataf[col].replace('Village', " ")
        dataf[col]= dataf[col].replace('Post', " ")
        dataf[col]= dataf[col].replace('VILLAGE', " ")
        dataf[col]= dataf[col].replace('POST', " ")
    dataf.update(dataf) 
    return (dataf)

#calling functtion replaceKeywordsWithSpace
#dataf1 = replaceKeywordsWithSpace(dataf)
#print(dataf1)


#step - 2 REMOVE MESSY DATA IN STATE COLUMN AND REPLACE WITH SPACE
ad_l=[]
def removeMessyData(dataf):
    AD=dataf['ADDRESS_LINE'].tolist()
    pattern = r'[^A-Za-z]'   #only the alphabet are allowed in state col
    regex = re.compile(pattern)
    for i in AD:
        ad_l.append(str(regex.sub('',str(i))))
    #REMOVE ANY SINGLE CHAR AND REPLACE WITH SPACE
    s=pd.Series(AD) #convert into series
    s=s.str.replace(r'\b\w\b','').str.replace(r'\s+', ' ') #replace single char with space
    lis_idx=[] #gettin row no. for itirate through every row
    for row in dataf.index:
        lis_idx.append(row)
    new_col= pd.Series(s, name = 'ADDRESS_LINE', index=lis_idx) #update the address_line col with new series value
    dataf.update(new_col)
    return dataf


#dataf2 = removeMessyData(AD)
#print(dataf2)

#remove any alphabet from G-id and Part_id columns
g_id=[]
part_id=[]
def removeAlphabet(dataf):
    G_ID=dataf['G_ID'].tolist()
    PART_ID=dataf['PART_ID'].tolist()
    p = r'[^0-9]'
    regex = re.compile(p)
    for i in G_ID:
        g_id.append(str(regex.sub('',str(i))))
    #print(g_id)    
    for i in PART_ID:
        part_id.append(str(regex.sub('',str(i))))
    #print(part_id)
    '''s_gid=pd.Series(g_id)
    s_id=pd.Series(part_id)
    dataf['G_ID']=s_gid
    dataf['PART_ID']=s_gid
    return dataf'''

#dataf3 = removeAlphabet(dataf)
#print(dataf3)

ad_l1=[]
ad_l2=[]
ad_l3=[]
ad_l4=[]
def removeSpacialChar(dataf):
    AD1=dataf['ADDRESS_LINE1'].tolist()
    AD2=dataf['ADDRESS_LINE2'].tolist()
    AD3=dataf['ADDRESS_LINE3'].tolist()
    AD4=dataf['ADRESS_LINE4'].tolist()

    pattern = r'[^A-Za-z0-9 ]'
    regex = re.compile(pattern)

    for i in AD1:
        ad_l1.append(str(regex.sub('',str(i))))
    #print(lis3)    

    for i in AD2:
        ad_l2.append(str(regex.sub('',str(i))))

    for i in AD3:
        ad_l3.append(str(regex.sub('',str(i))))
        
    for i in AD4:
        ad_l4.append(str(regex.sub('',str(i))))

#remove any alphabet from postcode and strict to length 6
pc_l=[]
def removeAlphabetPostalStrictLength(dataf):
    pc=[]
    dataf['POSTCODE'] = dataf['POSTCODE'].astype(str).str.extract('(\d{6})', expand=False)
    pc=dataf['POSTCODE'].tolist()
    for i in pc:
        pc_l.append(i)
    #dataf.update(dataf)
    #dataf.head(6)



#make a new csv file with cleaned data
def makeNewDataframe(g_id, part_id, ad_l1, ad_l2, ad_l3, ad_l4, ad_l, pc_l):
    new_df=pd.DataFrame({'G_ID':g_id,
                        'PART_ID':part_id,
                        'ADDRESS_LINE1':ad_l1,
                        'ADDRESS_LINE2':ad_l2,
                        'ADDRESS_LINE3':ad_l3,
                        'ADDRESS_LINE4':ad_l4,
                        'ADDRESS_LINE':ad_l,
                        'POSTCODE':pc_l})
    #new_df.head(6)
    #dataf.update(new_df)
    #dataf.head()
    return new_df

def makeNewCsv(new_df, new_csv_file_path):
    new_df.to_csv(new_csv_file_path+"/aftercleaning.csv", index=False, header=True)




#at last calling all the function and get new cleand file
dataf = replaceKeywordsWithSpace(dataf)
dataf = removeMessyData(dataf)
removeAlphabet(dataf)
removeSpacialChar(dataf)
removeAlphabetPostalStrictLength(dataf)
new_df = makeNewDataframe(g_id, part_id, ad_l1, ad_l2, ad_l3, ad_l4, ad_l, pc_l)
#print(new_df)
makeNewCsv(new_df, new_csv_file_path)
