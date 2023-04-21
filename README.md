# etcd Snapshot Backup to Minio

This Python script creates a backup of an etcd snapshot and uploads it to a Minio object storage server for storage. It also deletes old snapshots that are older than 1 day.

### Prerequisites

    Python 3 installed
    Minio Python client library (minio) installed
    etcdctl command-line tool installed

### Usage

    Update the following variables in the script according to your environment:
        todayDate: The current date and time, used as a timestamp for the snapshot filename.
        logfile: The path to the log file where logs will be written.
        backpath: The directory where the snapshots will be stored.
        minio_endpoint: The URL of your Minio endpoint.
        minio_access_key: The access key for your Minio server.
        minio_secret_key: The secret key for your Minio server.
        minio_bucket_name: The name of the bucket in your Minio server where the snapshots will be uploaded.
        subprocess.run() commands: Update the etcdctl command with the appropriate parameters for your etcd setup, such as endpoints, certificates, and keys.
    Run the script using Python 3: python3 backup.py

### Functionality

The script performs the following steps:

    Writes the start time of the backup to the log file.
    Creates a snapshot of etcd using the etcdctl command-line tool with the provided parameters, and saves it to a file in the specified backpath directory with the format <todayDate>-snapshot.db.
    Compresses the snapshot using gzip.
    Uploads the compressed snapshot to the specified Minio bucket using the Minio Python client library.
    Deletes old snapshots that are older than 1 day from the backpath directory using the find command.
    Logs any errors encountered during the process to the log file.

#### Note: The script uses insecure connection to Minio (secure=False) for demonstration purposes. It is recommended to use a secure connection in a production environment.
