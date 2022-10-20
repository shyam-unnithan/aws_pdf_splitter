import time
import urllib.parse
from io import BytesIO

import boto3
from pikepdf import Pdf

bucketIn = 'bucketinbound'
bucketOut = 'bucketoutbound'
ts = time.time()


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    if key.endswith('.pdf'):
        bucketObject = s3.get_object(Bucket=bucketIn, Key=key)
        pdf = BytesIO(bucketObject['Body'].read())
        totalPages = splitPDF(pdf, key)
        dept = key[0:4]
        updateDynamoDB(dept, ts, key, totalPages)
        s3.delete_object(Bucket=bucketIn, Key=key)

    # TODO implement
    return {
    'statusCode': 200,
    'body': ''
    }


def splitPDF(fileBytes, key):
    pdf = Pdf.open(fileBytes)
    totalPages = len(pdf.pages)
    for n, page in enumerate(pdf.pages):
        bio = BytesIO()
        output = Pdf.new()
        output.pages.append(page)
        output.save(bio)
        writePDF(bio, f'{key.split(".")[0]}_{n+1:03d}.pdf')
    return totalPages


def writePDF(bio, objectName):
    s3 = boto3.resource('s3')
    boto_bucketOutbound = s3.Bucket(bucketOut)
    bio.seek(0)
    boto_bucketOutbound.upload_fileobj(bio, objectName)

def updateDynamoDB(dept, ts, filename, totalPages):
    dynamoDB = boto3.client('dynamodb')
    dynamoDB.put_item(TableName = 'PDFSlicer', Item = {'Department' : {'S': dept}, 'Timestamp' : {'S':str(ts)}, 'FileName' : {'S': filename }, 'Pages' : {'N' : str(totalPages)}})
    