# # from django.db import models
from django.db import models
from common.registration.models import UserProfile
from datetime import datetime, timedelta, date
import uuid
"""
This model contains the following tables:
1. PostLoginTicketStatus
2. PostLoginTicketTypes
3. PostLoginCommonQuestionsByTicketTypes
4. PostLoginTickets
5. PostLoginTicketReplies

"""
# Create your models here.


#
class PostLoginTicketStatus(models.Model):
    status_id = models.AutoField(primary_key=True, default=1)
    status_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.status_id)


#
class PostLoginTicketTypes(models.Model):
    type_id = models.AutoField(primary_key=True, default=1)
    type_name = models.CharField(max_length=100)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.type_id)


#
class PostLoginCommonQuestionsByTicketTypes(models.Model):
    common_question_id = models.AutoField(primary_key=True, default=1)
    common_question_text = models.CharField(max_length=100)
    ticket_type_id = models.ForeignKey(PostLoginTicketTypes, null=True, default=None, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.type_id)


#
class PostLoginTickets(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_type = models.ForeignKey(PostLoginTicketTypes, default=None, null=True, on_delete=models.CASCADE)
    ticket_question = models.ForeignKey(PostLoginCommonQuestionsByTicketTypes, default=None, null=True, on_delete=models.CASCADE)
    ticket_subject = models.CharField(max_length=100)
    ticket_query = models.CharField(max_length=10000, default=datetime.now)
    ticket_owner = models.ForeignKey(UserProfile, default=None, null=True, on_delete=models.CASCADE,  related_name='owner')
    ticket_status = models.ForeignKey(PostLoginTicketStatus, default=None, null=True, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.ForeignKey(UserProfile, default=None, null=True, on_delete=models.CASCADE, related_name='creator')
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.ForeignKey(UserProfile, default=None, null=True, on_delete=models.CASCADE,  related_name='responder')

    def __str__(self):
        return str(self.ticket_id)


#
class PostLoginTicketsReplies(models.Model):
    reply_id = models.AutoField(primary_key=True)
    ticket_id = models.ForeignKey(PostLoginTickets, default=None, null=True, on_delete=models.CASCADE)
    ticket_reply = models.CharField(max_length=10000, default=datetime.now)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.ForeignKey(UserProfile, default=None, null=True, on_delete=models.CASCADE,  related_name='replied_by')
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.ForeignKey(UserProfile, default=None, null=True, on_delete=models.CASCADE,  related_name='editor')

    def __str__(self):
        return str(self.reply_id)
