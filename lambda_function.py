import urllib.parse
from io import BytesIO

import boto3
from pikepdf import Pdf

bucketIn = 'bucketinbound'
bucketOut = 'bucketoutbound'

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    if key.endswith('.pdf'):
        bucketObject = s3.get_object(Bucket=bucketIn, Key=key)
        pdf = BytesIO(bucketObject['Body'].read())
        splitPDF(pdf, key)

    # TODO implement
    return {
    'statusCode': 200,
    'body': ''
    }


def splitPDF(fileBytes, key):
    pdf = Pdf.open(fileBytes)
    for n, page in enumerate(pdf.pages):
        bio = BytesIO()
        output = Pdf.new()
        output.pages.append(page)
        output.save(bio)
        writePDF(bio, f'{key.split(".")[0]}_{n+1:03d}.pdf')


def writePDF(bio, objectName):
    print(objectName)
    s3 = boto3.resource('s3')
    boto_bucketOutbound = s3.Bucket(bucketOut)
    bio.seek(0)
    boto_bucketOutbound.upload_fileobj(bio, objectName)
