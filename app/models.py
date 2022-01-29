# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    building = models.CharField(max_length=250, unique=True)
    address = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    dob = models.DateField(null=True)
    ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.building


class Exist(models.Model):
    email = models.CharField(max_length=250, unique=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    surname = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    thousand = models.CharField(max_length=250, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    sts = models.BooleanField(default=False)
    ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    address = models.CharField(max_length=250)
    uid = models.ForeignKey(User, related_name="vote_user", on_delete=models.CASCADE, default=1)
    ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    meeting_id = models.CharField(max_length=250, primary_key=True)
    meeting_title = models.CharField(max_length=250)
    meeting_question = models.CharField(max_length=250, null=True)
    meeting_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    meeting_date = models.DateField()
    meeting_time = models.TimeField(auto_now=False, auto_now_add=False)
    meeting_end_detail = models.DateTimeField(null=True, blank=True)
    meeting_sts = models.BooleanField(default=False)
    meeting_no = models.BooleanField(default=False)
    ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.meeting_title


class Meeting_Questions(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    ts = models.DateTimeField(auto_now_add=True)


class Meeting_Question_Logs(models.Model):
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    question = models.ForeignKey(Meeting_Questions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delegated = models.ForeignKey(User, related_name='delegate', on_delete=models.CASCADE, null=True, blank=True)
    answer = models.BooleanField(default=False)
    sts=models.BooleanField(default=False)
    ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.meeting.title


class Daligate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delegated_to = models.ForeignKey(User, related_name='delegate_to', on_delete=models.CASCADE, null=True, blank=True)
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    sts = models.BooleanField()
    delegated_sts = models.BooleanField()


class Attend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    sts=models.BooleanField(default=True)
