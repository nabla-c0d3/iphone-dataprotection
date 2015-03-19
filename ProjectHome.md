Tools and informations on iOS 3/4/5/6/7 data protection features.

Slides for our talk at [HITB 2011 Amsterdam](http://conference.hackinthebox.org/hitbsecconf2011ams/) are available [here](http://conference.hackinthebox.org/hitbsecconf2011ams/materials/D2T2%20-%20Jean-Baptiste%20Be%cc%81drune%20&%20Jean%20Sigwald%20-%20iPhone%20Data%20Protection%20in%20Depth.pdf).

The [main repository](http://code.google.com/p/iphone-dataprotection/source/browse?repo=default) contains tools to create a forensics ramdisk, bruteforce simple passcodes (4 digits) and decrypt iTunes backups.

A modified version of [HFSExplorer](http://www.catacombae.org/hfsx.html) uses output from the ramdisk tools to process iOS data partition images ([source code](http://code.google.com/p/iphone-dataprotection/source/list?repo=hfsexplorer)).

The KeychainViewer application can be installed on a jailbroken device to inspect keychain items and their protection classes.

**UPDATE**: disk images can be decrypted permanently using the [emf decrypter](http://code.google.com/p/iphone-dataprotection/source/browse/python_scripts/emf_decrypter.py) tool.

  * [iOS 5 updates](http://esec-lab.sogeti.com/post/iOS-5-data-protection-updates)
  * [Low-level iOS forensics](http://esec-lab.sogeti.com/post/Low-level-iOS-forensics)
  * [Apple - iOS Security - May 2012](http://images.apple.com/ipad/business/docs/iOS_Security_May12.pdf)
  * [SEC-T 2012 - iPhone raw NAND recovery and forensics - Torbjörn Lofterud](http://www.youtube.com/watch?v=5Es3wRSe3kY)