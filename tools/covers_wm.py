import sys,os,glob; sys.path.insert(0,'/home/claude/work')
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from reel4 import load, fit
P="/home/claude/ker-photos"; FD="/usr/share/fonts/opentype/inter/"
# watermark
wf=ImageFont.truetype(FD+"Inter-SemiBold.otf",34)
for f in sorted(glob.glob(f"{P}/ker-car-*.jpg")):
    if f.endswith("-wm.jpg"): continue
    out=f[:-4]+"-wm.jpg"
    if os.path.exists(out): continue
    im=Image.open(f).convert("RGBA"); t="@kermenhir"
    tw=wf.getbbox(t)[2]; x=im.width-40-tw; y=im.height-56-34
    sh=Image.new("RGBA",im.size,(0,0,0,0)); ImageDraw.Draw(sh).text((x+2,y+2),t,font=wf,fill=(0,0,0,110)); sh=sh.filter(ImageFilter.GaussianBlur(3))
    im=Image.alpha_composite(im,sh); ov=Image.new("RGBA",im.size,(0,0,0,0)); ImageDraw.Draw(ov).text((x,y),t,font=wf,fill=(255,255,255,204))
    im=Image.alpha_composite(im,ov).convert("RGB"); q=90; im.save(out,quality=q,optimize=True)
    while os.path.getsize(out)>1_000_000 and q>70: q-=5; im.save(out,quality=q,optimize=True)
# covers
C={"goudoul":("7877","Les rochers\ndu Goudoul"),"arcenciel":("9111","Après\nla pluie"),"couchant":("8063","Couchers\nde soleil"),
"perdrix":("2072","Loctudy,\ncôté port"),"riviere":("8156","Au fil\nde la rivière"),"kervilzic":("2167","Plage de\nKervilzic"),
"lune":("z4/6023","Nuits de\npleine lune"),"gourmandises":("5381","Saveurs\nbretonnes"),"sentier":("7863","Le sentier\ncôtier"),
"feu":("8138","Au coin\ndu feu"),"brume":("z4/5742","Matins\nde brume"),"balades":("8202","Balades\nau domaine"),"pontlabbe":("2274","Pont-l’Abbé,\npays bigouden")}
tf=ImageFont.truetype(FD+"Inter-ExtraBold.otf",112); kf=ImageFont.truetype(FD+"Inter-Medium.otf",34)
for slug,(k,title) in C.items():
    im=fit(load(k),1080,1920); im=ImageEnhance.Color(im).enhance(1.08).convert("RGBA")
    veil=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(veil)
    for y in range(500,1450): d.line([(0,y),(1080,y)],fill=(0,0,0,int(90*(1-abs(y-960)/480))))
    im=Image.alpha_composite(im,veil)
    tx=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(tx)
    tag="KERMENHIR  ·  FINISTÈRE SUD"; tw=d.textlength(tag,font=kf); d.text(((1080-tw)/2,760),tag,font=kf,fill=(255,255,255,235))
    y=830
    for line in title.split("\n"):
        lw=d.textlength(line,font=tf); d.text(((1080-lw)/2,y),line,font=tf,fill="white"); y+=128
    d.rounded_rectangle((490,y+30,590,y+40),radius=5,fill=(30,110,200,255))
    sh=tx.filter(ImageFilter.GaussianBlur(6)); shadow=Image.new("RGBA",im.size,(0,0,0,0)); shadow.putalpha(sh.split()[3].point(lambda a:a*0.55))
    im=Image.alpha_composite(Image.alpha_composite(im,shadow),tx).convert("RGB")
    im.save(f"{P}/ker-cover-{slug}.jpg",quality=88,optimize=True)
print("ok")
