# Data Compression

Data compression is a set of steps for packing data into a smaller space by reducing the number of bits needed to represent data while allowing for the original data to be seen again.

Compressing data can save storage capacity, speed up file transfer, and decrease costs for storage hardware and network bandwidth.

The design of data compression schemes involves trade-offs among various factors, for example, the degree of compression, the amount of distortion introduced, the computational resources required for compression and decompression etc.

Please refer this link https://en.wikipedia.org/wiki/Data_compression for more details

## How compression works:-

Compression is performed by a program that uses a formula or algorithm to determine how to shrink the size of the data.

We can apply the following algorithm in any type of files like CSV/JSON/XML/ Database's Tables.

Applied 5 different formula/algorithm to compress pandas's dataframe and find the details in below:

- Mapping for repeated data 
    - This algorithm is applied in pandas dataframe column wise
    - This algorithm is appliable if column data is having less then 2000 uniqu values
    - All the unique values are concatenate and saved in mapping.txt file
    - unique values are replaced with numbers in the dataframe column
    - For Example: Unique values are [Chennai,Bangalore, Madurai,Delhi,Mumbai], this values are stored in mapping file and replaced with 0,1,2,3,4
- Group by for repeated data
    - This is only applicable if "Mapping for repeated data" algorithm applied
- Date values convert into integer format 
    - convert the date values into integer 
- Convert Base10 to Base64 for integer Values
    - I have developed new method for this conversion.
    - Apply this algorithm (Base10 to Base64) in all the integer and float columns 
- Concatenate all the rows and make it single text!
    - saved the text into compressed.txt file


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

##### Test File - TESTING

<img width="1341" alt="Screenshot 2022-09-05 at 7 41 34 AM" src="https://user-images.githubusercontent.com/112493795/188347562-e72c5673-c8be-4da2-94b1-f7df891abb62.png">

<img width="1340" alt="Screenshot 2022-09-05 at 7 41 54 AM" src="https://user-images.githubusercontent.com/112493795/188347625-9cc442ff-902c-4a04-9146-97ed99526635.png">

##### Your Own CSV File - TESTING

<img width="1353" alt="Screenshot 2022-09-05 at 7 43 21 AM" src="https://user-images.githubusercontent.com/112493795/188348011-2626f263-8e41-45b6-885f-48283f29cf39.png">


### Conclusion:
- This method will be saved approx 60-70% of your space and cost. 
- For example, if you are uploading 10 MB csv file, this method will compressed data and store 3 MB files [mapping & compressed]
- Important Note, We can use any kind of files which is supported by pandas. (CSV/JSON/XML or DB's TABLE Also). This method apply all the algorithm/formula on pandas dataframe only so this will applicable for all the file format which is supported by pandas dataframe.






