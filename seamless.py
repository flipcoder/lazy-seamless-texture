#!/usr/bin/env python3

import sys
from PIL import Image

for img_fn in sys.argv[1:]:
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
    img.save(img_fn.replace(".","_seamless."))

