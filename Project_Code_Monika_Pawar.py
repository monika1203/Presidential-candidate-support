

## Import Statements
import requests
from requests.exceptions import HTTPError
import pandas as pd
import json
from isys613_project import predict_ethnicity_1, predict_ethnicity_2, predict_gender



## 1.Get the Candidate's Id via FEC open candidate API.

## Here is the data source url we are intrested in
FEC_URL = 'https://api.open.fec.gov/v1/candidates/search/?'

## The API key got from https://api.data.gov/signup
API_KEY = 'ymQSJL8G3Hbrl6o5pbha3imqmmKUbcnYMgW3AeCx'

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    }

parameters = {
    'name':'Booker, Cory',
    'party':'DEM',
    'api_key': API_KEY,
    'election_years': '2020',
    'candidate_status': 'C'
}

## Using try and except block to catch and handle exceptions 

try:
    response = requests.get(FEC_URL, params = parameters,headers = headers)
    ## If the response was successful, no Exception will be raised
    ## by the following line
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
else:
    print('Success!')


## Deserialize the JSON payload
json_data = response.json()
json_data_dict = json.dumps(json_data, indent = 4)

##---------------------------Output of response.json---------------------------
#print(f'The ouput of json response: {json_data_dict}')
##-----------------------------------------------------------------------------

for value in json_data['results']:
    if value['office_full'] == 'President':
        candidate_id = value['candidate_id']
        
##---------------------------Output for Candidate's Id-------------------------
print(f'Candidate Id: {candidate_id}')
##-----------------------------------------------------------------------------

## 2. Locating my candidate’s official presidential committee id by using 
##candidate’s id to filter the committee master data (provided as a delimited file).


header_file = pd.read_csv('cm_header_file.csv')
cm20_df = pd.read_csv('cm20.txt', sep='|', names = header_file)

## verifying few rows from cm20_df dataframe
#print(cm20_df.head(5))

presidential_committee_id= cm20_df[cm20_df['CAND_ID'] == candidate_id]['CMTE_ID'].item()


##-----------------Output for presidental committee Id-------------------------
print(f'Official presidental committee id for candidate is {presidential_committee_id}')
##-----------------------------------------------------------------------------


## 3.Isolating all the individual contributions to my candidate’s official presidential 
## committee by filtering the data file (Contributions by Individuals)
## provided as two delimited file, based on my candidate’s presidential committee id.


header_file1 = pd.read_csv('indiv_header_file.csv')

indiv_contributor_f1 = pd.read_csv('itcont_2020_20190629_20190908.txt',\
                                   sep='|', names = header_file1, parse_dates=True, low_memory = False)

indiv_contributor_f2 = pd.read_csv('itcont_2020_20190909_20191120.txt',\
                                   sep='|', names = header_file1, parse_dates=True, low_memory = False)

## Verifying few rows from indiv_contributor_f1,indiv_contributor_f2  dataframes
#print(indiv_contributor_f1.head(5))
#print(indiv_contributor_f2.head(5))

## Retaining only requried attributes along with recommended datatypes.
column_dict = {'CMTE_ID' :str,'TRANSACTION_PGI':str,'ENTITY_TP':str,
               'NAME':str, 'CITY':str,'STATE':str, 'ZIP_CODE':str, 
               'OCCUPATION':str,'TRANSACTION_DT':str, 'TRANSACTION_AMT':float } 

contributor_f1_df = indiv_contributor_f1[column_dict.keys()]
contributor_f2_df = indiv_contributor_f2[column_dict.keys()]

contributor_f1_df = contributor_f1_df.astype(column_dict) 
contributor_f2_df = contributor_f2_df.astype(column_dict)

## Verifying the datatypes and size for the contributors file.
#print("\nsize of the data frame (contributor_f1_df):",contributor_f1_df.shape)
#print(contributor_f1_df.dtypes)
#print(contributor_f1_df.head(2))
#print("\nsize of the data frame (contributor_f2_df):",contributor_f2_df.shape)
#print(contributor_f2_df.dtypes)
#print(contributor_f2_df.tail(2))

## Combining the independent contributor's data from both dataframes.
combined_indiv_contr_df = pd.DataFrame()
combined_indiv_contr_df = contributor_f1_df.append(contributor_f2_df,ignore_index = True,sort = False)

## Verifying few rows from combined contributors dataframe.
#print("\nsize of the data frame (combined_indiv_contr_df):",combined_indiv_contr_df.shape)
#print(combined_indiv_contr_df.head(2))
#print(combined_indiv_contr_df.tail(2))

## 4. Restricting Rows Using Filters
## Filtering  the individual contributions data based on the following criteria

## a) Contributions made during the month of September year of 2019

combined_indiv_contr_df=combined_indiv_contr_df[combined_indiv_contr_df['TRANSACTION_DT'].str.match(r'9[0-9][0-9]2019')]
##-----------------Verifying the Output result---------------------------------
#print(combined_indiv_contr_df)

## b) Your candidate’s presidential committee id

combined_indiv_contr_df=combined_indiv_contr_df[combined_indiv_contr_df['CMTE_ID'] == presidential_committee_id]
##------------------------Verifying the Output result---------------------------
#print(Ccombined_indiv_contr_df)

## c) Transaction amounts > 0

combined_indiv_contr_df= combined_indiv_contr_df[combined_indiv_contr_df['TRANSACTION_AMT'] >0]
##------------------------Verifying the Output result--------------------------
#print(combined_indiv_contr_df)

## d) Contributions made by entities of type individual

combined_indiv_contr_df = combined_indiv_contr_df[combined_indiv_contr_df['ENTITY_TP'] == 'IND']
##------------------------Verifying the Output result--------------------------
#print(combined_indiv_contr_df)


## 5. Creating a dataframe with First and last name of the contributors.

splitted = combined_indiv_contr_df['NAME'].str.split(',', expand = True)
combined_indiv_contr_df['Last_Name'] = splitted[0]
combined_indiv_contr_df['Last_Name'] = combined_indiv_contr_df['Last_Name'].str.strip()
combined_indiv_contr_df['First_Name'] = splitted[1]
combined_indiv_contr_df['First_Name'] = combined_indiv_contr_df['First_Name'].str.strip()
combined_indiv_contr_df['First_Name'] = combined_indiv_contr_df['First_Name'].str.replace(r'\s\w\.',"")
##------------------------Verifying the Output result--------------------------
#print(combined_indiv_contr_df)


## 6. Ethnicity Classification:

ethnicity_1 = predict_ethnicity_1(combined_indiv_contr_df, 'Last_Name')
ethnicity_2 = predict_ethnicity_2(combined_indiv_contr_df, 'Last_Name')
##------------------------Verifying the Output result--------------------------
#print( ethnicity_1 )
#print( ethnicity_2 )


## Computing the Average ethinicity based on result of the two (ethnicity_1,ethnicity_2) dataframe

ethnicity_2.rename(columns={'asian':'asian_2','black':'black_2','hispanic':'hispanic_2', 'white':'white_2'}, inplace = True)
#print(ethnicity_2.head(2))


concated_ethinicity_df = pd.concat([ethnicity_1, ethnicity_2], axis=1)
#print(concated_ethinicity_df.head(2))

Avg_ethinicity = pd.DataFrame()

Avg_ethinicity['Asian'] = concated_ethinicity_df[['asian','asian_2']].mean(axis=1,skipna = True)
Avg_ethinicity['Black'] = concated_ethinicity_df[['black','black_2']].mean(axis=1,skipna = True)
Avg_ethinicity['Hispanic'] = concated_ethinicity_df[['hispanic','hispanic_2']].mean(axis=1,skipna = True)
Avg_ethinicity['White'] = concated_ethinicity_df[['white','white_2']].mean(axis= 1,skipna = True)

#print(Avg_ethinicity)

## Defining the function to assign each observation to single ethinicity category
## if average ethinicity is greater than .50

def category(row):
    if row['Asian'] > 0.50:
        return 'asian'
    if row['Black'] > 0.50:
        return 'black'
    if row['Hispanic'] > 0.50:
        return 'hispanic'
    if row['White'] > 0.50:
        return 'white'
    return 'unknown'


combined_indiv_contr_df['Category'] = Avg_ethinicity.apply(lambda row: category(row), axis = 1)
##-----------------Output for Ethnicity Classification-------------------------
#print(f'{combined_indiv_contr_df}')
##-----------------------------------------------------------------------------

## 7. Gender Classification:

gender_classification = predict_gender(combined_indiv_contr_df, 'First_Name')
combined_indiv_contr_df['Gender'] = gender_classification
#-----------------Output for Gender Classification----------------------------
#print(f'{combined_indiv_contr_df.head(10)}')
print("\nSize of the data frame (combined_indiv_contr_df):",combined_indiv_contr_df.shape)

#export_csv = combined_indiv_contr_df.to_csv('Ethinicty$Gender_Output.csv')
#-----------------------------------------------------------------------------


# Analysis - Proof of Concept:

## Question 1: How many male and female Contributor supported the candidate?

Gender_count = combined_indiv_contr_df.groupby('Gender')['CMTE_ID'].count().reset_index(name='Total_Count')
print(f'\nThe total number of male and female contributors:')
print(Gender_count)


## Question 2: How much transaction amount each ethnicity category has raised for the candidate?

Category_Contribution = combined_indiv_contr_df.groupby('Category')['TRANSACTION_AMT'].sum().reset_index(name='Total_Transaction_amount').sort_values(by='Total_Transaction_amount', ascending=False).reset_index(drop=True)
print(f'\nThe Total transaction amount contribution made by each ethinicity category:')
print(Category_Contribution)


## Question 3: Which states are the Top 10 highest contributors for the candidate?

STATE_Contribution = combined_indiv_contr_df.groupby('STATE')['TRANSACTION_AMT'].sum().reset_index(name='Total_Transaction_amount').sort_values(by='Total_Transaction_amount', ascending=False).reset_index(drop=True).head(10)
print(f'\nThe Top 10 state"s total transaction amount contribution:')
print(STATE_Contribution)

## Question 4: Which Occupation type are the Top 5 highest contributors for the candidate?

Occupation_Contribution = combined_indiv_contr_df.groupby('OCCUPATION')['TRANSACTION_AMT'].sum().reset_index(name='Total_Transaction_amount').sort_values(by='Total_Transaction_amount', ascending=False).reset_index(drop=True).head(5)
print(f'\nThe Top 5 Occupation total transaction amount contribution:')
print(Occupation_Contribution)


## Question 5:What is the count for each ethnicity category according to the Gender? 

Ethinicity_by_Gender_count = combined_indiv_contr_df.groupby(['Gender','Category'])['CMTE_ID'].count()
print(f'\nEach ethinicity category count according to the gender:')
print(Ethinicity_by_Gender_count )
