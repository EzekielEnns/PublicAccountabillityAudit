from pickle import HIGHEST_PROTOCOL, dumps, loads
import h5py;
from dataclasses import dataclass
import numpy
from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
#storeage will be using cerializing objects via (pickle) and storing the objects in diffrent 
#hdf5 groups, we can then export it out as a graphql api on flask 
'''
every video will have a group named after it with a master group caled videos 
and inside each video group will be the following sub groups 
videos : all the serilized video objects 
transcripts: all the serilized transcripts 
comments : a sub groups with sub groups in it based on the video ID 
    VIDEO ID : all comments from video
'''

#https://github.com/jdepoix/youtube-transcript-api
#https://docs.python.org/3/library/pickle.html
#https://docs.h5py.org/en/stable/quick.html
#graph ql tut https://www.apollographql.com/blog/graphql/python/complete-api-guide/
#https://docs.python.org/3/library/csv.html

# ds for this is defined bellow with a special case for video transcripts defined bellow
# transcripts are stored in a group labed t-{video ID} showing only the text content 

@dataclass
class Comment:
#https://developers.google.com/youtube/v3/docs/commentThreads#resource-representation
#https://developers.google.com/youtube/v3/docs/comments#resource-representation
#all found under topLevelComment
    id:str 
    text:str #textOriginal
    publishedAt:str #publishedAt
    likes:int #likeCount
@dataclass
class VideoTotals:
    views:int #statistics.viewCount
    likes:int #statistics.likeCount
    dislikes:int #statistics.dislikeCount
    comments:int #statistics.commentCount
@dataclass
class Video:
#https://developers.google.com/youtube/v3/docs/videos#resource-representation
#https://developers.google.com/youtube/v3/docs/playlistItems#resource-representation
#https://developers.google.com/youtube/v3/docs/playlistItems/list#response
    id:str
    publishedAt:str #status.publishAt
    length:str #contentDetails.duration
    tags:set[str] 
    counts:VideoTotals 
    threadId:str # @ commentThreads
    description:str #snippet.description
    recordingDate:str #recordingDetails.recordingDate
    location:str #recordingDetails.location
    comments:set[Comment] # populated

# phase 1
dChannel = numpy.dtype([
#https://developers.google.com/youtube/v3/docs/channels#resource-representation
    ("id","S30"),
    ("name","S30"),
    ("publishAt","S24"),
    ("description","S1000"),
    ("uploadsId","S30"),
    ("likesId","S30"),
    ("topics","S70"),
    ("keywords","S500"),
    ("subCount",numpy.uint32), # over kill I know
    ("videoCount",numpy.uint32),
    ("viewCount",numpy.uint32),
])
#so this is a unstable way to get them #test = YouTubeTranscriptApi.get_transcript('T1MWP87Hdk4')
f = h5py.File("data.hdf5", "w")
root = f.create_group('root')
newData = numpy.array([('id','hello-World','asd','123','asdasd','1231','asd','cloe',100,100,100)],dtype=dChannel)
test = root.create_dataset('Channels',data=newData)

print(test.shape[0])
print(test[0]['keywords'])



exit(0)

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
SERVICE_ACCOUNT_FILE = './creds.json'
cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


api_service_name = "youtube"
api_version = "v3"
#TODO add with for error halding 
yt = googleapiclient.discovery.build(api_service_name,api_version,credentials=cred)
# level one channel id 
yt.search().list(
     part="snippet",
     maxResults=1,
     q="News Now Houston",
     type="channel"
)

# req[0].snippet.channelId #UC39jLNl2UpxDeYVYCToA56A
yt.channels().list(
        part="snippet,contentDetails,statistics",
        id="UC39jLNl2UpxDeYVYCToA56A"
)

# level 2 playslist id's and the video id's
#contentDetails.relatedPlaylists.uploads: "UU39jLNl2UpxDeYVYCToA56A"
yt.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        playlistId="UU39jLNl2UpxDeYVYCToA56A"
)
transcript = YouTubeTranscriptApi.get_transcript("7TzFNqOfTEQ")


# level 3 comment thread id
#items[0].contentDetails.videoID
yt.commentThreads().list(
        part="snippet,replies",
        videoId="7TzFNqOfTEQ"
)
#items[0].topLevelComment.textOriginal, id:UgyBBtA2WkyJbGqYjrt4AaABAg


'''
from youtube_transcript_api import YouTubeTranscriptApi

YouTubeTranscriptApi.get_transcript(video_id)
req = yt.captions().list(
    pazart="snippet",
    videoId="T1MWP87Hdk4",
)

res = req.execute()
#
id = res["items"][0]["id"]
print(id)

test = yt.captions().download(id=id).execute()
print("did we do it boi?")
print(json.dumps(test,sort_keys=True,indent=4))

@dataclass
class ChannelTotals:
    subs:int #statistics.subscriberCount
    videos:int #statistics.videoCount
    views:int #statistics.viewCount
@dataclass
class Channel:
    id:str
    name:str #snippet.title
    publishedAt:str #snippet.publishedAt
    description:str #snippet.description
    uploadsId:str #contentDetails.relatedPlaylists.uploads
    likesID:str #contentDetails.relatedPlaylists.likes
    favoritesID:str #contentDetails.relatedPlaylists.favorites
    topics:set[str] #topicDetails.topicCategories
    keywords:str #brandingSettings.channel.keywords
    counts:ChannelTotals
    videos:set[Video] #populated
'''
