import os
from pathlib import Path
import dj_database_url
from .settings import *



DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://jobmatrix_owner:0wD5tnmPdBXF@ep-small-cloud-a1wby35h.ap-southeast-1.aws.neon.tech/jobmatrix?sslmode=require',
        conn_max_age=600
    )
}