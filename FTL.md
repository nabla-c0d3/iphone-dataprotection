# Introduction #

iOS devices use a software FTL, implemented in iBoot and the kernel. The iOS FTL is based on the Samsung Whimory FTL. Two translation layers are used :
  * VFL (Virtual Flash Layer): low-level layer, handles bad blocks remapping and geometry abstraction
  * FTL: upper FTL layer

![http://wiki.iphone-dataprotection.googlecode.com/hg/ftl_overview.svg](http://wiki.iphone-dataprotection.googlecode.com/hg/ftl_overview.svg)

# FTL versions #

|iOS version|FTL components|Type|
|:----------|:-------------|:---|
|< 3.x|[FTL](LegacyFTL.md)/VFL|Hybrid mapping|
|>= 3.x|[YaFTL](YaFTL.md)/VSVFL|Page mapping|
|>= 4.1, PPN devices|[ApplePPNFTL](ApplePPNFTL.md)/[AppleSwissPPNFTL](AppleSwissPPNFTL.md)|Page mapping|
|>= 7.0, A7 devices|[ASPStorage](ASPStorage.md)|? |



# References #

  * http://www.freemyipod.org/wiki/Nano2G_FTL
  * https://github.com/iDroid-Project/openiBoot
  * http://openembed.googlecode.com/hg/som2416/wince5/SMDK2416_WinCE5.0_PM_MLC_NANDSolution_PortingGuide.pdf
  * [A survey of Flash Translation Layer](http://idke.ruc.edu.cn/people/dazhou/Papers/AsurveyFlash-JSA.pdf)