import os
import boto3
import time
import pandas as pd
from dotenv import load_dotenv

#load env variables and change logging level to info
load_dotenv()

#authenticate S3 client with your user credentials that are stored in your .env config file
s3client = boto3.client('s3',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )

#authenticate S3 client for logging with your user credentials that are stored in your .env config file
clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )

#intialise dictionary to store scraped data before moving it to a sqllite table
scraped_goes18_dict = {
    'id': [],
    'product': [],
    'year': [],
    'day': [],
    'hour': []
}

def scrape_goes18_data():

    """USed to scrape  n and mfgyear as input to give registration details of planes manufactured in the entered year, 
    The value of n specifies whether the data required is for surveillance or non surveillance planes 
    n=0 means data for surveillance planes and n=1 indicates data for non surveillance planes.
    ----------
    year : int
        the manufactured year
    Returns
    -------
    json
        1.  Records of flight registration details
        2.  if entered year doesn't return any value or data related to that year does not exists the merely prints the years of which data is available from
            which the user can choose and enter appropriately.
    """
    
    clientLogs.put_log_events(      #logging to AWS CloudWatch logs
        logGroupName = "assignment01-logs",
        logStreamName = "db-logs",
        logEvents = [
            {
            'timestamp' : int(time.time() * 1e3),
            'message' : "Scraping data from GOES18 bucket"
            }
        ]
    )

    id=1    #for storing as primary key in db
    prefix = "ABI-L1b-RadC/"    #just one product to consider as per scope of assignment
    result = s3client.list_objects(Bucket=os.environ.get('GOES18_BUCKET_NAME'), Prefix=prefix, Delimiter='/')

    #traversing into each subfolder and store the folder names within each
    for o in result.get('CommonPrefixes'):
        path = o.get('Prefix').split('/')
        prefix_2 = prefix + path[-2] + "/"      #new prefix with added subdirectory path
        sub_folder = s3client.list_objects(Bucket=os.environ.get('GOES18_BUCKET_NAME'), Prefix=prefix_2, Delimiter='/')
        for p in sub_folder.get('CommonPrefixes'):
            sub_path = p.get('Prefix').split('/')
            prefix_3 = prefix_2 + sub_path[-2] + "/"    #new prefix with added subdirectory path
            sub_sub_folder = s3client.list_objects(Bucket=os.environ.get('GOES18_BUCKET_NAME'), Prefix=prefix_3, Delimiter='/')
            for q in sub_sub_folder.get('CommonPrefixes'):
                sub_sub_path = q.get('Prefix').split('/')
                sub_sub_path = sub_sub_path[:-1]    #remove the filename from the path
                scraped_goes18_dict['id'].append(id)   #map all scraped data into the dict
                scraped_goes18_dict['product'].append(sub_sub_path[0])
                scraped_goes18_dict['year'].append(sub_sub_path[1])
                scraped_goes18_dict['day'].append(sub_sub_path[2])
                scraped_goes18_dict['hour'].append(sub_sub_path[3])
                id+=1

    clientLogs.put_log_events(      #logging to AWS CloudWatch logs
        logGroupName = "assignment01-logs",
        logStreamName = "db-logs",
        logEvents = [
            {
            'timestamp' : int(time.time() * 1e3),
            'message' : "Data scraped successfully"
            }
        ]
    )
      
    scraped_goes18_df = pd.DataFrame(scraped_goes18_dict)     #final scraped metadata stored in dataframe
    return scraped_goes18_df

def main():
    metadata_goes18 = scrape_goes18_data()

if __name__ == "__main__":
    main()