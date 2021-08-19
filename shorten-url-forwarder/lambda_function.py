import os
import boto3
from botocore.client import Config

S3_BUCKET = os.environ['S3_BUCKET']
# S3 버킷 이름을 담은 변수를 전역변수로 두었고 버킷 이름은 환경변수에 저장을 한다 


def lambda_handler(event, context):
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
    # S3에 접근할 수 있도록 클라이언트를 생성한다

    try:
        shorten_key = "url/" + event.get("pathParameters").get("key")
        # key 라는 값은 어디서 가져올까?
        resp = s3.head_object(Bucket=S3_BUCKET, Key=shorten_key)
        # S3 버킷에서 파일 경로를 Key에 지정한다
        redirect_url = resp.get('WebsiteRedirectLocation')
        # S3 버킷에서 가져온 파일에 대해 WebsiteRedirectLocation 속성의 값을 가져온다.
        # 우리가 원하는 원 URL 값이 된다
    except Exception as e:
        print(e)
        redirect_url = os.environ["HOST"]
        # S3 버킷에 접속하면서 버킷이 존재하지 않거나 연결이 불안정한 이유로 예외가 발생할 수 있다.
        # 이러한 경우를 위해 redirect_url로 서비스의 주소로 가도록 설정하였다

    return {
        "statusCode": 301,
        "headers": {
            "Location": redirect_url
        },
        "isBase64Encoded": False,
    }
    # 301 상태 코드는 요청에 대해 헤더에 주어진 값으로 완전히 옮겨졌음을 나타낸다