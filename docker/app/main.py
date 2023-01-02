import os
import json
import base64
import requests
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

LAMBDA_URL = os.environ.get("LAMBDA_URL", "http://lambda:8080")
TEST_SUB = os.environ.get("TEST_SUB", "test_user")
TEST_NAME = os.environ.get("TEST_NAME", "test")

def parse_jwt(jwt):
    payload = {"sub": TEST_SUB, "name": TEST_NAME}
    try:
        tmp = jwt.split(".")
        payload = json.loads(base64.b64decode(tmp[1]).decode())
    except Exception as e:
        print(e)
    return payload


class BaseHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        payload = parse_jwt(self.headers["Authorization"])
        post_json = {
            "requestContext": {
                "authorizer": {
                    "principalId": payload["sub"],
                }
            },
            "headers": {
                "Authorization": "test_token"
            },
            "resource": self.path,
            "httpMethod": "GET",
            "body": "",
        }
        r = requests.post(
            f"{LAMBDA_HOST}/2015-03-31/functions/function/invocations",
            data=json.dumps(post_json),
        )
        resp = r.json()
        self.send_response(resp["statusCode"])
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent,X-Amzn-Trace-Id",
        )
        self.end_headers()
        body = resp["body"]
        self.wfile.write(body.encode())

    def do_POST(self):
        payload = parse_jwt(self.headers["Authorization"])
        content_len = int(self.headers.get("content-length").encode())
        requestBody = self.rfile.read(content_len).decode("utf-8")
        post_json = {
            "requestContext": {
                "authorizer": {
                    "principalId": payload["sub"],
                }
            },
            "headers": {
                "Authorization": "test_token"
            },
            "resource": self.path,
            "httpMethod": "POST",
            "body": requestBody,
        }
        r = requests.post(
            "http://lambda:8080/2015-03-31/functions/function/invocations",
            data=json.dumps(post_json),
        )
        resp = r.json()
        body = resp["body"]
        self.send_response(resp["statusCode"])
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent,X-Amzn-Trace-Id",
        )
        self.end_headers()
        self.wfile.write(body.encode())

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("content-length", 0)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent,X-Amzn-Trace-Id",
        )
        self.end_headers()


ip = "0.0.0.0"
port = 8080

server = HTTPServer((ip, port), BaseHttpServer)
server.serve_forever()
