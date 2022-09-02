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
import os
import math
pd.options.mode.chained_assignment = None  # default='warn'

# ------------------------------------------------------------------------------
# -- UDF's --
# ------------------------------------------------------------------------------
def convert_bytes(size):
    for x in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

def file_size(file):
    if os.path.isfile(file):
        file_info = os.stat(file)
        return convert_bytes(file_info.st_size),file_info.st_size

def listToDict(b):
    s = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/'
    if b=="b":
        return {s[i]:i for i in range(len(s))}
    else:
        return {i:s[i] for i in range(len(s))}

def base64_to_base10(b64dec):
    conversion_table = listToDict("b")
    decimal = 0
    power = len(b64dec) -1
    for digit in b64dec:
        decimal += conversion_table[digit]*64**power
        power -= 1
    return decimal

def base10_to_base64(decimal):
    conversion_table = listToDict("d")
    remainder=0
    b64dec = ''
    while(decimal > 0):
        remainder = decimal % 64
        b64dec = conversion_table[remainder] + b64dec
        decimal = decimal // 64

    return b64dec

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
        #msg="Source file's size:"+str(train_df.size)
        df_map=[]
        df_col={col:len(train_df[col].unique()) for col in train_df.columns}
        df_dt=[train_df[col].dtypes for col in train_df.columns ]
        key_srtby=""

        for col in train_df.columns:
            col_len=len(train_df[col].unique())
            #print("Column Name:",col,"|Unique Cnt:",col_len,"|DataType:",train_df[col].dtypes,"| DateTime:",datetime.datetime.now())
            if col_len < 2000 :
                df_unique=train_df[col].unique()
                s=",".join(map(str,df_unique))
                train_df[col] = train_df[col].replace(df_unique[0:int(col_len/2)],[a for a in range(int(col_len/2))])
                train_df[col] = train_df[col].replace(df_unique[int(col_len/2)-1:col_len],[a for a in range(int(col_len/2)-1,col_len)])
                train_df[col] = train_df[col].apply(lambda x: x if np.isnan(x) else base10_to_base64(int(x)))
            elif train_df[col].dtypes=='int64':
                #print("Base64 Conversion...",train_df[col].dtypes)
                train_df[col] = train_df[col].apply(lambda x: x if np.isnan(x) else base10_to_base64(int(x)))
                s="b"
            elif train_df[col].dtypes=='object':
                try:
                    train_df[col] = pd.to_datetime(train_df[col]).view(int) // 10 ** 9
                    train_df[col] = train_df[col].apply(lambda x: x if np.isnan(x) else base10_to_base64(int(x)))
                    #print("Date Column:",col)
                    s="d"
                except (ParserError,ValueError):
                    pass
            elif train_df[col].dtypes=='float64':
                #train_df[col] = train_df[col].apply(lambda x: x if np.isnan(x) else str(base10_to_base64(int(str(x).split(".")[0]))+"."+base10_to_base64(int(str(x).split(".")[1]))))
                s="f"
            else: # or train_df[col].dtypes=='float64':
                s="n"
            df_map.append(s)
        df_map.append(str(df_col))
        df_map.append(str(df_dt))

        #srtby=min(df_col, key=df_col.get)
        #train_df=train_df.sort_values(by=srtby)
        #df_map.append("s-"+srtby)

        print(df_col)
        print(train_df.head())

        file_mapping='mapping.txt'
        with open(file_mapping, 'w') as f:
            f.write("|".join(df_map))

        df_comp=[]
        for col in train_df.columns:
            s=",".join(map(str,train_df[col]))
            df_comp.append(s)

        file_compressed='compressed.txt'
        with open(file_compressed, 'w') as f:
            f.write("|".join(df_comp))

        #df_final="|".join(df_comp)
        #df = pd.DataFrame(list(df_final), columns = ['compressed'])
        #msg=msg+" After Compressed File Info:"+str(len(df_final))+":"+str(df.size)
        msg="Data compression is completed! Please download the zip file."
        file_name_list = [file_mapping, file_compressed]
        #zip_file_name = filepath+".zip"
        zip_file_name = "output.zip"
        file_compress(file_name_list, zip_file_name)

        return msg,zip_file_name,train_df
    except Exception as ex:
            print("Error:"+str(ex))
            df=[]
            df.append(ex)
            return "failed"+str(ex),df

def s_ui():
    try:
        st.set_page_config(layout = "wide")
        st.title("Data Compression")
        st.info("Developed by Chinnappar & Team (R-AI)")
        with st.expander("ℹ️ - About this app", expanded=False):
            st.write(
                """
             -  Data compression is performed by a program that uses a formula/algorithm to determine how to shrink the size of the data.
             -  Applied 5 different formula/algorithm to compress pandas's dataframe and find the details in below:
                -   Mapping for repeated data
                -   Group by for repeated data
                -   Date values convert into epoch format
                -   Convert Base10 to Base64 for integer Values
                -   Concatenate all the rows and make it single text!
                """
            )
        st.write("#### Data Compression for CSV file:")

        if st.button("Test"):
            test_file="training_data_sales_10k.csv"
            msg,output,train_df=csvfile_compression(test_file)
            st.info("Data compression is completed for test file. Please find the details below...")
            ftest_size,test_size=file_size(test_file)
            ftmap_size,tmap_size=file_size("mapping.txt")
            ftcomp_size,tcomp_size=file_size("compressed.txt")
            ftzip_size,tzip_size=file_size(output)
            tnumber="{:.2%}".format((test_size-tcomp_size)/test_size)

            df_test=pd.read_csv(test_file)
            with st.expander("ℹ️ - Sample Data:", expanded=True):
                st.write(df_test.head())

            with st.expander("ℹ️ - Compressed - Sample Data:", expanded=True):
                st.write(train_df.head())

            with st.expander("ℹ️ - Test File Results:", expanded=True):
                st.write(
                    f'''
                 -  Test File Details- File Name: {test_file} File Type: csv File Size: {ftest_size}
                 -  Size of mapping file which is used for decompression: {ftmap_size}
                 -  Size of compression csv file: {ftcomp_size}
                 -  Size of zipped file for above two: {ftzip_size}
                    '''
                )
            with st.expander("ℹ️ - Test File Compression %:", expanded=True):
                st.write(
                    f'''
                -  Test file is compressed - {tnumber}
                    '''
                )


        csv_file = st.file_uploader("Please upload your own csv file", type=['csv'], accept_multiple_files=False)

        if csv_file is not None:
            msg,output,train_df=csvfile_compression(csv_file)
            st.info(msg)
            csv_size=csv_file.size
            fmap_size,map_size=file_size("mapping.txt")
            fcomp_size,comp_size=file_size("compressed.txt")
            fzip_size,zip_size=file_size(output)
            number="{:.2%}".format((csv_size-comp_size)/csv_size)

            with st.expander("ℹ️ - Compressed - Sample Data:", expanded=True):
                st.write(train_df.head())

            with st.expander("ℹ️ - Results:", expanded=True):
                st.write(
                    f'''
                 -  Uploaded File Details- File Name: {csv_file.name} File Type: {csv_file.type} File Size: {convert_bytes(csv_size)}
                 -  Size of mapping file which is used for decompression: {fmap_size}
                 -  Size of compression csv file: {fcomp_size}
                 -  Size of zipped file for above two: {fzip_size}
                    '''
                )

            with st.expander("ℹ️ - Compression %:", expanded=True):
                st.write(
                    f'''
                -  Your csv file is compressed - {number}
                    '''
                )

            with open(output, "rb") as fp:
                btn = st.download_button(
                    label="Download ZIP",
                    data=fp,
                    file_name=output,
                    mime="application/zip"
                )
            #st.write(file_size(csv_file))

    except Exception as ex:
        st.write("Failed!:... "+str(ex))

# ------------------------------------------------------------------------------
# Call main function using csv file as a input
# This main function is used for testing purpose in local
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("Started - DateTime:",datetime.datetime.now())
        #csvfile_compression('training_data_sales_5m_sample.csv')
        s_ui()
        print("compression is completed...")
        print("End - DateTime:",datetime.datetime.now())

    except Exception as msg:
        print(f'''Error {msg}''')
