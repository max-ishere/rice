# Rice blocks
*v0.0.1*

A block is a portable piece of code. You can put your color scheme in a block and share it with others. When they import your block they can then choose that color scheme. But in order for this to work any block dependencies must also be installed and anything you want to use from the block should be passed to generators.

Since blocks are just python scripts, please make sure that what you are importing is not malicious. The source code for the block is avaliable in the auto-generated preview.

# Block properties

Properties are simply global variables within the block. This is a sample block file with all the supported fields:

```py
title=''
category=''
author=''
description=''

color_themes=[ ColorTheme() ]
```

# Subdirectories

- `md` - This is where the automatically generated previews go for now. You can generate a preview using `python3 -m rice.block name > rice/block/md/name.md`
