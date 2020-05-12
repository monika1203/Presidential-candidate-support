# presidential-candidate-support-Analysis

For a given 2020 Democratic Party presidential candidate, characterize their support from (a) a gender perspective and (b) an ethnicity perspective?

### Project Data Sources
Data for this project will be taken from data sources derived or directly captured from the United States Federal Election Commission (FEC). (https://www.fec.gov/data/browse-data/?tab=bulk-data) The objective is to build a dataframe suitable for answering our research question. Our dataframe will include data regarding individual financial contributes to candidates as reported in the FEC Individual Contributions File. We will also be required to impute the race and gender of individual financial donors and thus, dataframe will also include imputed gender and ethnicity data.<br>

#### Federal Election Commission (FEC) Data
Individual contributions are linked to presidential committees, not to candidates. A single presidential committee is officially “linked” to (registered by) each presidential candidate. These presidential committees are directly related to their candidates via the CAND_ID attribute located in the Committee Master File. For this project, we are only interested in contributions made to a candidate’s presidential committee.
All information regarding the FEC data used in this project can be reviewed at the following URL. https://www.fec.gov/data/browse-data/?tab=bulk-data. Completion the steps below will require to utilize the information provided in several of the documents and/or data sources available from that URL.

Objective is to construct a dataframe containing information about individual contributions to candidate’s presidential committee. 
<br> 
1. Locate your candidate’s unique FEC candidate id via the FEC Open Candidate API.<br>
2. Locate your candidate’s official presidential committee id by using your candidate’s id to filter the committee master data (provided as a delimited file).<br>
3. Isolate all the individual contributions to your candidate’s official presidential committee (and hence your candidate) by filtering the Contributions by Individuals data (provided as two delimited files) based on your candidate’s presidential committee id.<br>

#### FEC Open Candidate API
To use the FEC API to locate the candidate ID for your candidate. To do so, need an API key for https://api.data.gov.  We can get an API key at https://api.data.gov/signup. The key will be provided immediately.
Data Source URL: https://api.open.fec.gov/developers/#/candidate

#### Committee Master File
The committee master file contains basic information for each committee registered with the Federal Election Commission, including:
 Federal political action committees and party committees <br> 
 Campaign committees for presidential, house, and senate candidates <br> 
 Groups or organizations spending money for or against candidates for federal office <br> 
The file has one record per committee and shows the committee identification number, committee name, sponsor (when appropriate), treasurer name, committee address, information about the type of committee, and the candidate identification number (for campaign committees

### Data Source File Name: cm20.txt 
The FEC provides this data in a single file. The delimited file does not contain header rows. So, need to use a separately provided header file to assign a column index for committee master dataframe.<br> 

Header File: https://www.fec.gov/files/bulk-downloads/data_dictionaries/cm_header_file.csv

Objective in working with the committee master file is to find candidate’s official presidential committee id.

### Individual Contributions File
The individual contributions file contains each contribution from an individual to a federal committee if the contribution was at least $200. It includes the ID number of the committee receiving the contribution, the name, city, state, zip code, and place of business of the contributor along with the date and amount of the contribution.

### Data Source Files: itcont_2020_20190629_20190908.txt and itcont_2020_20190909_20191120.txt. 
The FEC provides this data in separate files named for the date ranges contained within the file. The two delimited files do not contain header rows.

Header File: https://www.fec.gov/files/bulk-downloads/data_dictionaries/indiv_header_file.csv

Restricting Rows Using Filters
Filter the individual contributions data based on the following criteria: <br>
1. Contributions made during the month of September year of 2019 <br>
2. Your candidate’s presidential committee id <br>
3. Transaction amounts > 0 <br>
4. Contributions made by entities of type individual <br>

Ethnicity Classification (Based on ethnicolr module): In the ethnicity and gender classification requirements that follow, need access to contributors first and last names <br>
<br> 1. The isys613_project module depends on the ethnicolr module.<br>

(NOTE: classify each observation as belonging to one of the four ethnicities. For each observation, you are to compute the average ethnicity likelihood by ethnicity based on the results of the two estimation methods. This will yield one average estimate for each of the four ethnicities.
assign each observation to a single ethnicity category if the average ethnicity likelihood exceeds .50. If no average ethnicity estimate exceeds .50 then, assign the observation to the ‘unknown’ ethnicity category. Incorporate your ethnicity category attribute into dataframe)

Gender Classification : In this step will be using the given name (first name) from FEC dataframe to impute the gender of individual contributors, again be importing the isys613_project module.<br>

(NOTE:The predict_gender function returns a pandas Series which is conformed to the source input dataframe. The returned Series contains the results of a naïve Bayesian gender classification model.)

#### Analysis – Proof of Concept
Once you have completed construction of your dataframe, you are to conduct some very cursory analysis of your results. You can explore your data using several reducing/aggregation functions such as counts, means, etc. There a several interesting categorical variables by which you could evaluate your data including gender, ethnicity, city, state, occupation, day, etc.
