from numpy import dtype,uint32
from numpy.core.multiarray import array
#TODO make a function for 
dChannel = dtype([
#https://developers.google.com/youtube/v3/docs/channels#resource-representation
    ("id","S30"),
    ("name","S30"),
    ("publishAt","S26"),
    ("description","S1000"),
    ("uploadsId","S30"),
    ("likesId","S30"),
    ("topics","S200"),
    ("subCount",'S10'), 
    ("videoCount",'S10'),
    ("viewCount",'S10'),
    ("fetchdate","S26")
])
