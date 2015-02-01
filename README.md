# GooDSync
This project uses Google Drive API to create a snapshot of a directory.
GooDSync  provides an example use case that takes  advantage of the api in order to perform a backup/recovery action.

## Download

* Clone on GitHub:
  - git clone https://github.com/adispataru/GooDSync.git
  
* Download zip:
  - get https://github.com/adispataru/GooDSync/archive/master.zip
  
## Install
1. Change into the root directory of the project
2. Run 'python setup.py install'

## Use 

* To create a backup for the Pictures folder run:
  - ~$goodsync --backup /home/ubuntu/Pictures pictures.2.1.15
  
* To later recover the data run:
  - ~$goodsync --recover pictures.2.1.15 /home/ubuntu/Pictures
