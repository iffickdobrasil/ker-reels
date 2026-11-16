import os,glob
U="/mnt/user-data/uploads/Kermenhir/Media"
def resolve(k):
    if k.startswith('/'): return k
    if k.startswith("z4/"): c=glob.glob(f"/tmp/z4/IMG_{k[3:]}.*")
    else: c=glob.glob(f"{U}/Photos-1-001 (*)/IMG_{k}.*")+glob.glob(f"{U}/IMG_{k}.*")
    c=[x for x in c if not x.upper().endswith(".AAE")]
    img=[x for x in c if x.upper().endswith((".HEIC",".JPG",".JPEG",".PNG"))]
    c=img or c
    return c[0] if c else None
