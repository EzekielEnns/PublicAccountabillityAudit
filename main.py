from dataclasses import dataclass
from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
#storeage will be using cerializing objects via (pickle) and storing the objects in diffrent 
#hdf5 groups, we can then export it out as a graphql api on flask 

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
@dataclass
class ChannelTotals:
    subs:int #statistics.subscriberCount
    videos:int #statistics.videoCount
    views:int #statistics.viewCount
@dataclass
class Channel:
#https://developers.google.com/youtube/v3/docs/channels#resource-representation
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

#so this is a unstable way to get them #test = YouTubeTranscriptApi.get_transcript('T1MWP87Hdk4')

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
SERVICE_ACCOUNT_FILE = './creds.json'
cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


api_service_name = "youtube"
api_version = "v3"
#TODO add with for error halding 
yt = googleapiclient.discovery.build(api_service_name,api_version,credentials=cred)




'''
req = yt.captions().list(
    part="snippet",
    videoId="T1MWP87Hdk4",
)

res = req.execute()
#
id = res["items"][0]["id"]
print(id)

test = yt.captions().download(id=id).execute()
print("did we do it boi?")
print(json.dumps(test,sort_keys=True,indent=4))
'''
