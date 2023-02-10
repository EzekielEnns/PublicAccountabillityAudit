from csv import DictReader
import h5py as h5
from channels import getChannels

from ..types import dChannel
from numpy import array
from typing import Type, cast

from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
from googleapiclient.errors import HttpError;

def handleError(e:Exception):
    print('oh no')

#goole init
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
SERVICE_ACCOUNT_FILE = '../../creds.json'
cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
api_service_name = "youtube"
api_version = "v3"
yt = googleapiclient.discovery.build(api_service_name,api_version,credentials=cred)

csvName ="../../resources/Public Accountability Audits - YouTube Accounts.csv"
with h5.File("PAAProject.hdf5", "w") as hFile,open(csvName,newline='') as csvFile:
    csvReader = DictReader(csvFile,delimiter=',', quotechar='|')
    channels = cast(h5.Dataset,hFile["Channels"])
    if not channels:
        channels = hFile.create_dataset('Channels',(20,),dtype=dChannel,chunks=True)
        hFile.flush()
    if not channels[19]["id"]: 
        for row in getChannels(channels,csvReader,yt):
            if isinstance(row,Exception): handleError(row)
            else: hFile.flush()
    #TODO vidoes
    #TODO comments

'''
except HttpError as err:
    if err.resp.status in [403,500,503]:
        print('re try later')
    else: raise
'''

