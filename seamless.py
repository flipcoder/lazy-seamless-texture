#!/usr/bin/env python3

import sys
import os
from PIL import Image

def rreplace(s, match, repl, count=1):
    return repl.join(s.rsplit(match, count))

for img_fn in sys.argv[1:]:
    # ignore generated files
    if img_fn.find("_seamless.") != -1:
        continue
    
    simg_fn = rreplace(img_fn, ".", "_seamless.")
    
    # seamless version already exists, dont regenerate
    if os.path.isfile(simg_fn):
        print("Seamless image already exists, ignoring %s..." % img_fn)
        continue
    
    img = Image.open(img_fn)
    print("Converting %s..." % img_fn)
    sz = img.size
    region = []
    for i in range(4):
        region += [img.crop((0,0,sz[0],sz[1]))]
    img = img.resize((sz[0] * 2, sz[1] * 2))
    
    region[1] = region[1].transpose(Image.FLIP_TOP_BOTTOM)
    
    region[2] = region[2].transpose(Image.FLIP_LEFT_RIGHT)
    
    region[3] = region[3].transpose(Image.FLIP_TOP_BOTTOM)
    region[3] = region[3].transpose(Image.FLIP_LEFT_RIGHT)
    
    img.paste(region[0], ((0,0,sz[0],sz[1])))
    img.paste(region[1], ((0,sz[1],sz[0],sz[1]*2)))
    img.paste(region[2], ((sz[0],0,sz[0]*2,sz[1])))
    img.paste(region[3], ((sz[0],sz[1],sz[0]*2,sz[1]*2)))
    img.save(simg_fn)

