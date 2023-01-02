import os
import yaml
import boto3

if os.path.exists('/config/tables.yaml'):
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://dynamodb:8000",
        aws_access_key_id="ACCESS_ID",
        aws_secret_access_key="ACCESS_KEY",
        region_name='us-west-2'
    )

    # テーブル定義を読み込む
    with open('/config/tables.yaml', 'r') as f:
        tables = yaml.safe_load(f)

    for table_name, table_schema in tables.items():
        # テーブルを作成する
        table = dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=table_schema['AttributeDefinitions'],
            KeySchema=table_schema['KeySchema'],
            ProvisionedThroughput=table_schema['ProvisionedThroughput']
        )
