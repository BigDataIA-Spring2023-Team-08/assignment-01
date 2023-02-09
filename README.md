# Building a Data Exploration Tool for Geospatial Startups: Utilizing NOAA's NexRad and GOES Satellite Data Sources - Assignment_01
-----

> Status ✅: Active 



## Index
  - [Abstract 📝](#abstract-)
  - [Data Sources 💽](#data-sources-)
  - [Streamlit 🖥️](#streamlit-)
  - [S3 🧊](#s3-)
  - [SQLite DB 🛢](#sqlite-db-)
  - [Unit Testing ⚒️](#unit-testing-️)




## Abstract
The task involves building a data exploration tool for a geospatial startup. The tool utilizes publicly available data sources, specifically the NexRad and GOES satellite datasets, to make it easier for data analysts to download data. The data sources can be found on the National Oceanic and Atmospheric Administration (NOAA) website and the tool has several capabilities to support data exploration and download. The following capabilties can be performed from this project:

- point 1
- point 2
- point 3

## Data Sources
The National Oceanic and Atmospheric Administration (NOAA) is a government agency responsible for monitoring the weather and climate of the United States. It operates two types of satellites, the [Geostationary Operational Environmental Satellite (GOES)](https://www.goes.noaa.gov) and the [Next Generation Weather Radar (NexRad)](https://www.ncei.noaa.gov/products/radar/next-generation-weather-radar) , which collect data on various meteorological phenomena. This data is then made publicly available through the NOAA website, allowing data analysts to easily access it. We have aimed to build a data exploration tool that leverages these publicly available data sources to simplify the process of downloading and analyzing the data.


## Streamlit
The data exploration tool for the Geospatial startup uses the Python library Streamlit for its user interface. The tool offers a user-friendly experience with three distinct pages, each dedicated to NexRad, GOES, and NexRad location maps. On each page, users can choose between downloading satellite data based on filename or specific field criteria. The UI then displays a download link to the S3 bucket, enabling users to successfully retrieve the desired satellite images.






[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


    
   [dill]: <https://github.com/joemccann/dillinger>
   [Next Generation Weather Radar (NexRad)]: <https://www.ncei.noaa.gov/products/radar/next-generation-weather-radar>
   [Geostationary Operational Environmental Satellite (GOES)]: <https://www.goes.noaa.gov>
   
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
