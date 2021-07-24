from django.db import models
from datetime import datetime
from common.registration.models import UserProfile
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from common.utilities.file_storage import PublicMediaStorage
from genericfrontend.settings import USER_DEFINED_MEDIA_URL

# Create your models here.
'''
This File Contains Following Tables
1.MediaLibraryStatus
2.MediaLibrary
3.DpStatus
4.Dp
'''


class ExtensionValidator(RegexValidator):
    def __init__(self, extensions, message=None):
        if not hasattr(extensions, '__iter__'):
            extensions = [extensions]
        regex = '\.(%s)$' % '|'.join(extensions)
        if message is None:
            message = 'File type not supported. Accepted types are: %s.' % ', '.join(
                extensions)
        super(ExtensionValidator, self).__init__(regex, message)

    def __call__(self, value):
        super(ExtensionValidator, self).__call__(value.name)

    def validate_file_size(fieldfile_obj):
        filesize = fieldfile_obj.size
        megabyte_limit = 100.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" %
                                  str(megabyte_limit))


def user_directory_path(instance, file_content):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}/'.format(instance.file_owner_profile_id, file_content)


class MediaLibraryStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)
    added_by = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.status_id)


class MediaLibrary(models.Model):
    media_id = models.AutoField(primary_key=True)
    media_type = models.CharField(max_length=50, default="image")
    file_content = models.FileField(storage=PublicMediaStorage(), upload_to=user_directory_path, blank=False, null=False)
    file_caption = models.CharField(max_length=100, default="default", blank=True)
    file_owner_profile_id = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE)
    media_static_path = models.CharField(
        max_length=1000, default=USER_DEFINED_MEDIA_URL, blank=True)
    # ForeignKey of medias_status table
    status = models.ForeignKey(MediaLibraryStatus, on_delete=models.CASCADE)
    added_by = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.media_id)


class DpStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default="not defined")
    added_by = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.status_id)


class Dp(models.Model):
    dp_id = models.AutoField(primary_key=True)
    profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    media_id = models.ForeignKey(MediaLibrary, on_delete=models.CASCADE)
    status_id = models.ForeignKey(DpStatus, on_delete=models.CASCADE)
    added_by = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.dp_id)
