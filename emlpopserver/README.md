This script was created for a situation where I was required to move from 
Thunderbird to Outlook email user agents. This is a minimal *one shot* tool
that is neither robust nor well tested.

My memory is hazy, but I believe I exported the folders from Thunderbird as
directories of .eml files and then ran this script and connected Outlook to
the fake pop server running on the local machine at port `1110`.

When I was done I replaced the fake pop server with the real network POP
server.

I believe I used the [mbox-eml-extractor.exe](http://www.outlookimport.com/updated-version-of-mbox-email-extractor-mbox-converter/)
tool to export the Thunderbird folders. Which is ironic, as I wrote this script
in response to the fact the makers of [Outlook Import Wizard](http://www.outlookimport.com/description/outlook-import-wizard/)
had updated the tool so I could no longer use it, as the license was for a previous
version which they no longer offered for download.
