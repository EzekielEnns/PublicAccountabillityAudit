import enum
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
    #TODO make this clean
    if channels[19]["id"]: 
        print("finished collecting channels")
        exit(0) 

    for (index,row) in enumerate(csvReader):
        if channels[index]["id"]: continue;
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
            id = res['items'][0]["snippet"]["channelId"]
            
            req = yt.channels().list(
                    part="snippet,contentDetails,statistics,topicDetails",
                    id=str(res["items"][0]["id"])
            )
            res = req.execute()
            
            channel = res['items'][0]
            test = ','.join(channel['topicDetails']['topicCategories'])
            
            #TODO save all data 
            channels[index] = array([
                (channel['id']),
                (channel['snippet']['title']),
                (channel['snippet']['publishedAt']),
                (channel['snippet']['description']),
                (channel['contentDetails']['relatedPlaylists']
                    ['uploads']),
                (channel['contentDetails']['relatedPlaylists']
                    ['likes']),
                (','.join(channel['topicDetails']['topicCategories'])),
                (channel['statistics']['subscriberCount']),
                (channel['statistics']['videoCount']),
                (channel['statistics']['viewCount']),
                ],dtype=dChannel)
            hFile.flush()
            
        except HttpError as err:
            print(search)
            if err.resp.status in [403,500,503]:
                print('re try later')
            else: raise
        except:
            print(search)
            raise
