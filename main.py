import boto3
import requests
import json

# CONFIGURATION
# Issue key with purge permission from https://dashboard.imgix.com/api-keys
IMGIX_API_KEY = '<API_KEY>'

IMGIX_SUBDOMAIN = '<EXAMPLE>'  # https://<SUBDOMAIN>.imgix.net/path/image.jpg

S3_BUCKET_NAME = '<BUCKET_NAME>'


# Variable initialization
API_ENDPOINT = "https://api.imgix.com/api/v1/purge"

s3 = boto3.client('s3')
purge_count = 0
skipped_count = 0
other_status = {}

headers = {
    "Authorization": f"Bearer {IMGIX_API_KEY}",
    "Content-Type": "application/vnd.api+json",
}

payload = {
    "data": {
        "type": "purges",
        "attributes": {
            "url": '',
            "sub_image": False,
        }
    }
}

# Retrieve list of all items in S3 bucket
s3_response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)

# Iterage through list and send purge request for each item.
for item in s3_response['Contents']:
    if not item['Key'].endswith('/'):
        payload['data']['attributes']['url'] = f"https://{IMGIX_SUBDOMAIN}.imgix.net/{item['Key']}"
        response = requests.post(
            url=API_ENDPOINT, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            purge_count += 1
        elif response.status_code == 404:
            skipped_count += 1
        else:
            if response.status_code not in other_status:
                other_status[response.status_code] = 1
            else:
                other_status[response.status_code] += 1

# Print result
print(f'{purge_count} assets were purged from cache. \n{skipped_count} assets were already removed. \nOther responses:{other_status}')
