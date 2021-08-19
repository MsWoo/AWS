import json


def lambda_handler(event, context):
    original_url = event.get("original_url")

    return {
        'original_url': original_url
    }