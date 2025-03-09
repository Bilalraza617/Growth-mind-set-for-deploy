import streamlit as st
import pandas as pd
import os 
from io import BytesIO


# Set page configuration
st.set_page_config(page_title="Bilal" ,layout="wide")

# Add a title
st.title("Data sweeper")

# Add a description
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization")

# File uploader
uploaded_files = st.file_uploader("Upload you files (CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df=pd.read_csv(file)
        elif file_ext == ".xlsx":       
            df = pd.read_excel(file)
        else: 
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display info about the file
        st.write(f"**File Nmae:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        # Show 5 rows of df 
        st.write("Preview teh Head of the Dataframe")
        st.dataframe(df.head())

        #Options for data cleaning
        st.subheader("Dara Cleaning options")
        if st.checkbox(f"Clean Data for : {file.name}"):
            col1,col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill missing Valuse for {file.name}"):
                    numeric_col = df.select_dtypes(include=["number"]).columns
                    df[numeric_col] = df[numeric_col].fillna(df[numeric_col].mean())
                    st.write("Fill missing values")

        #Specific col
        st.subheader("Select Colums to Convert")
        colums = st.multiselect(f"Choose Colums for {file.name}", df.columns , default=df.columns)
        df = df[colums]

        #create some visualixations
        st.subheader("👓 Data Visualiaztion")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

        #Convert the File -> CSV to Excel
        st.subheader("🎗Convertion Options")
        convertion_type = st.radio(f"Convert {file.name} to:",["CSV","Excel"], key=file.name)
        if st.button(f'Convert {file.name}'):
            buffer = BytesIO() 
            if convertion_type == "CSV":
              df.to_csv(buffer,index=False)
              file_name = file.name.replace(file_name,"CSV")
              mime_type = "text/csv"
            elif convertion_type == "Excel":
                df.to_excel(buffer,index=False)
                file_name = file.name.replace(file_ext,"xlsx")
                mime_type = "application/vnd.openxmlformatts-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #Download Button 
            st.download_button(
                label=f"Download {file.name} as {convertion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

            st.success("🎉 All file processed")
