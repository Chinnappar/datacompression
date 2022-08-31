# ------------------------------------------------------------------------------
# Project : The Very First Daisi Hackathon
# File : data_compression.py
# Create on :
# Purpose :
#    This python file is developed for The Very First Daisi Hackathon .
#    This function will compress the csv/json and db table also.
#    I have developed csvfile compression function to compress csv file
# ------------------------------------------------------------------------------
#!/usr/bin/env python
# coding: utf-8

# ------------------------------------------------------------------------------
# Call required packages
# ------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import datetime
from pandas.errors import ParserError
import sys
import zipfile
import streamlit as st
import base64
import time

# ------------------------------------------------------------------------------
## Function Name: file_compress
## Input : mapping and csvfile as a first parameter and 2nd = output file
## This is normal file compression function and this is similar to winzip/7z
# ------------------------------------------------------------------------------
def file_compress(inp_file_names, out_zip_file):
    compression = zipfile.ZIP_DEFLATED
    print(f" *** Input File name passed for zipping - {inp_file_names}")
    print(f' *** out_zip_file is - {out_zip_file}')
    zf = zipfile.ZipFile(out_zip_file, mode="w")

    try:
        for file_to_write in inp_file_names:
            print(f' *** Processing file {file_to_write}')
            zf.write(file_to_write, file_to_write, compress_type=compression)
    except FileNotFoundError as e:
        print(f' *** Exception occurred during zip process - {e}')
    finally:
        zf.close()

# ------------------------------------------------------------------------------
## Function Name: csvfile_compression and Input : Csv file file full path
## To applied 5 different algorithm to compress the csv file
## 1.Mapping for repeated data [completed]
## 2.Group by for repeated data
## 3.Date values convert into epoch format
## 4.Convert Base10 to Base64 for integer Values
## 5.Concatenate all the rows and make it single text [completed]
## final file will be compressed with normal compression function like winzip
# ------------------------------------------------------------------------------
def csvfile_compression(filepath):
    try:
        train_df=pd.read_csv(filepath)
        df_map=[]
        df_col=[]
        key_srtby=""

        for col in train_df.columns:
            col_len=len(train_df[col].unique())
            #print("Column Name:",col,"|Unique Cnt:",col_len,"|DataType:",train_df[col].dtypes,"| DateTime:",datetime.datetime.now())
            if col_len < 2000 :
                if train_df[col].dtypes=='object':
                    try:
                        train_df[col]=pd.to_datetime(train_df[col])
                        train_df[col]=train_df[col].astype(int)
                        #print("Date Column:",col)
                    except (ParserError,ValueError):
                        pass
                    df_col.append(col)
                    df_unique=train_df[col].unique()
                    s=",".join(map(str,df_unique))
                    train_df[col] = train_df[col].replace(df_unique[0:int(col_len/2)],[a for a in range(int(col_len/2))])
                    train_df[col] = train_df[col].replace(df_unique[int(col_len/2)-1:col_len],[a for a in range(int(col_len/2)-1,col_len)])
                elif train_df[col].dtypes=='int64':
                    s="n"
                else: # or train_df[col].dtypes=='float64':
                    s="n"
                df_map.append(s)

        #file_mapping='mapping.txt'
        #with open(file_mapping, 'w') as f:
            #f.write("|".join(df_map))

        df_comp=[]
        for col in train_df.columns:
            s=",".join(map(str,train_df[col]))
            df_comp.append(s)

        #file_compressed='compressed.txt'
        #with open(file_compressed, 'w') as f:
            #f.write("|".join(df_comp))

        df_final="|".join(df_comp)

        #file_name_list = [file_mapping, file_compressed]
        #zip_file_name = filepath+".zip"
        #file_compress(file_name_list, zip_file_name)
        return len(df_final)
    except Exception as ex:
            df=[]
            df.append(ex)
            return df

def data_compression(file):
    train_df=pd.read_csv(file)
    df_map=[]
    df_col=[]
    key_srtby=""

    for col in train_df.columns:
        col_len=len(train_df[col].unique())
        #print("Column Name:",col,"|Unique Cnt:",col_len,"|DataType:",train_df[col].dtypes,"| DateTime:",datetime.datetime.now())

        if col_len < 2000 :
            if train_df[col].dtypes=='object':
                try:
                    train_df[col]=pd.to_datetime(train_df[col])
                    train_df[col]=train_df[col].astype(int)
                    #print("Date Column:",col)
                except (ParserError,ValueError):
                    pass
                df_col.append(col)
                df_unique=train_df[col].unique()
                s=",".join(map(str,df_unique))
                train_df[col] = train_df[col].replace(df_unique[0:int(col_len/2)],[a for a in range(int(col_len/2))])
                train_df[col] = train_df[col].replace(df_unique[int(col_len/2)-1:col_len],[a for a in range(int(col_len/2)-1,col_len)])
            elif train_df[col].dtypes=='int64':
                s="n"
            else:
                s="n"
            df_map.append(s)

    df_comp=[]
    for col in train_df.columns:
        s=",".join(map(str,train_df[col]))
        df_comp.append(s)

    return train_df

def get_table_download_link(df):
    val = to_csv(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Your_File.xlsx">Download Excel file</a>' # decode b'abc' => abc

def s_ui():
    st.set_page_config(layout = "wide")
    st.title("Data Compression")
    st.caption("Data Compression")
    st.info("Developed by Chinnappar & Team (R-Anlytics)")
    st.header("Upload a csv file for data compression")
    csv_file = st.file_uploader("Load your own csv file", type=['csv'], accept_multiple_files=False)

    if csv_file is not None:
        st.text(csv_file)
        df=csvfile_compression(csv_file)
        #df=data_compression(csv_file)
        #st.subheader(msg)
        st.write(df)
        #st.info(msg)
        #st.markdown(get_table_download_link(df), unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Call main function using csv file as a input
# This main function is used for testing purpose in local
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        #csvfile_compression('training_data_sales_10k.csv')
        s_ui()
        print("compression is completed...")
    except Exception as msg:
        print(f'''Error {msg}''')
