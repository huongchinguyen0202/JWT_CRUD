from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tag_groups(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=200)
    code = models.IntegerField(unique=True)

    # class Meta:
    #     managed = False
    #     db_table = 'gtiauth_tag_groups'

class Tags(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=200)
    tag_group_id = models.ForeignKey(Tag_groups, on_delete = models.DO_NOTHING)

    # class Meta:
    #     managed = False
    #     db_table = 'gtiauth_tags'

class User(AbstractUser):
    avatar = models.ImageField(upload_to ='avatar/', height_field=200, width_field=200, blank=True, null=True)
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    street_address = models.CharField(max_length=200, blank=True, null=True)
    apartment_number = models.CharField(max_length=200, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    tag_category_id = models.ForeignKey(Tags, on_delete = models.DO_NOTHING, blank=True, null=True)
    creator_id = models.ForeignKey('self', on_delete = models.DO_NOTHING, blank=True, null=True)

    # class Meta:
    #     managed = False
    #     db_table = 'gtiauth_user'

class User_tags(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    tag_id = models.ForeignKey(Tags, on_delete = models.DO_NOTHING)

    # class Meta:
    #     managed = False
    #     db_table = 'gtiauth_user_tags'