# API Gateway Proxy

API Gateway + Lambda + DynamoDBの環境をテストするためのモックAPI

## Local Tests
```bash
$ docker-compose up -d --build
$ curl http://localhost:9000/hello
$ curl http://localhost:9000/hello -H "Authorization: xxxxxxxxxxxxx"
$ curl http://localhost:9000/post -XPOST -d 'hoge' -H "Authorization: xxxxxxxxxxxxx"
```
