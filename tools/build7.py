import sys,subprocess,os; sys.path.insert(0,'/home/claude/work')
from themes7 import T,VO
import reel4
M="/home/claude/work/music"; O="/home/claude/work/out"
only=sys.argv[1:]
for s,t,m,v,it in T:
    if only and s not in only: continue
    out=f"{O}/ker-reel-{s}-v7.mp4"
    reel4.build(t,it,f"{M}/{m}.mp3",out,vol=v)
    reel4.carousel(it,f"car-{s}",O)
    if s in VO:
        vo=f"/home/claude/work/vo/{s}.mp3"; o2=f"{O}/ker-reel-{s}-v8vo.mp4"
        fc="[1:a]adelay=3200|3200,apad,volume=1.6,asplit=2[vo][key];[0:a][key]sidechaincompress=threshold=0.03:ratio=8:attack=80:release=600[duck];[duck][vo]amix=inputs=2:duration=first:normalize=0,volume=1.5,alimiter=limit=0.95[a]"
        r=subprocess.run(["ffmpeg","-y","-v","error","-i",out,"-i",vo,"-filter_complex",fc,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-movflags","+faststart",o2],capture_output=True,text=True)
        print("VO",s,"OK" if r.returncode==0 else r.stderr[-300:],flush=True)
print("ALL DONE",flush=True)
