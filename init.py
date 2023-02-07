import h5py as h5;
from csv import DictReader

from datatypes_for_project import dChannel
from numpy import array
from typing import cast

from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
from googleapiclient.errors import HttpError;

#goole init
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
SERVICE_ACCOUNT_FILE = './creds.json'
cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
api_service_name = "youtube"
api_version = "v3"
yt = googleapiclient.discovery.build(api_service_name,api_version,credentials=cred)

csvName ="Public Accountability Audits - YouTube Accounts.csv"
with h5.File("PAAProject.hdf5", "w") as hFile,open(csvName,newline='') as csvFile:
    csvReader = DictReader(csvFile,delimiter=',', quotechar='|')
    channels = cast(h5.Dataset,hFile["Channels"])
    if not channels:
        channels = hFile.create_dataset('Channels',(20,),dtype=dChannel,chunks=True)
        hFile.flush()
    if channels[20]["id"]:
        exit(0) # data phase finished

    #TODO get to current index
    index = 0;
    for row in csvReader:

        search = row['Account Name']
        try:
            req = yt.search().list(
                part="snippet",
                maxResults=1,
                q=search,
                type="channel"
            )
            res = req.execute()
            #TODO make sure we got something 
            
            req = yt.channels().list(
                    part="snippet,contentDetails,statistics",
                    id=str(res["items"][0]["id"])
            )
            res = req.execute()
            #TODO save all data 
            channels[index] = array([()],dtype=dChannel)
            # final clean up
            hFile.flush()
            index += 1

        except HttpError as err:
            #TODO
            print()
        except:
            #TODO
            print()
# helpers
