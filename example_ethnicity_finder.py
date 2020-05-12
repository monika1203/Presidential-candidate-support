

import pandas as pd
from isys613_project import predict_ethnicity_1, predict_ethnicity_2

names = {
    'lname': ['smith', 'zhang', 'jackson'],
    'fname': ['john', 'wei', 'andrew'] }

df = pd.DataFrame(names)

# Ethnicity ML:
# _1 fucntion uses census data to make its predictions
# _2 function uses Florida voting registration data to make its predictions
#
# ARGUMENTS: (1) DataFrame containing a column of last names
#            (2) The name of the DF column that contains the lastname data
# RETURNS: Pandas DF with 4 columns - asian, black, hispanic, white
#           Values in these cols reflect the estimate of the likelihood that the 
#           name in the corresponding row of original DF is of that ethnicity.
#           Returned DF will have the same row index as the supplied Df
#
et1 = predict_ethnicity_1( df, 'lname')
et2 = predict_ethnicity_2( df, 'lname')

print( et1 )
print( et2 )
