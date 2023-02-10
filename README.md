# Building a Data Exploration Tool for Geospatial Startups: Utilizing NOAA's NexRad and GOES Satellite Data Sources
-----

> Status ✅: Active <br>
> [Application link 🔗](https://anushkadesai077-data-eng-assignment01-finalstreamlit-app-p0g6vh.streamlit.app/) <br>
> [Colab Slides 🧪](https://docs.google.com/document/d/13P-uClVhvU06-DsU9b-BeoZrHEp6w9i-1XbBmKHDtEA/edit?usp=sharing)


----- 

## Index
  - [Abstract 📝](#abstract)
  - [Data Sources 💽](#data-sources)
  - [SQLite DB 🛢](#sqlite-db)
  - [Scraping Data and Copying to AWS S3 bucket🧊](#scraping-data-and-copying-to-aws-s3-bucket)
  - [Streamlit UI 🖥️](#streamlit)
  - [Storing logs to AWS CloudWatch 💾](#storing-logs-to-aws-cloudwatch)
  - [Unit Testing ⚒️](#unit-testing)
  - [Great Expectations ☑️](#great-expectations)




## Abstract
The task involves building a data exploration tool for a geospatial startup. The tool utilizes publicly available data sources, specifically the NexRad and GOES satellite datasets, to make it easier for data analysts to download data. The data sources can be found on the National Oceanic and Atmospheric Administration (NOAA) website and the tool has several capabilities to support data exploration and download. This work can help one: 

- Access the publicly available SEVIR satellite radar data in a highly interactive & quick way
- Scrap the data from public AWS S3 buckets to store them into a personal S3 bucket making it convenient to then perform additional tasks or use these saved files from your personal bucket. Government’s public data can always be hard to navigate across but we make it easy with our application
- Get files through the application by 2 options: searching by fields or directly entering a filename to get the URL from the source
- View the map plot of all the NEXRAD satellite locations in the USA


The application site for the project hosted on [Streamlit Cloud](https://streamlit.io/cloud) can be accessed [here](https://anushkadesai077-data-eng-assignment01-finalstreamlit-app-p0g6vh.streamlit.app/).

## Data Sources
The National Oceanic and Atmospheric Administration (NOAA) is a government agency responsible for monitoring the weather and climate of the United States. It operates two types of satellites, the [Geostationary Operational Environmental Satellite (GOES)](https://www.goes.noaa.gov) and the [Next Generation Weather Radar (NexRad)](https://www.ncei.noaa.gov/products/radar/next-generation-weather-radar) , which collect data on various meteorological phenomena. This data is then made publicly available through the NOAA website, allowing data analysts to easily access it. We have aimed to build a data exploration tool that leverages these publicly available data sources to simplify the process of downloading and analyzing the data.

## SQLite DB
After the metadata is scraped and stored as dataframes each corresponding to GOES18,NexRad and NexRad location maps, we first check if the database exists and initialize it if there is no database. Once a connection to the database is established, SQL queries are made to create tables to store the scraped data (GOES, NexRad and  NexRad location maps) in the [SQLite](https://www.sqlite.org/index.html) database. The tables are named GOES_METADATA, NEXRAD_METADATA and MAPDATA_NEXRAD.In order to enable the users to search by field criteria on Streamlit UI, they should be presented with the values based on their selection. This is done in the backend through SQL queries to the database to fetch data depending on the user’s selections dynamically.


## Scraping Data and Copying to AWS S3 bucket
Data scraping for the data sources is done from the publicly accessible AWS S3 bucket for eac - [GOES (provided by NOAA)](https://registry.opendata.aws/noaa-goes/) & [NEXRAD data registry](https://registry.opendata.aws/noaa-nexrad/). For the purpose of our application, we restrict our data to [GOES-18 data](https://noaa-goes18.s3.amazonaws.com/index.html) and [NEXRAD level 2](https://noaa-nexrad-level2.s3.amazonaws.com/index.html) buckets respectively. Within this, the data for our prototype application is further restricted (mentioned below). The third data source needed for this application is the latitude, longitudes and state information for all NEXRAD satellites in the US. This scraping is done from a [.txt file](https://www.ncei.noaa.gov/access/homr/file/nexrad-stations.txt) found on NOAA’s data registry. The final sources where data is scraped from: 

- Product `ABI-L1b-RadC/` within GOES-18
- Years `2022` and `2023` for NEXRAD
- NEXRAD satellite’s geographical locations

### Set up AWS account & credential variables:
Scraping of data from these sources is done using the `boto3` python library which allows you to connect to AWS resources using your credentials. After creating a free AWS account, one needs to store their `AWS_ACCESS_KEY` & `AWS_SECRET_KEY` in their local `.env` configuration file in order to access these keys while executing the code.

### Executing code to scrape all data:
Only the `scraper_main.py` script needs to be executed to perform scraping & storing scraped data into the SQLite database. This script calls the 3 data scraper function for the 3 data sources defined above: `scraper_goes18.py, scraper_nexrad.py, scraper_mapdata.py`.
The two scripts scripts `scraper_goes18.py` & `scraper_nexrad.py` access the relevant S3 bucket and return the data as a dataframe. Similarly, the `scraper_mapdata.py` function returns the data scraped from the txt file. 

At the end, the `scraper_main.py` script calls the `store_scraped_data_to_db` function to store this scraped metadata in the relevant tables within our SQLite database.

## Streamlit
The data exploration tool for the Geospatial startup uses the Python library [Streamlit](https://streamlit.iohttps://streamlit.io) for its user interface. The tool offers a user-friendly experience with three distinct pages, each dedicated to NexRad, GOES, and NexRad location maps. On each page, users can choose between downloading satellite data based on filename or specific field criteria. The UI then displays a download link to the S3 bucket, enabling users to successfully retrieve the desired satellite images.

### Streamlit UI layout:
  - GOES18 data downloader page
      - Download file by entering field values
      - Get public URL by entering filename
  - NEXRAD data downloaded page
      - Download file by entering field values
      - Get public URL by entering filename
  - NEXRAD Maps Location page

### Flow for Download file by entering field values
1. Enter text box fields for each value (for example, in GOES18 it is year, day & hour)
2. Once these initial selections are made, dynamically list the files available at the folder with the selections given 
3. Choose a file from the list to download it via a URL

### Flow for Get public URL by entering filename
1. Enter a filename (along with the file extension, if any) and hit enter
2. If found, the URL from the public bucket is shown, else a relevant error/warning is given 

### Flow for NEXRAD Maps Location page
1. Displays a map of all satellite locations with hover text for all points

### Steps:
1. Install Streamlit package

```
pip install streamlit
```

2. Create a new file [streamlit_app.py](streamlit_app.py) to build a UI for the app. Code snippet for main function, depicting 3 different pages for GOES, NEXRAD and NEXRAD locations Map:
```
def main():
    st.set_page_config(page_title="Weather Data Files", layout="wide")
    page = st.sidebar.selectbox("Select a page", ["GOES-18", "NEXRAD", "NEXRAD Locations - Map"])   #main options of streamlit app

    if page == "GOES-18":
        with st.spinner("Loading..."): #spinner element
            goes_main()
    elif page == "NEXRAD":
        with st.spinner("Loading..."): #spinner element
            nexrad_main()
    elif page == "NEXRAD Locations - Map":
        with st.spinner("Generating map..."): #spinner element
            map_main()

```
3. Run the code
```
streamlit run streamlit_app.py
```


## Storing logs to AWS CloudWatch


## Unit Testing
[PyTest](https://docs.pytest.org/en/7.1.x/contents.html) framework implemented to write tests which is easy to use but can be scaled to support functional testing for applications and libraries.

### Steps:
1. Install PyTest package
```
pip3 install pytest

#For HTML PyTest Report, Install package:
pip3 install pytest-html
```

2. Create Tests
* Create a new file [test.py](test.py), containing test functions
* Implemented testing functions `test_gen_goes_url(), test_gen_nexrad_url()` that tests functions `generate_goes_url(filename), generate_nexrad_url(filename)` which takes goes and nexrad filenames to generate respective urls.

```
# Code snippet for test functions

def test_gen_goes_url():
    assert generate_goes_url(fileGOES1) == urlGOES1
def test_gen_nexrad_url():
    assert generate_nexrad_url(fileNEXRAD1) == urlNEXRAD1
    
```
3. Run tests
```
pytest -v test.py
```
4. Export test result to log or html file
```
# Export to log file
pytest -v test.py > test_results.log

# Export to html file 
pytest --html=test_results.html test.py
```

## Great Expectations
[Great Expectations](https://docs.greatexpectations.io/docs/) is a tool used to validate, document and profile data in order to eliminate pipeline debt. The python library has been used on extracted GOES18 and NEXRAD csv data in this assignment.

### Steps

**1. Setup**

1.1. Install Great_Expectation module
```
pip3 install great_expectations
```
1.2. Verify version
```
great_expectations --version
```
output:`great_expectations, version 0.15.47`

1.3. Initialize Base Directory
```
great_expectations init
```
- Change working directory to Great Expectations base directory
```
cd great_expectations
```
- Create data folder for datasource to import `GOES18` and `NEXRAD` data

1.4. Import data into Repo

> GOES18

> NEXRAD

**2. Datasource**

Configured datasources in order to connect to `GOES18` and `NEXRAD` data.

2.1. Create datasource with CLI

```
great_expectations datasource new
```

*Options to select from prompt:*

> `1` - Local File 
>
> `1` - Pandas
>
> `data` - Relative path to GOES and NEXRAD datasets

- `datasource_new` python notebook is generated

* Rename datasource name i.e. `goes18-nexrad_datasource` 

* Edit `example.yml` file to ignore non csv files

```
example_yaml = f"""
name: goes18-nexrad_datasource
class_name: Datasource
execution_engine:
  class_name: PandasExecutionEngine
data_connectors:
  default_inferred_data_connector_name:
    class_name: InferredAssetFilesystemDataConnector
    base_directory: data
    default_regex:
      group_names:
        - data_asset_name
      pattern: (.*)\.csv
  default_runtime_data_connector_name:
    class_name: RuntimeDataConnector
    assets:
      my_runtime_asset_name:
        batch_identifiers:
          - runtime_batch_identifier_name
"""
print(example_yaml)
```

- Save the datasource Configuration and close Jupyter notebook
- Wait for terminal to show `Saving file at /datasource_new.ipynb`

**3. Expectations**

3.1 Create Expectation Suite with CLI

```
great_expectations suite new
```

*Options to select from prompt:*

>`3` - Automatically, using a Data Assistant
>
>`1` - Select index of file `goes18_db_extract.csv` 
>
>*or*
>
>`2` - Select index of file `nexrad_db_extract.csv`
>
> Suite Name: `goes18_suite` or `nexrad_suite` based on data file selected from prompt

*Note: Proceed with steps 3 and onwards for each data file at a time.*

- suite python notebook is generated

- Update `exclude_column_names`:

  - `goes18_suite`
  
 
  ```
  exclude_column_names = [
  # "id",
  # "product",
  # "year",
  # "day",
  # "hour",
  ]
  ```
  
  - `nexrad_suite`
  
  
  ```
  exclude_column_names = [
  # "id",
  # "year",
  # "month",
  # "day",
  # "ground_station",
  ]
  ```
 - Run all cells to create default expectation and analyze the result

 - Wait for terminal to show `Saving file at /*.ipynb`

 - Modify JSON files for suite as per need
 
 For `goes18_suite`:
 
 ```
 great_expectations suite edit goes18_suite
 ```
 
  For `nexrad_suite`:
 
 ```
 great_expectations suite edit nexrad_suite
 ```
 
 *Options to select from prompt:*
 
 >`1` - Manually, without interacting with a sample batch of data (default)
 
 
**4. Data Validation**

4.1. Create Checkpoint 

For `GOES18` checkpoint:

```
great_expectations checkpoint new goes18_checkpoint_v0.1
```

For `NEXRAD` checkpoint:
```
great_expectations checkpoint new nexrad_checkpoint_v0.1
```

- checkpoint python notebook is generated, run all cells to generate report in new page

**5. Deploy using GitHub Actions**

 - Go to Project Settings
 - Navigate to GitHub Pages 
 - Select `GitHub Actions` as source for build and deployment
 - Configure Static HTML for GitHub Actions workflow to deploy static files in a repository without a build
 - Set path to `great_expectations/uncommitted/data_docs/local_site` in `static.yml` file
 - Commit changes

-----
> WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.
> 
> Vraj: 25%, Poojitha: 25%, Merwin: 25%, Anushka: 25%
-----


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


    

   [Next Generation Weather Radar (NexRad)]: <https://www.ncei.noaa.gov/products/radar/next-generation-weather-radar>
   [Geostationary Operational Environmental Satellite (GOES)]: <https://www.goes.noaa.gov>
   

