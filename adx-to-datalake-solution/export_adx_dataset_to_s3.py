import json
import boto3
import datetime

client = boto3.client('dataexchange')

def getDataSet(DataSetId):
    try:
        response = client.get_data_set(
        DataSetId=DataSetId
        )
        return response
    except Exception as e:
        return e

def getRevision(DataSetId, RevisionId):
    try:
        response = client.get_revision(
        DataSetId=DataSetId,
        RevisionId=RevisionId
        )
        return response
    except Exception as e:
        return e

def getAsset(AssetId, DataSetId, RevisionId):
    try:
        response = client.get_asset(
        AssetId='string',
        DataSetId='string',
        RevisionId='string'
        )
        return response
    except Exception as e:
        return e

def listRevisionAssets(DataSetId, RevisionId):
    try:
        response = client.list_revision_assets(
        DataSetId=DataSetId,
        MaxResults=123,
        RevisionId=RevisionId
        )
        return response
    except Exception as e:
        return e

def listDataSets():
    try:
        response = client.list_data_sets(
        MaxResults=123,
        Origin="ENTITLED"
        )
        return response
    except Exception as e:
        return e

def listDataSetRevisions(DataSetId):
    try:
        response = client.list_data_set_revisions(
        DataSetId=DataSetId,
        MaxResults=123
        )
        return response
    except Exception as e:
        return e

def createJob(JobConfiguration):
    try:
        response = client.create_job(
        Details=JobConfiguration,
        Type='EXPORT_ASSETS_TO_S3'
        )
        return response
    except Exception as e:
        return e

def startJob(JobId):
    try:
        response = client.start_job(
        JobId=JobId
        )
        return response
    except Exception as e:
        return e

def lambda_handler(event, context):
    DataSetId = event['Id']
    DataLakeRawBucket = ""

    MyDataSetRevisions = listDataSetRevisions(DataSetId)
    MyDataSetRevisionsL = []

    for DataSetRevision in MyDataSetRevisions['Revisions']:
        MyDataSetRevisionsL.append(DataSetRevision['Id'])

    MyRevisionAssets = listRevisionAssets(DataSetId, MyDataSetRevisionsL[0])
    MyRevisionAssetS3Key = MyRevisionAssets['Assets'][0]['Name']
    MyRevisionAssetId = MyRevisionAssets['Assets'][0]['Id']

    JobConfig = {
        'ExportAssetsToS3': {
            'AssetDestinations': [
                {
                    'AssetId': MyRevisionAssetId,
                    'Bucket': DataLakeRawBucket,
                    'Key': MyRevisionAssetS3Key
                },
            ],
            'DataSetId': DataSetId,
            'RevisionId': MyDataSetRevisionsL[0]
            }
        }

    try:
        NewExportJob = createJob(JobConfig)
        startJob(NewExportJob['Id'])
        return "SUCCESS"
    except Exception as e:
        return e
