import os,glob
D2="/mnt/user-data/uploads/Media/Photos-1-001 (2)"; D3="/mnt/user-data/uploads/Media/Photos-1-001 (3)"; Z4="/home/claude/newphotos/z4"
def resolve(k):
    if k.startswith('/'): return k
    if k.startswith("z4/"): c=glob.glob(f"{Z4}/IMG_{k[3:]}.*")
    else: c=glob.glob(f"{D2}/IMG_{k}.*")+glob.glob(f"{D3}/IMG_{k}.*")+glob.glob(f"/mnt/user-data/uploads/Media/Photos-1-001 (5)/IMG_{k}.*")
    c=[x for x in c if not x.upper().endswith((".AAE",))]
    return c[0] if c else None
