#!/usr/bin/env python3

import subprocess
import os
from minio import Minio

# Set the necessary variables
todayDate = subprocess.getoutput('date +%Y%m%d-%H%M%S')
logfile = '/var/log/etcd-snapshots.log'
backpath = '/backup/'
minio_endpoint = "IP:Port"  # Update with your Minio endpoint
minio_access_key = "Access_key"  # Update with your Minio access key
minio_secret_key = "Secret_key"  # Update with your Minio secret key
minio_bucket_name = "Bucket_name"  # Update with your Minio bucket name

try:
    # Log the start time
    with open(logfile, 'a') as log:
        log.write(f'{todayDate}\n')

    # Take snapshot from etcd
    subprocess.run([
        '/usr/local/bin/etcdctl',
        '--endpoints=https://IP : Port',
        '--cacert=/etc/ssl/etcd/ssl/ca.pem',
        '--cert=/etc/ssl/etcd/ssl/file.pem',
        '--key=/etc/ssl/etcd/ssl/file-key.pem',
        'snapshot', 'save', f'{backpath}{todayDate}-snapshot.db'
    ])

    # Compress snapshot
    subprocess.run([
        'gzip', '-1', f'{backpath}{todayDate}-snapshot.db'
    ])

    # Upload to Minio
    minio_client = Minio(minio_endpoint,
                         access_key=minio_access_key,
                         secret_key=minio_secret_key,
                         secure=False)
    minio_client.fput_object(minio_bucket_name,
                             f'{todayDate}-snapshot.db.gz',
                             f'{backpath}{todayDate}-snapshot.db.gz')


    # Find and delete old snapshots
    os.system('find {0} -type f -name "*.gz" -mtime +1 -exec rm {{}} \;'.format(backpath))
except Exception as e:
    # Log any errors
    with open(logfile, 'a') as log:
        log.write(f'Error: {str(e)}\n')
