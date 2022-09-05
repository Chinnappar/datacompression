# Data Compression

Data compression is a set of steps for packing data into a smaller space by reducing the number of bits needed to represent data while allowing for the original data to be seen again.

Compressing data can save storage capacity, speed up file transfer, and decrease costs for storage hardware and network bandwidth.

The design of data compression schemes involves trade-offs among various factors, for example, the degree of compression, the amount of distortion introduced, the computational resources required for compression and decompression etc.

Please refer this link https://en.wikipedia.org/wiki/Data_compression for more details

## How compression works:-

Compression is performed by a program that uses a formula or algorithm to determine how to shrink the size of the data.

We can apply the following algorithm in any type of files like CSV/JSON/XML/ Database's Tables.

Applied 5 different formula/algorithm to compress pandas's dataframe and find the details in below:

#### 1. Mapping for repeated data

#### 2. Group by for repeated data

#### 3. Date values convert into epoch format

#### 4. Convert Base10 to Base64 for integer Values

#### 5. Concatenate all the rows and make it single text!


#### How will use this function from Jupyter Notebook?

##### STEP 1:
import pydaisi as pyd

data_compression = pyd.Daisi("chinnappar/data compression")

##### STEP 2:
data_compression.compression(csvfile="training_data_sales_10k.csv", 
                             file_mapping="mapping.txt", 
                             file_compressed="compressed.txt", 
                             zip_file_name="output.zip").value
                            
 ##### Parameters:
 - csvfile - This is input csv file and optional. This file should be presented in the server.
 - file_mapping - first output file [Mapping File] and this will used for decompression.
 - file_compressed - second output file [Compressed File] and compressed data will be stored.
 - zip_file_name - third output file [output.zip]. Above two files (mapping and compressed) are zipped and stored in this file.
 
 Note: if you are facing any file permission issue, please run chmod 777 command and try again.
 
### Screenshot:

<img width="1015" alt="Screenshot 2022-09-05 at 7 11 02 AM" src="https://user-images.githubusercontent.com/112493795/188343968-931aede6-c479-4fc4-84ae-269708f40b0c.png">

#### How will use this function from Streamlin?

##### STEP 1:

Go to this link:
https://app.daisi.io/daisies/chinnappar/data%20compression/streamlit

##### STEP 2:
Click the Test button, automatically read the test csv file.
Function will trigger and final output files are saved and also detail information will be displayed in the page.

##### STEP 3:

Please click the browse buttom for upload your own csv file. 
Function will trigger and final output files are saved and also detail information will be displayed in the page.

##### Screenshots:

##### Test File

##### Own Csv File



### Conclusion:
This method will be saved approx 60-70% of your space and cost. 
For example, if you are uploading 10 MB csv file, this method will compressed data and store 3 MB files [mapping & compressed]





