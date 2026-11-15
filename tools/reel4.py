# -*- coding: utf-8 -*-
import os, subprocess, sys
from PIL import Image, ImageOps, ImageEnhance
import pillow_heif; pillow_heif.register_heif_opener()
sys.path.insert(0,"/home/claude/work")
from resolve import resolve
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
fps=30; W,H=1080,1920
EQ="eq=contrast=1.06:brightness=0.045:saturation=1.10"
WORK="/home/claude/work"; CROP=f"{WORK}/reelcrop4"; os.makedirs(CROP,exist_ok=True)
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print("ERR",r.stderr[-800:],flush=True)
    return r.returncode==0
def load(k):
    return ImageOps.exif_transpose(Image.open(resolve(k))).convert("RGB")
def fit(im,w,h,fx=0.5):
    sc=max(w/im.width,h/im.height); im=im.resize((round(im.width*sc),round(im.height*sc)),Image.LANCZOS)
    x=int((im.width-w)*fx); y=(im.height-h)//2; return im.crop((x,y,x+w,y+h))
def crop_photo(k,fx=0.5):
    out=f"{CROP}/{k.replace('/','_')}_{fx}.jpg"
    if not os.path.exists(out): fit(load(k),W,H,fx).save(out,quality=92)
    return out
def esc(t): return t.replace(":","\\:").replace("'","\u2019").replace("%","\\%")
def build(title, items, music, out, seg=4.6, tr=0.45, vol=0.6):
    """items: list of dict(k=id, cap=str, ss=float for video, fx=crop x position 0..1)"""
    SEG=f"{WORK}/seg4"; os.makedirs(SEG,exist_ok=True)
    for f in os.listdir(SEG): os.remove(os.path.join(SEG,f))
    segs=[]; N=int(seg*fps)
    for i,it in enumerate(items):
        s=f"{SEG}/s{i}.mp4"; src=resolve(it["k"]); fx=it.get("fx",0.5)
        if src.upper().endswith((".MOV",".MP4")):
            # vidéo paysage -> 9:16, légère poussée de zoom lisse
            cx=f"(iw-{W})*{fx}"
            vf=(f"scale=-2:{H}:flags=lanczos,crop={W}:{H}:{cx}:0,"
                f"scale={W*2}:{H*2}:flags=lanczos,zoompan=z='1+0.04*on/{N}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={fps},{EQ},format=yuv420p")
            ok=run(["ffmpeg","-y","-hide_banner","-loglevel","error","-ss",str(it.get("ss",0)),"-i",src,"-an",
                "-vf",vf,"-frames:v",str(N),"-c:v","libx264","-preset","medium","-crf","18","-r",str(fps),s])
        else:
            img=crop_photo(it["k"],fx)
            zexpr=f"1+0.08*on/{N}" if i%2==0 else f"1.08-0.08*on/{N}"
            vf=f"scale={W*4}:{H*4}:flags=lanczos,zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={fps},{EQ},format=yuv420p"
            ok=run(["ffmpeg","-y","-hide_banner","-loglevel","error","-loop","1","-i",img,
                "-vf",vf,"-frames:v",str(N),"-c:v","libx264","-preset","veryfast","-crf","18","-r",str(fps),s])
        if not ok: print("seg fail",i,it); return False
        segs.append(s)
    trans=["fade","smoothleft","slideup","smoothright","circleopen","dissolve"]
    ins=[]; [ins.extend(["-i",p]) for p in segs]
    fc=[f"[{i}:v]setsar=1,fps={fps},format=yuv420p[c{i}]" for i in range(len(segs))]
    prev="c0"; T=seg; starts=[0.0]
    for i in range(1,len(segs)):
        off=T-tr; fc.append(f"[{prev}][c{i}]xfade=transition={trans[(i-1)%6]}:duration={tr}:offset={off:.3f}[x{i}]")
        prev=f"x{i}"; starts.append(off); T=T+seg-tr
    total=T
    d=(f"[{prev}]drawtext=fontfile='{FONT}':text='@kermenhir':fontcolor=white:fontsize=34:x=(w-text_w)/2:y=1450:box=1:boxcolor=0x0B2D5B@0.75:boxborderw=12"
       f",drawtext=fontfile='{FONT}':text='KERMENHIR':fontcolor=white:fontsize=96:x=(w-text_w)/2:y=h*0.38:box=1:boxcolor=0x0B2D5B@0.8:boxborderw=26:enable='between(t,0.3,3.0)'"
       f",drawtext=fontfile='{FONT}':text='{esc(title)}':fontcolor=0x0B2D5B:fontsize=42:x=(w-text_w)/2:y=h*0.38+150:box=1:boxcolor=white@0.88:boxborderw=16:enable='between(t,0.3,3.0)'")
    for i,it in enumerate(items):
        if it.get("cap"):
            a=starts[i]+(0.35 if i==0 else tr+0.35); b=starts[i]+seg-0.2
            if i==0: a=3.1
            d+=f",drawtext=fontfile='{FONT}':text='{esc(it['cap'])}':fontcolor=white:fontsize=54:x=(w-text_w)/2:y=1330:box=1:boxcolor=0x0B2D5B@0.75:boxborderw=20:enable='between(t,{a:.2f},{b:.2f})'"
    d+=f",drawtext=fontfile='{FONT}':text='kermenhir.bzh':fontcolor=0x0B2D5B:fontsize=62:x=(w-text_w)/2:y=h*0.47:box=1:boxcolor=white@0.88:boxborderw=24:enable='between(t,{total-2.6:.2f},{total-0.2:.2f})'"
    d+=f",fade=t=in:st=0:d=0.4,fade=t=out:st={total-0.7:.2f}:d=0.7[v]"
    fc.append(d)
    tmpv=f"{SEG}/_novid.mp4"
    if not run(["ffmpeg","-y","-hide_banner","-loglevel","error"]+ins+["-filter_complex",";".join(fc),
        "-map","[v]","-c:v","libx264","-preset","medium","-crf","23","-maxrate","3M","-bufsize","6M","-pix_fmt","yuv420p","-r",str(fps),"-movflags","+faststart",tmpv]): return False
    af=f"[1:a]atrim=0:{total:.2f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.6,afade=t=out:st={total-1.0:.2f}:d=1.0,volume={vol}[a]"
    ok=run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",tmpv,"-i",music,"-filter_complex",af,
        "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",out])
    print("OUT",out,"OK" if ok else "FAIL",f"{total:.1f}s",flush=True); return ok
def carousel(items, slugbase, outdir):
    """4:5 1080x1350 jpgs; video items -> frame at ss+1.5s"""
    outs=[]
    for j,it in enumerate(items):
        out=f"{outdir}/ker-{slugbase}-{j+1}.jpg"; outs.append(os.path.basename(out))
        if os.path.exists(out): continue
        src=resolve(it["k"])
        if src.upper().endswith((".MOV",".MP4")):
            fr=f"{WORK}/seg4/_frame.jpg"
            run(["ffmpeg","-y","-hide_banner","-loglevel","error","-ss",str(it.get("ss",0)+1.5),"-i",src,"-frames:v","1","-q:v","2",fr])
            im=Image.open(fr).convert("RGB")
        else: im=load(it["k"])
        im=fit(im,1080,1350,it.get("fx",0.5))
        im=ImageEnhance.Color(im).enhance(1.08); im=ImageEnhance.Brightness(im).enhance(1.05); im=ImageEnhance.Contrast(im).enhance(1.04)
        q=90; im.save(out,quality=q,optimize=True)
        while os.path.getsize(out)>1_000_000 and q>70: q-=5; im.save(out,quality=q,optimize=True)
    return outs
