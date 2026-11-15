import sys,os; sys.path.insert(0,'/home/claude/work')
from themes5 import T
import reel4
R="/home/claude/ker-reels"; P="/home/claude/ker-photos"; M="/home/claude/work/music"
only=sys.argv[1:]
for s,t,m,v,it in T:
    if only and s not in only: continue
    print("==",s,flush=True)
    reel4.build(t,it,f"{M}/{m}.mp3",f"{R}/ker-reel-{s}-v7.mp4",vol=v)
    reel4.carousel(it,f"car-{s}",P)
print("ALL DONE",flush=True)
