import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title = "Data Sweeper", page_icon="🧹",layout='wide')
st.title("Data Sweeper")

# custom css
st.markdown(
    """
    <style>
    .stAPP{background-color: black; color: white;}
    </style>
    """,
    unsafe_allow_html=True
)
# title and description
st.title("📀 Data Sweeper Sterling Integeration by Mujahid Shaikh")
st.write("Transform your files between CSV and Excel formats. Clean up your data and make it ready for analysis.")

# upload file
uploaded_files = st.file_uploader("upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlxs":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue

        # file details
        st.write("🔍 Preview the head of the DataFrame:")
        st.dataframe(df.head())

        #data cleaning options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed successfully")

            with col2:
                if st.button(f"Fill missing values in the file : {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values filled successfully")

        st.subheader("🎯 Select Columns to Keep")
        columns =st.multiselect("Select columns for {file.name}". df.columns, default=df.columns)
        df = df[columns]

        #data visulization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        #conversion options
        st.subheader("🔄 Conversion Options")
        conversion_format = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_format == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_format == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_format}", 
                data=buffer, 
                file_name=file_name, 
                mime=mime_type
            )

st.success("🎉File conversion completed!")
