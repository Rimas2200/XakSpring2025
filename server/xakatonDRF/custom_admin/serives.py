from ner_model import test

import pprint
import os 
import subprocess
from celery import shared_task

from connectionsbottg import models

def date_model():
    messages = models.SavesTgMessages.objects.get(id=106)
    pprint.pprint(messages.message)
    pprint.pprint("--------------------------------------------------")
    result = test.predict_entities(messages.message)
    pprint.pprint(result)
    
    return result