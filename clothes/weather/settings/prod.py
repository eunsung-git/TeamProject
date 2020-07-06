from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY')

DEBUG = True # 추후에 False로 변경 예정

ALLOWED_HOSTS = [
    '.compute.amazonaws.com',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# S3

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'clothes'
AWS_S3_REGION_NAME = 'ap-northeast-2' # 서울
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_DEFAULT_ACL = None
