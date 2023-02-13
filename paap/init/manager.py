from csv import DictReader
import h5py as h5
from .channels import getChannels

from ..types import dChannel
from numpy import array, isin, linalg
from typing import Type, cast

from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
from googleapiclient.errors import HttpError;
import time

def handleError(e:Exception):
    if isinstance(e,HttpError):
        if e.reason == 'quotaExceeded':
            time.sleep(1)
    else:
        raise e

def googleInit():
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    SERVICE_ACCOUNT_FILE = './creds.json'
    cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    api_service_name = "youtube"
    api_version = "v3"
    return googleapiclient.discovery.build(api_service_name,api_version,credentials=cred)


def fetchDataCsv():
    yt = googleInit()
    csvName ="./resources/Public Accountability Audits - YouTube Accounts.csv"
    with h5.File("./resources/PAAProject.hdf5", "a") as hFile,open(csvName,newline='') as csvFile:
        csvReader = DictReader(csvFile,delimiter=',', quotechar='|')
        totalChannelsIndex = len(csvFile.readlines())-1; csvFile.seek(0) #TODO change this to fetch from csv
        try: channels = cast(h5.Dataset,hFile["Channels"])
        except:
            channels = hFile.create_dataset('Channels',(totalChannelsIndex,),
                    dtype=dChannel,chunks=True,maxshape=(None,))
            hFile.flush()
        finally:
            if channels.shape[0] < totalChannelsIndex:
                channels.resize((totalChannelsIndex,))
            start = 0
            for i in range(totalChannelsIndex):
                if channels[i]['id']: start=i
            if start > 0: print("skipping ",start," entries")
            if not channels[totalChannelsIndex]["id"]:
                for (index, row) in enumerate(getChannels(csvReader,yt,start)):
                    print(index+start,' fetched ',row['name'].item().decode())
                    if isinstance(row,Exception): handleError(row);
                    else: 
                        channels[index+start] = row
                        hFile.flush()
        #TODO vidoes
        #TODO comments

def debugReadCSV():
    csvName ="./resources/Public Accountability Audits - YouTube Accounts.csv"
    csvFile = open(csvName,newline='')
    return DictReader(csvFile,delimiter=',', quotechar='|')
'''
except HttpError as err:
    if err.resp.status in [403,500,503]:
        print('re try later')
    else: raise
'''

