import pandas as pd
import numpy as np
from pathlib import Path
print(Path.cwd())

input_file_path='/home/navneet/Documents/companyTask/accuracy/finalAccuracy/py/testaccu.csv'
df = pd.read_csv(input_file_path)
df=df.astype(str) #convert all data into string for accurate matching


#function to Add columns into new dataframe 
def makeNewDataframe():

    col=['inputpincode = geocodepincode',
        'inputcity = geocodecity',
        'firstword = inputcity',
        'inputpincode = spatialpincode',
        'inputcity = spatialcityname164',
        'inputcity = spatialcitynamegeoexpansion',
        'inputstate = spatialstate',
        ]
    new_df= pd.DataFrame(columns=col)
    return new_df

new_df = makeNewDataframe()

#function to calculate matching between columns of input df and store the true false in new_df:
def trueFalseAccordingCondition(new_df, df):

    T='true'
    F='false'
    new_df['inputpincode = geocodepincode']=np.where(df['Input Pincode'] == df['Geocoded Pincode'],T,F)
    new_df['inputcity = geocodecity']=np.where(df['Input City'] == df['Geocoded City'],T,F)
    new_df['firstword = inputcity']=np.where(df['first word'] == df['Input City'],T,F)
    new_df['inputpincode = spatialpincode']=np.where(df['Input Pincode'] == df['Spatial Pincode'],T,F)
    new_df['inputcity = spatialcityname164']=np.where(df['Input City'] == df['SpatialCityName164'],T,F)
    new_df['inputcity = spatialcitynamegeoexpansion']=np.where(df['Input City'] == df['SpatialCityNameGeoexpansion'],T,F)
    new_df['inputstate = spatialstate']=np.where(df['Input State'] == df['Spatial State'],T,F)
    return new_df

new_df = trueFalseAccordingCondition(new_df, df)

#now a new dataframe is created with true false value according to condition
#assign new_df to tf_df(truefalse dataframe) and chnage its data value to str type 
tf_df=new_df
tf_df.astype(str)


#function for merg input dataframe with truefalse data frame
#and store into another csv file
def mrgInputTfDataframe(df, tf_df):
    inp_tf_df=df.join(tf_df)
    inp_tf_df.to_csv('/home/navneet/Documents/companyTask/accuracy/finalAccuracy/py/input_true_false.csv')
    return inp_tf_df
#make new dataframe conditionwise
#gcon1- > geocondition1, gspcon -> geocode and spatial contion likewise
def makeConditionalDataframe(df):

    col1=['gcon1','gcon2','spcon1','spcon2','gspcon1','gspcon2','gsp2con1','gsp2con2','gpcon1','gpcon2','gfalse1',
      'gfalse2','match']
    con_df=pd.DataFrame(columns=col1) #dataframe is created with above col name
    con_df['match']=df['Match_types'] #put the match value of input datframe into con_df match col
    return con_df

con_df=makeConditionalDataframe(df)

def checkForCondition(tf_df,con_df):
    #geocode condition
    #1.GEOCODED CONDITIONS - TRUE
    #check for condition true store it into conditional dataframe
    condition1=[
        (tf_df['inputpincode = geocodepincode'].str.lower() == 'true' ) & 
        (tf_df['inputcity = geocodecity'].str.lower() == 'true') & 
        (tf_df['firstword = inputcity'].str.lower() == 'true')
        ]
    choice1=['true']
    con_df['gcon1'] = np.select(condition1, choice1,default='false')
    #2.GEOCODED CONDITIONS - TRUE
    condition2=[(tf_df['inputpincode = geocodepincode'].str.lower() == 'true') &
            (tf_df['inputcity = geocodecity'].str.lower() == 'true')
            ]
    choice2=['true']
    con_df['gcon2'] = np.select(condition2, choice2,default='false')
    #SPATIAL CONDITIONS - TRUE
    #3 SPATIAL CONDITIONS - TRUE
    condition3=[
        (tf_df['inputpincode = spatialpincode'].str.lower() == 'true' ) & 
        (tf_df['inputcity = spatialcityname164'].str.lower() == 'true') | 
        (tf_df['inputcity = spatialcitynamegeoexpansion'].str.lower() == 'true') &
        (tf_df['firstword = inputcity'].str.lower() == 'true')
        ]
    choice3=['true']
    con_df['spcon1'] = np.select(condition3, choice3,default='false')
    #4 SPATIAL CONDITIONS - TRUE
    condition4=[(tf_df['inputpincode = spatialpincode'].str.lower() == 'true' ) & 
        (tf_df['inputcity = spatialcityname164'].str.lower() == 'true') | 
        (tf_df['inputcity = spatialcitynamegeoexpansion'].str.lower() == 'true')
            ]
    choice4=['true']
    con_df['spcon2'] = np.select(condition4, choice4, default='false')
    #GEOCODED & SPATIAL CONDITIONS – GEOCODED PINCODE TO SPATIAL CITY - TRUE
    #5GEOCODED & SPATIAL CONDITIONS
    condition5=[
        (tf_df['inputpincode = geocodepincode'].str.lower() == 'true' ) & 
        (tf_df['inputcity = spatialcityname164'].str.lower() == 'true') | 
        (tf_df['inputcity = spatialcitynamegeoexpansion'].str.lower() == 'true') &
        (tf_df['firstword = inputcity'].str.lower() == 'true')
        ]
    choice5=['true']
    con_df['gspcon1'] = np.select(condition5, choice5,default='false')
    #6GEOCODED & SPATIAL CONDITIONS
    condition6=[(tf_df['inputpincode = geocodepincode'].str.lower() == 'true' ) & 
        (tf_df['inputcity = spatialcityname164'].str.lower() == 'true') | 
        (tf_df['inputcity = spatialcitynamegeoexpansion'].str.lower() == 'true')
            ]
    choice6=['true']
    con_df['gspcon2'] = np.select(condition6, choice6,default='false')
    #GEOCODED & SPATIAL CONDITIONS – GEOCODED CITY TO SPATIAL PINCODE - TRUE
    #1 GEOCODED CITY TO SPATIAL PINCODE 
    condition7=[
        (tf_df['inputcity = geocodecity'].str.lower() == 'true' ) & 
        (tf_df['inputpincode = spatialpincode'].str.lower() == 'true') &
        (tf_df['firstword = inputcity'].str.lower() == 'true')
        ]
    choice7=['true']
    con_df['gsp2con1'] = np.select(condition7, choice7,default='false')
    #2 GEOCODED CITY TO SPATIAL PINCODE 
    condition8=[(tf_df['inputcity = geocodecity'].str.lower() == 'true' ) & 
        (tf_df['inputpincode = spatialpincode'].str.lower() == 'true') ]
    choice8=['true']
    con_df['gsp2con2'] = np.select(condition8, choice8, default='false')
    #GEOCODED PINCODE - TRUE
    #3GEOCODED PINCODE
    condition9=[
        (tf_df['inputpincode = geocodepincode'].str.lower() == 'true' ) & 
        (tf_df['firstword = inputcity'].str.lower() == 'true')
        ]
    choice9=['true']
    con_df['gpcon1'] = np.select(condition9, choice9,default='false')
    #4GEOCODED PINCODE
    condition10=[(tf_df['inputpincode = geocodepincode'].str.lower() == 'true' )]
    choice10=['true']
    con_df['gpcon2'] = np.select(condition10, choice10,default='false')
    #GEOCODED CONDITIONS – FALSE
    #5GEOCODED CONDITIONS – FALSE
    tf_df['PD']=df['PincodeDistance']
    condition11=[(tf_df['PD'].astype(float) > -2 ) & (tf_df['PD'].astype(float) < +2 ) & 
        (tf_df['inputpincode = geocodepincode'].str.lower() == 'false' ) & 
        (tf_df['firstword = inputcity'].str.lower() == 'true')
        ]
    choice11=['true']
    con_df['gfalse1'] = np.select(condition11, choice11,default='false')
    #5GEOCODED CONDITIONS – FALSE
    condition12=[(tf_df['PD'].astype(float) > -2 ) & (tf_df['PD'].astype(float) < +2 ) &
                (tf_df['inputpincode = geocodepincode'].str.lower() == 'false' )
                ]
    choice12=['true']
    con_df['gfalse2'] = np.select(condition12, choice12,default='false')
    return con_df

con_df=checkForCondition(tf_df, con_df)

def cheeckForKeyword(con_df):
    #check for keywords acc geocond2 a , b , c, d
    #check for keywords acc geocond1 a
    m=con_df['match']  #extrcat the match series from con_df used for keyword matching
    #keyword geocondition 1
    gka1='political'
    gka2='administrative'
    gka3='pincode'
    #emptylist
    gk1a=[]
    #check if any keyword exist in match col and store the true false in empty list
    for i in m:
        if((gka1 in str(i)) or (gka2 in str(i)) or (gka3 in str(i))):
            gk1a.append('true')
        else:
            gk1a.append('false')
    #covert list into series
    gk1a=pd.Series(gk1a)
    #make a gk1a column and store the series into it
    con_df['gk1a']=gk1a
    
    #keyword spatialcondition1
    ska1='political'
    ska2='administrative'
    ska3='postalcode'
    #emptylist
    sk1a=[]
    for i in m:
        if((ska1 in str(i)) or (ska2 in str(i)) or (ska3 in str(i))):
            sk1a.append('true')
        else:
            sk1a.append('false')
    sk1a=pd.Series(sk1a)
    con_df['sk1a']=sk1a
    #for geocondition (a) keywords
    ka1='establishment'
    ka2='premise'
    ka3='subpremise'

    k2a=[]
    for i in m:
        if((ka1 in str(i)) or (ka2 in str(i)) or (ka3 in str(i))):
            k2a.append('true')
        else:
            k2a.append('false')
            
    k2a=pd.Series(k2a)
    con_df['k2a']=k2a
    #for geocondition (b) keywords   
    k2b=[]
    kb1='street' 
    kb2='intersection'
    kb3='route'
    kb4='town_square'
    for i in m:
        if((kb1 in str(i)) or (kb2 in str(i)) or (kb3 in str(i)) or (kb4 in str(i))):
            k2b.append('true')
        else:
            k2b.append('false')
    k2b=pd.Series(k2b)
    con_df['k2b']=k2b
    #for geocondition (c) keywords 
    k2c=[]
    kc1='locality' 
    kc2='political'
    kc3='administrative'
    for i in m:
        if((kc1 in str(i)) or (kc2 in str(i)) or (kc3 in str(i))):
            k2c.append('true')
        else:
            k2c.append('false')

    k2c=pd.Series(k2c)
    con_df['k2c']=k2c
    #for geocondition (d) keywords
    k2d=[]
    kd1='postalcode'
    for i in m:
        if((kd1 in str(i))):
            k2d.append('true')
        else:
            k2d.append('false')
            
    k2d=pd.Series(k2d)
    con_df['k2d']=k2d

    kgf1a=[]
    kgf1='administrative'
    for i in m:
        if((kgf1 in str(i))):
            kgf1a.append('true')
        else:
            kgf1a.append('false')
    kgf1a=pd.Series(kgf1a)
    con_df['kgf1a']=kgf1a
    kgf1a=[]
    kgf1='administrative'
    for i in m:
        if((kgf1 in str(i))):
            kgf1a.append('true')
        else:
            kgf1a.append('false')        
    kgf1a=pd.Series(kgf1a)
    con_df['kgf1a']=kgf1a
    kgf1b=[]

    kgf2='political'
    for i in m:
        if((kgf2 in str(i))):
            kgf1b.append('true')
        else:
            kgf1b.append('false')
            
    kgf1b=pd.Series(kgf1b)
    con_df['kgf1b']=kgf1b
    return con_df

con_df=cheeckForKeyword(con_df)

#add accuracy column in con_df dataframe and assign it to test dataframe
con_df['accuracy']=''
test=con_df

def checkConditionStoreValueInAccuracy(test):
    #put the value in accuracy column according to 1.GEOCODED CONDITIONS - TRUE 1 & 2
    for i in test.index:
        if(str(test.at[i,'gcon1']) == str(test.at[i,'gk1a']) == 'True'):
            test.at[i, 'accuracy']='pincode'  
        elif(str(test.at[i,'gcon2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='rooftop'
        elif(str(test.at[i,'gcon2']) == str(test.at[i,'k2b']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='street'
        elif( (str(test.at[i,'gcon2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='locality'
        elif( (str(test.at[i,'gcon2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='pincode'   
    
    #put the value in accuracy column according to GEOCODED & SPATIAL CONDITIONS – GEOCODED PINCODE TO SPATIAL CITY - TRUE 5 & 6
        elif(str(test.at[i,'gspcon1']) == str(test.at[i,'gk1a']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='pincode'  
        elif(str(test.at[i,'gspcon2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='rooftop'
        elif(str(test.at[i,'gspcon2']) == str(test.at[i,'k2b']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='street'
        elif( (str(test.at[i,'gspcon2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='locality'
        elif( (str(test.at[i,'gspcon2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='pincode'
    
    #put the value in accuracy column according to GEOCODED & SPATIAL CONDITIONS – GEOCODED PINCODE TO SPATIAL CITY - TRUE 5 & 6
        elif(str(test.at[i,'gsp2con1']) == str(test.at[i,'gk1a']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='pincode'  
        elif(str(test.at[i,'gsp2con2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='rooftop'
        elif(str(test.at[i,'gsp2con2']) == str(test.at[i,'k2b']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='street'
        elif( (str(test.at[i,'gsp2con2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='locality'
        elif( (str(test.at[i,'gsp2con2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='pincode'
    
    #GEOCODED PINCODE - TRUE 3,4
        elif(str(test.at[i,'gpcon1']) == str(test.at[i,'gk1a']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='pincode'  
        elif(str(test.at[i,'gpcon2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='rooftop'
        elif(str(test.at[i,'gpcon2']) == str(test.at[i,'k2b']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='street'
        elif( (str(test.at[i,'gpcon2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='locality'
        elif( (str(test.at[i,'gpcon2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='pincode'

    #GEOCODED CONDITIONS – FALSE 5,6
    #Set filter on pincode distance column – Range +2 to -2 – Check with +1 to -1
    for i in test.index:
        if(str(test.at[i,'gfalse1']) == str(test.at[i,'kgf1a']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='city'  
        elif(str(test.at[i,'gfalse2']) == str(test.at[i,'kgf1b']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='locality'
        elif(str(test.at[i,'gfalse2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='rooftop'
        elif( (str(test.at[i,'gfalse2']) == str(test.at[i,'k2b']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='street'
        elif( (str(test.at[i,'gfalse2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='locality'
        elif( (str(test.at[i,'gfalse2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
            test.at[i, 'accuracy']='regeocode'
        else:
            test.at[i, 'accuracy']=''
    
    return test 

test = checkConditionStoreValueInAccuracy(test)

#function to  merg input data + truefalse + Accuracy
def mrgInputTrueFalseWithAccuracy(inp_tf_df, test):
    #mrg input dataset + trueFalse + Accuracy
    #inp_tf_df.head()
    inp_tf_df['accuracy']=test['accuracy']
    return inp_tf_df

inp_tf_df = mrgInputTfDataframe(df, tf_df)
finaldata = mrgInputTrueFalseWithAccuracy(inp_tf_df, test)

#function to make final csv file
def makefinalcsv(finaldata):
    finaldata.to_csv('/home/navneet/Documents/companyTask/accuracy/finalAccuracy/py/finaldata.csv')

makefinalcsv(finaldata)  

#at the end you have a csv file with final output in accuracy column in your defined directory 