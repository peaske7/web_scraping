import logging
from datetime import datetime

import boto3
import botocore
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region, ACL_type):
    try:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(ACL=ACL_type, Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        print(str(e))
        return False
    return True


def s3_upload(s3_bucket_name, local_filename, s3_keyname):
    s3 = boto3.client('s3')

    for attempt in range(1, 6):
        try:
            # files automatically upload parts in parallel
            s3.upload_file(local_filename, s3_bucket_name, s3_keyname)
        except Exception as e:
            print(str(e))
        else:
            print('finished uploading to s3 in attempt ', attempt)


def get_last_mod_file(s3_bucket_name, file_type=None, substring_to_match=''):
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(s3_bucket_name)
    last_modified_date = datetime(1939, 9, 1).replace(tzinfo=None)

    if any(my_bucket.objects.all()) is False:
        last_modified_file = 'None'
    for file in my_bucket.objects.all():
        file_date = file.last_modified.replace(tzinfo=None)
        file_name = file.key
        if file_type is None:
            if last_modified_date < file_date and substring_to_match in \
                    file_name:
                last_modified_date = file_date
                last_modified_file = file_name
        else:
            if last_modified_date < file_date and substring_to_match \
                    in file_name and file_type == file_name.split('.')[-1]:
                last_modified_date = file_date
                last_modified_file = file_name
    return last_modified_file


def download_file_from_s3(s3_bucket_name, s3_keyname, local_filename):
    s3 = boto3.resource('s3')
    for attempt in range(1, 6):
        try:
            s3.meta.client.download_file(s3_keyname, s3_keyname, local_filename)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print('The object does not exist')
        except Exception as e:
            print(e)
            logging.info(str(e))
        else:
            print('downloaded successfully on attempt ', attempt)
            break


# deleting an object
#
# s3 = boto3.client('s3')
# bucket_name = '<bucket_name>'
# key_name = '<key_name>'
# response = s3.delete_object(Bucket=bucket_name, Key=key_name)


def delete_all_objects(bucket_name):
    result = []
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    for obj_version in bucket.objects_versions.all():
        result.append({'Key': obj_version.object_key, 'VersionId': obj_version.id})
    print(result)
    bucket.delete_objects(Delete={'Objects': result})


def delete_bucket(bucket_name):
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    if any(my_bucket.objects.all()) is True:
        delete_all_objects(bucket_name)
    my_bucket.delete()
    return True


def list_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    for bucket in response['Buckets']:
        print({bucket['Name']})
        print('*' * 10)
