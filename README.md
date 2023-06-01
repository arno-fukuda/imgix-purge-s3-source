# Python script to bulk purge a list of S3 images from Imgix cache

## Prerequisites
* Python 3

* boto3 and requests library (`pip3 install boto3 requests`)

* AWS CLI installed (https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

* AWS IAM User with **List** and **Get** permission to the bucket and items. You can use the below JSON policy draft.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::<bucket-name>"
        },
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<bucket-name>/*"
        }
    ]
}
```

* AWS CLI configured (`aws config`)

* Imgix API key with purge permission (Create on https://dashboard.imgix.com/api-keys)


## Setup & Execution

* Open `main.py` and navigate to #CONFIGURATION

* Update the IMGIX_API_KEY, IMGIX_SUBDOMAIN and S3_BUCKET_NAME

* Run the script with `python3 main.py`

## Note

In order to not run into any rate limits, the script only sends around 9 purge requests per second.
This means, you can achieve:
* 540 purges in 1 minute
* 16200 purges in 30 minutes
* 32400 purges in 1 hour
