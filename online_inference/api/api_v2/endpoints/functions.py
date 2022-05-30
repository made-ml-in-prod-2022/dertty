import datetime
import secrets
from io import StringIO
from typing import List, Optional

import numpy as np
import pytz
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File
from passlib.hash import pbkdf2_sha256
from sklearn.metrics import accuracy_score
from sqlalchemy.orm import Session

from core.credentials import API_ACCESS_TOKEN
from core.database import get_db
from core.functions.s3 import get_file_from_s3, save_file_to_s3
from core.models import schemas
from core.models.crud import crud, submits, users, hackathons

from api_versioning import versioned_api_route


router = APIRouter(route_class=versioned_api_route(2, 0))
