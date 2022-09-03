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




#### How will execute this program:

##### STEP 1:
import pydaisi as pyd
data_compression = pyd.Daisi("chinnappar/data compression")

##### STEP 2:
filepath="<FILE_FULL_PATH>"
data_compression.csvfile_compression(filepath).value

##### STEP 3:
Three output files are generated after executed the above code.
1. Mapping File
2. Compressed File
3. Output.zip (Above two files are compressed)

### Important Note:
This method will be saved approx 60-70% of your space and cost. 
For example, 10 MB file => 3 MB file





