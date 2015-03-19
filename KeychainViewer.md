<img src='http://wiki.iphone-dataprotection.googlecode.com/hg/KeychainViewer.png' align='right' width='320px' />

GUI application that displays the keychain contents for iOS 3,4 and 5. Source code is available on the [repository](http://code.google.com/p/iphone-dataprotection/source/list?repo=keychainviewer), as well as deb package on the downloads page.

The app runs as root and uses the following entitlements :

```
<key>com.apple.keystore.access-keychain-keys</key>
<true/>
<key>com.apple.keystore.device</key>
<true/>
```

Items using protection classes tied to the user passcode (not always accessible) are displayed in green.