from csv import DictReader
from typing import Optional
from googleapiclient._apis.youtube.v3.resources import YouTubeResource
from googleapiclient.errors import HttpError;
from h5py import Dataset
from ..types import dChannel
from numpy import array
from datetime import datetime

def getChannels(channels:Dataset,csvReader:DictReader,yt:YouTubeResource,refetch:Optional[bool]=False): 
    for (index,row) in enumerate(csvReader):
        if channels[index]["id"] and not refetch: continue;
        search = row['Account Name']
        try:
            req = yt.search().list(
                part="snippet",
                maxResults=1,
                q=search,
                type="channel"
            )
            res = req.execute()
            req = yt.channels().list(
                    part="snippet,contentDetails,statistics,topicDetails",
                    id=str(res["items"][0]["id"])
            )
            res = req.execute()
            channel = res['items'][0]
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
                (datetime.now().isoformat())
            ],dtype=dChannel)
            yield;
        except Exception as e:
            yield e;
