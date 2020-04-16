import pandas as pd 

from isys613_project import predict_gender

df = pd.DataFrame( {
        'fname': ['sue', 'sally', 'john', 'william', 'james' ],
        'lname': ['ligman', 'forth', 'smith', 'hurt', 'jones' ],
    })

# precdict_gender returns a Series object which can be assigned 
# to df as a new column
#

# Gender ML:
# predict_gender fucntion uses NLTK toolkit and a Baysian classifier to 
# make predictions regarding gender based on first names only.
#
# ARGUMENTS: (1) DataFrame containing a column of first names
#            (2) The name of the DF column that contains the first name data
# RETURNS: Pandas Series object that can be assigned to a DF as a new column
#
g = predict_gender( df, 'fname' )
df['gender'] = g
print(df)
