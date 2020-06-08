{
  "Comment": "An example data pipeline using Step Functions and Glue",
  "StartAt": "IngestRawDataSet",
  "States": {
    "IngestRawDataSet": {
      "Comment": "Triggers the lambda function to ingest the raw dataset from ADX",
      "Type": "Task",
      "Resource": "<ingestion lambda function arn>",
      "OutputPath": "$",
      "ResultPath": "$.DataPipelineConfig.Results",
      "Parameters": {
        "DataSetId.$": "$.DataPipelineConfig.DataSetId",
        "DataLakeRawBucket.$": "$.DataPipelineConfig.DataLakeRawBucket",
        "RawCrawlerName.$": "$.DataPipelineConfig.RawCrawlerName",
        "ConvertAndCurateJobName.$": "$.DataPipelineConfig.ConvertAndCurateJobName",
        "CuratedCrawlerName.$": "$.DataPipelineConfig.CuratedCrawlerName"
      },
      "Next": "CrawlRawDataSet"
    },
    "CrawlRawDataSet": {
      "Comment": "Triggers the Glue crawler against the raw dataset",
      "Type": "Task",
      "Resource": "<glue executor lambda function arn>",
      "OutputPath": "$",
      "ResultPath": "$.DataPipelineConfig.Results",
      "Parameters": {
        "CrawlerName.$": "$.DataPipelineConfig.RawCrawlerName"
      },
      "Next": "ConvertAndCurateDataSet"
    },
    "ConvertAndCurateDataSet": {
      "Comment": "Triggers the Glue job to convert and curate the raw dataset",
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "OutputPath": "$",
      "ResultPath": "$.DataPipelineConfig.Results",
      "Parameters": {
        "JobName.$": "$.DataPipelineConfig.ConvertAndCurateJobName"
      },
      "Next": "CrawlCuratedDataSet"
    },
    "CrawlCuratedDataSet": {
      "Comment": "Triggers the Glue crawler against the curated dataset",
      "Type": "Task",
      "OutputPath": "$",
      "ResultPath": "$.DataPipelineConfig.Results",
      "Resource": "<glue executor lambda function arn>",
      "Parameters": {
        "CrawlerName.$": "$.DataPipelineConfig.CuratedCrawlerName"
      },
      "End": true
    }
  }
}
