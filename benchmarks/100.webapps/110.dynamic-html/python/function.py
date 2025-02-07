from datetime import datetime
from random import sample
from os import path
from time import time
import os

from jinja2 import Template

from storage import storage

SCRIPT_DIR = path.abspath(path.join(path.dirname(__file__)))

def handler(event):

    # start timing
    name = event.get('username')
    size = event.get('random_len')
    cur_time = datetime.now()
    random_numbers = sample(range(0, 1000000), size)
    storage.ndp_phase('input-read')
    template = Template( open(path.join(SCRIPT_DIR, 'templates', 'template.html'), 'r').read())
    storage.ndp_phase('input-read-done')
    html = template.render(username = name, cur_time = cur_time, random_numbers = random_numbers)
    # end timing
    # dump stats 
    return {'result': html}
