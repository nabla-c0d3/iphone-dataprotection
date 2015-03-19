# Description #

This [technique](http://www.dfrws.org/2008/proceedings/p76-burghardt.pdf) was presented by Aaron Burghardt and Adam J. Feldman in 2008 at the [Digital Forensic Research Workshop](http://www.dfrws.org/) conference.

The idea is to carve the HFS journal file (**/.journal**) to find [catalog file](http://dubeiko.com/development/FileSystems/HFSPLUS/tn1150.html#CatalogFile) entries of deleted files.

# EMF journal carving #

The emf\_undelete tool implements this technique for iOS 4 & 5 data partition images. The only difference with the original method is that we must also search for [cprotect](HFSContentProtection.md) extended attributes in the journal file to be able to decrypt deleted file contents.

Due to the limited size of the journal file (8 megabytes), and the fact that it operates at the block device level, this technique can only recover a limited set of files.