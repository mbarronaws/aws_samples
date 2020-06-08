import json
import boto3 

client = boto3.client('glue')

def startCrawler(CrawlerName):
    response = client.start_crawler(
    Name=CrawlerName
    )
    return response

def lambda_handler(event, context):
    MyCrawlerName = event['CrawlerName']

    try:
        startCrawler(MyCrawlerName)
        return "SUCCESS"
    except Exception as e: 
        return e
