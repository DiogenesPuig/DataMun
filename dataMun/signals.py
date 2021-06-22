from datetime import datetime
from django.db.models.signals import *
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import *
from .forms import *


import openpyxl

import string
import datetime

def alphabet():
  return list(string.ascii_uppercase)

"""
@receiver(post_save,sender=Archivo)
def CreateSemana(sender, instance, created, **kwargs):
    archivo = Archivo()
    """
        

@receiver(post_delete, sender=SpreadSheet)
def clientupload_delete(sender, instance, **kwargs):
    if instance.file:
        # Pass false so FileField doesn't save the model.
        instance.file.delete(False)
        
        