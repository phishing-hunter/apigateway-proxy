import os
import boto3
from uuid import uuid4

dynamodb_resource = boto3.resource(
    "dynamodb",
    region_name="ap-northeast-1",
    endpoint_url=os.environ.get("DYNAMODB_ENDPOINT_URL", "https://dynamodb.ap-northeast-1.amazonaws.com"),
)
posts_table = dynamodb_resource.Table("Posts")


def _get_user_id(event):
    user_id = ""
    try:
        user_id = event["requestContext"]["authorizer"]["principalId"]
    except:
        return "anonymous"
    return user_id


def handler(event=None, context=None):
    path = event["resource"]
    method = event["httpMethod"]
    body = event.get("body", "")
    user_id = _get_user_id(event)
    try:
        if path == "/hello" and method == "GET":
            return {
                "statusCode": 200,
                "body": f"hello {user_id}",
            }

        if path == "/post" and method == "POST":
            posts_table.put_item(Item={"post_id": uuid4().hex, "user_id": user_id, "comment": body})
            return {
                "statusCode": 200,
                "body": "ok",
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e),
        }

    return {"statusCode": 404, "body": "function not found."}
