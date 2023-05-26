#!/usr/bin/env bash
## Application-specific logic and mounting NVME storage removed ##
 
## Export NFS Mount
# mkdir /video
# service rpcbind start
# service nfs-common start
# mount -v $NFS_SERVER_IP:/ /video
# ls -a /video

MOUNT_SUCCESS=false
MOUNT_DIR=videoServer/sharedResources

while [ $MOUNT_SUCCESS = false ]; do
    
    mount $NFS_SERVER_IP:/ $MOUNT_DIR

    if [ $? -eq 0 ]; then
        echo "Mount sucessfully"
        MOUNT_SUCCESS=true
    else
        echo "Mount failed. Retrying in 10 seconds..."
        sleep 10
    fi
done

cp -a $MOUNT_DIR/* videoServer/resources

chmod -R a+rw videoServer/resources

ls -a videoServer/resources
"python3" -m videoServer