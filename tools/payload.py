import sys,json; sys.path.insert(0,'/home/claude/work')
from posts7 import P
from datetime import date,timedelta
R=sys.argv[1]; Ph=sys.argv[2]; vo=set(sys.argv[3].split(',')) if len(sys.argv)>3 and sys.argv[3] else set()
slugs=sys.argv[4].split(',')
for s in slugs:
    d,rt,rtag,ct,ctag=P[s]; d2=(date.fromisoformat(d)+timedelta(days=1)).isoformat()
    v="v8vo" if s in vo else "v7"
    reel={"autoPublish":True,"descendants":[],"draft":False,"firstCommentText":rtag,"hasNotReadNotes":False,
      "media":[f"https://raw.githubusercontent.com/iffickdobrasil/ker-reels/{R}/ker-reel-{s}-{v}.mp4"],
      "videoThumbnailUrl":f"https://raw.githubusercontent.com/iffickdobrasil/ker-photos/{Ph}/ker-cover-{s}.jpg",
      "mediaAltText":[],"providers":[{"network":"instagram"},{"network":"facebook"}],
      "publicationDate":{"dateTime":f"{d}T11:00:00","timezone":"Europe/Paris"},"shortener":False,"smartLinkData":{"ids":[]},
      "text":rt,"instagramData":{"type":"REEL","showReelOnFeed":True,"isAiGenerated":s in vo},"facebookData":{"type":"REEL"}}
    car={"autoPublish":True,"descendants":[],"draft":False,"firstCommentText":ctag,"hasNotReadNotes":False,
      "media":[f"https://raw.githubusercontent.com/iffickdobrasil/ker-photos/{Ph}/ker-car-{s}-{i}-wm.jpg" for i in range(1,7)],
      "mediaAltText":[],"providers":[{"network":"instagram"},{"network":"facebook"}],
      "publicationDate":{"dateTime":f"{d2}T11:00:00","timezone":"Europe/Paris"},"shortener":False,"smartLinkData":{"ids":[]},
      "text":ct,"instagramData":{"type":"POST","isAiGenerated":False},"facebookData":{"type":"POST"}}
    print(f"### {s} REEL {d}"); print(json.dumps(reel,ensure_ascii=False))
    print(f"### {s} CAR {d2}"); print(json.dumps(car,ensure_ascii=False))
