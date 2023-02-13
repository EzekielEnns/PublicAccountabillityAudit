from csv import DictReader
from ..types import dChannel
from numpy import array
from datetime import datetime
#lil note for my self arr['name'].item().decode()
def getChannels(csvReader:DictReader,yt,startIndex:int=0): 
    for (index,row) in enumerate(csvReader):
        if startIndex>0 and index < startIndex: continue;
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
                    id=str(res["items"][0]["id"]["channelId"])
            )
            res = req.execute()
            
            channel = res['items'][0]
            yield array((
                (channel['id']),
                (channel['snippet']['title'].encode("ascii", "ignore")),
                (channel['snippet']['publishedAt'].encode("ascii", "ignore")),
                (channel['snippet']['description'].encode("ascii", "ignore")),
                (channel['contentDetails']['relatedPlaylists']
                    ['uploads'].encode("ascii", "ignore")),
                (channel['contentDetails']['relatedPlaylists']
                    ['likes'].encode("ascii", "ignore")),
                (','.join(channel['topicDetails']['topicCategories']) if channel.get('topicDetails') 
                    else 'NA'),
                ( channel['statistics']['subscriberCount'] if channel.get('statistics') else 'NA'),
                (channel['statistics']['videoCount'] if channel.get('statistics') else 'NA'),
                (channel['statistics']['viewCount'] if channel.get('statistics') else 'NA'),
                (datetime.now().isoformat())
            ),dtype=dChannel)
        except Exception as e:
            raise e;

