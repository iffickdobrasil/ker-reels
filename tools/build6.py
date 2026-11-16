import sys; sys.path.insert(0,'/home/claude/work')
from themes6 import T
import reel4
M="/home/claude/work/music"; O="/home/claude/work/out"
only=sys.argv[1:]
for s,t,m,v,it in T:
    if only and s not in only: continue
    reel4.build(t,it,f"{M}/{m}.mp3",f"{O}/ker-reel-{s}-v7.mp4",vol=v)
    reel4.carousel(it,f"car-{s}",O)
