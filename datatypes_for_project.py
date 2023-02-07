from numpy import dtype,uint32
dChannel = dtype([
#https://developers.google.com/youtube/v3/docs/channels#resource-representation
    ("id","S30"),
    ("name","S30"),
    ("publishAt","S24"),
    ("description","S1000"),
    ("uploadsId","S30"),
    ("likesId","S30"),
    ("topics","S70"),
    ("keywords","S500"),
    ("subCount",uint32), # over kill I know
    ("videoCount",uint32),
    ("viewCount",uint32),
])
