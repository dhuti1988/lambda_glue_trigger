import json
import os
import boto3
from urllib.parse import unquote_plus

glue = boto3.client("glue")

def trigger_glue_crawler(glue_client, crawler_name: str) -> None:
    crawler_info = glue_client.get_crawler(Name=crawler_name)
    state = crawler_info["Crawler"]["State"]

    if state == "READY":
        glue_client.start_crawler(Name=crawler_name)
        print(f"Crawler {crawler_name} started successfully.")
    else:
        print(f"Crawler {crawler_name} is in state {state}. Skipping trigger.")

def lambda_handler(event, context):
    crawler_order = os.getenv("CRAWLER_NAME_CUSTOMER_ORDER")
    crawler_master = os.getenv("CRAWLER_NAME_CUSTOMER_MASTER")
    if not crawler_order or not crawler_master:
        raise RuntimeError("Missing required env vars: CRAWLER_NAME_CUSTOMER_ORDER / CRAWLER_NAME_CUSTOMER_MASTER")

    try:
        record = event["Records"][0]
        key = unquote_plus(record["s3"]["object"]["key"])
        bucket = record["s3"]["bucket"]["name"]
    except Exception:
        return {"statusCode": 400, "body": json.dumps("Invalid/non-S3 event")}

    print(f"New file detected: bucket={bucket}, key={key}")

    if "customer_order" in key:
        trigger_glue_crawler(glue, crawler_order)
        target = "customer_order"
    elif "customer_master" in key:
        trigger_glue_crawler(glue, crawler_master)
        target = "customer_master"
    else:
        return {"statusCode": 200, "body": json.dumps("No matching prefix; skipped")}

    return {"statusCode": 200, "body": json.dumps(f"Crawler trigger completed for {target}")}