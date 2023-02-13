from csv import DictWriter
from functools import reduce
import h5py as h5
from typing import cast
from dateutil import parser


def channelsToCsv():
    csvName ="./output/Public Accountability Audits - YouTube Accounts.csv"
    hdf5 = "./resources/PAAProject.hdf5"
    with h5.File(hdf5,'r') as hFile, open(csvName,'w',newline='') as csvFile:
        channels = cast(h5.Dataset,hFile["Channels"])
        topics = getTopics(channels)
        fieldnames = ['name','publishAt','subCount','videoCount','viewCount',
                *topics, 'fetchdate'];
        csvWriter = DictWriter(csvFile,fieldnames=fieldnames,extrasaction='ignore')
        csvWriter.writeheader()
        for row in getRowsToDict(channels,topicSet=topics):
            csvWriter.writerow(row)
            
            

def getTopics(d:h5.Dataset):
    value = set()
    for row in d:
        value.update( set( map( lambda x: x.split('/')[-1], 
            row['topics'].decode().split(','))));
    return value

def reduceRow(a,b): a.update(b); return a;
def getRowsToDict(d:h5.Dataset,**kwargs):
    for row in d: yield reduce(reduceRow,[*getFieldsToDict(row,**kwargs)])

def getFieldsToDict(row,**kwargs):
    for field in row.dtype.names: 
        if field == 'topics' and isinstance(kwargs['topicSet'],set):
            topics = row[field].decode().split(',')
            topics = kwargs['topicSet'].intersection( 
                    list(map( lambda x: x.split('/')[-1], topics)));
            yield dict.fromkeys(topics,True)
        elif field == 'fetchdate' or field == 'publishAt':
            try: 
                date = parser.parse(row[field].decode())
                yield {field: date.strftime('%I:%M%P %d/%b/%Y')}
            except: yield {field: row[field].decode()}

        else: yield {field:row[field].decode()}

def debugOpenHdFile():
    hdf5 = "./resources/PAAProject.hdf5"
    return h5.File(hdf5,'r')
