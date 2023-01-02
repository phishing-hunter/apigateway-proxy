# API Gateway Proxy

API Gateway + Lambda + DynamoDBの環境をテストするための環境

## Local Tests
```bash
$ docker-compose up -d --build
$ curl http://localhost:9000/hello
$ curl http://localhost:9000/echo -XPOST -d 'hoge' 
```
