from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.STATIC_LOCATION

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIA_LOCATION
    default_acl = 'private'
    custom_domain = False
