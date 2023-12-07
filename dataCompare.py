import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

st.set_page_config(page_title="Compare CSV",layout="wide")

client,database=st.columns(2)

with client:
    
    client_file=st.file_uploader("Upload Client File")
    if client_file is not None:
        client_df=pd.read_csv(client_file)
        st.dataframe(client_df)


with database:
    database_file=st.file_uploader("Upload your Database")
    if database_file is not None:
        database_df=pd.read_csv(database_file)  
        database_df_head=database_df.head()      
        st.dataframe(database_df)
        


checkCommon=st.button("Check and Download")



if checkCommon:
    if client_df is not None and database_df is not None:

        def calculate_similarity(client_name, database_name):
            return fuzz.ratio(client_name, database_name)
# Initialize empty columns for the client DataFrame
        
        client_df['Similarity Percentage'] = 0
        client_df['Matching Venue Code'] = ''
        client_df['Matching Venue Name'] = ''
        client_df['Matching City'] = ''

# Iterate over rows in the client DataFrame
        for client_index, client_row in client_df.iterrows():
            best_match = None
            max_similarity = 0
    
    # Iterate over rows in the database DataFrame
            for database_index, database_row in database_df.iterrows():
                similarity = calculate_similarity(client_row['Venue Name'], database_row['Venue Name'])

        # Update if a better match is found
                if similarity > max_similarity and similarity > 70:
                    max_similarity = similarity
                    best_match = database_row
    
    # Update the additional columns in the client DataFrame
            client_df.at[client_index, 'Similarity Percentage'] = max_similarity
            client_df.at[client_index, 'Matching Venue Code'] = best_match['Venue Code'] if best_match is not None else ''
            client_df.at[client_index, 'Matching Venue Name'] = best_match['Venue Name'] if best_match is not None else ''
            client_df.at[client_index, 'Matching City'] = best_match['City'] if best_match is not None else ''

# Save the updated client DataFrame to a new CSV file
    st.dataframe(client_df)
    # client_df.to_csv(r'C:\Users\Pravendra Singh\Downloads\test2.csv', index=False)
    
             



