from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from db_con import db

person_collection = db['users']
# Create your models here.


