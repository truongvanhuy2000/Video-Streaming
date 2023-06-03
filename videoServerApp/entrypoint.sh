#!/usr/bin/env bash
## Application-specific logic and mounting NVME storage removed ##
 
## Export NFS Mount
# mkdir /video
# service rpcbind start
# service nfs-common start
# mount -v $NFS_SERVER_IP:/ /video
# ls -a /video

sleep 5
mkdir -p videoServer/resources
cp -a $MOUNT_DIR/* videoServer/resources

chmod -R a+rw videoServer/resources

ls -a videoServer/resources
"python3" -m videoServer