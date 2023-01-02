def get_user_id(event):
    user_id = ""
    try:
        user_id = event["requestContext"]["authorizer"]["principalId"]
    except:
        return ""
    return user_id

def handler(event=None, context=None):
    path = event["resource"]
    method = event["httpMethod"]
    body = event.get("body", "")
    user_id = get_user_id(event)

    if path == "/hello" and method == "GET":
        return {
            "statusCode": 200,
            "body": "hello",
        }

    if path == "/echo" and method == "POST":
        return {
            "statusCode": 200,
            "body": body,
        }

    return {
        "statusCode": 404,
        "body": "function not found."
    }
