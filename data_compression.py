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

def base64_to_base10(b64dec,datatype=None):
    conversion_table = listToDict("b")

    if datatype == "f":
        x=b64dec.split(".")[0]
        y=b64dec.split(".")[1]

        x_dec=0
        x_power = len(x)-1
        for x_digit in x:
            x_dec += conversion_table[x_digit]*64**x_power
            x_power -= 1

        y_dec,z,f=0,0,0
        y_power = len(y)-1
        for y_digit in y:
            if y_digit=="0" and f==0:
                z=z+1
            else:
                f=1
            y_dec += conversion_table[y_digit]*64**y_power
            y_power -= 1

        return str(x_dec)+"."+str("").zfill(z)+str(y_dec)
    else:
        decimal = 0
        power = len(b64dec) -1
        for digit in b64dec:
            decimal += conversion_table[digit]*64**power
            power -= 1
        return decimal

def base10_to_base64(decimal,datatype=None):
    conversion_table = listToDict("d")

    if datatype == "f":
        x=int(str(decimal).split(".")[0])
        y=str(decimal).split(".")[1].strip()
        z=len(y)-len(str(int(y)))
        y=int(y)

        x_rem=0
        x_b64dec=''
        while(x > 0):
            x_rem = x % 64
            x_b64dec = conversion_table[x_rem] + x_b64dec
            x = x // 64

        y_rem=0
        y_b64dec=''
        while(y > 0):
            y_rem = y % 64
            y_b64dec = conversion_table[y_rem] + y_b64dec
            y = y // 64
        return x_b64dec+"."+str("").zfill(z)+y_b64dec
    else:
        b64dec = ''
        remainder=0
        while(decimal > 0):
            remainder = decimal % 64
            b64dec = conversion_table[remainder] + b64dec
            decimal = decimal // 64
        return b64dec

def save(fileName,filepath):
    directory = os.path.dirname(file_path)
    if directory != '':
        if not os.path.exists(directory):
            os.makedirs(directory)

    with open(filepath+'/'+fileName, 'w') as f:
        f.write("testing...")


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
## 3.Date values convert into int format  [completed]
## 4.Convert Base10 to Base64 for integer Values  [completed]
## 5.Concatenate all the rows and make it single text [completed]
## final file will be compressed with normal compression function like winzip
# ------------------------------------------------------------------------------
def csvfile_compression(filepath,file_mapping,file_compressed,zip_file_name):
    try:
        train_df=pd.read_csv(filepath)
        #msg="Source file's size:"+str(train_df.size)
        df_map=[]
        df_col={col:len(train_df[col].unique()) for col in train_df.columns}
        df_dt=[train_df[col].dtypes for col in train_df.columns ]
        key_srtby=""

        for col in train_df.columns:
            col_len=len(train_df[col].unique())
            print("Column Name:",col,"|Unique Cnt:",col_len,"|DataType:",train_df[col].dtypes,"| DateTime:",datetime.datetime.now())
            if col_len < 3000 :
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
                train_df[col] = train_df[col].apply(lambda x: x if np.isnan(x) else base10_to_base64(x,"f"))
                s="f"
            else: # or train_df[col].dtypes=='float64':
                s="n"
            df_map.append(s)
        df_map.append(str(df_col))
        df_map.append(str(df_dt))

        print(train_df.head())

        with open(file_mapping, 'w') as f:
            f.write("|".join(df_map))

        df_comp=[]
        for col in train_df.columns:
            s=",".join(map(str,train_df[col]))
            df_comp.append(s)

        with open(file_compressed, 'w') as f:
            f.write("|".join(df_comp))

        file_name_list = [file_mapping, file_compressed]
        file_compress(file_name_list, zip_file_name)

        return zip_file_name,train_df
    except Exception as ex:
            print("Error:"+str(ex))
            df=[]
            df.append(ex)
            return "failed"+str(ex),df

# ------------------------------------------------------------------------------
# Call main function using csv file as a input
# This main function is used for testing purpose from WebUI
# ------------------------------------------------------------------------------
def s_ui():
    try:
        st.set_page_config(layout = "wide")
        st.title("Data Compression")
        st.info("Developed by Chinnappar & Team (R-AI)")
        with st.expander("ℹ️ - About this app", expanded=True):
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
        file_mapping='mapping2.txt'
        file_compressed='compressed.txt'
        zip_file_name = 'output.zip'

        if st.button("Test"):
            test_file="training_data_sales_10k.csv"
            output,train_df=csvfile_compression(test_file,file_mapping,file_compressed,zip_file_name)
            if "failed" in output:
                st.error(output)

            st.info("Data compression is completed for test file. Please find the details below...")
            ftest_size,test_size=file_size(test_file)
            ftmap_size,tmap_size=file_size(file_mapping)
            ftcomp_size,tcomp_size=file_size(file_compressed)
            ftzip_size,tzip_size=file_size(zip_file_name)
            tnumber="{:.2%}".format((test_size-(tcomp_size+tmap_size))/test_size)

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
            output,train_df=csvfile_compression(csv_file,file_mapping,file_compressed,zip_file_name)
            if "failed" in output:
                st.error(output)

            st.info("Data compression is completed for your CSV file. Please download the Zip.")
            csv_size=csv_file.size
            fmap_size,map_size=file_size(file_mapping)
            fcomp_size,comp_size=file_size(file_compressed)
            fzip_size,zip_size=file_size(zip_file_name)
            number="{:.2%}".format((csv_size-(comp_size+map_size))/csv_size)

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
        st.error("Failed!:... "+str(ex))

# ------------------------------------------------------------------------------
# Call main function using csv file as a input
# This main function is used for testing purpose from local system
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("Started - DateTime:",datetime.datetime.now())
        file_mapping='mapping.txt'
        file_compressed='compressed.txt'
        zip_file_name = "output.zip"
        #csvfile_compression('training_data_sales_10k.csv',file_mapping,file_compressed,zip_file_name)
        s_ui()
        print("compression is completed...")
        print("End - DateTime:",datetime.datetime.now())

    except Exception as msg:
        print(f'''Error {msg}''')
