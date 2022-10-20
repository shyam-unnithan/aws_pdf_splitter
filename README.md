# AWS PDF File Splitter.
This lambda service helps split PDF files into pdfs page wise.

The function is triggered when a file is uploaded in BucketInbound. The following actions are performed
1) Check if the file is pdf
2) If the uploaded file is PDF split the PDF pagewise into multiple PDF's and store it in BucketOutbound
3) Delete the file from BucketInbound
4) Use the first 4 characters of file as department name
5) Upload the information regarding Department, Filename, Number of Pages and TimeStamp to DynamoDB

## AWS policy requirement
Create a role with read write list access to S3 bucket

Create a policy with 
getItems
putItems
deleteItems
listItems

access to DynamoDB

Add the above policies to the role used for running lambda services

## Using PikePDF on AWS
Use the following instruction to create a zip file with the python dependencies</br>

Use <b>CloudShell</b> to run following commands\

`sudo amazon-linux-extras install python 3.8`\
`python 3.8 -m venv venv`\
`source venv/bin/activate`\
`mkdir python`\
`cd python`\
`pip3 install --platform manylinux2014_x86_64 --implementation cp --python 3.9 --only-binary=:all: --upgrade pikepdf -t .`\
`cd ..`\
`zip -r ../slicer-lambda-package.zip python`

Download the zip file

#### Add Layer
Use the zip file downloaded in previous step to add a layer to the lambda service

## Lambda Service
The code for the lambda service is made available in lambda_function.py

## Lambda Invovation
Add a trigger on S3 inbound bucket to trigger the lambda service.