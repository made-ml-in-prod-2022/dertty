import datetime
import secrets
import csv
from io import StringIO
from fastapi.responses import StreamingResponse
from typing import List, Optional
from sqlalchemy import func, or_

import numpy as np
import pytz
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File
from fastapi.responses import StreamingResponse
from jinja2 import utils
from sklearn.metrics import accuracy_score, mean_absolute_error, roc_auc_score
from sqlalchemy.orm import Session, aliased

from api.api_v1.core.credentials import API_ACCESS_TOKEN
from api.api_v1.core.database import get_db
from api.api_v1.core.functions.s3 import get_file_from_s3, save_file_to_s3, get_file_from_s3_bytes
from api.api_v1.core.models import schemas, models
from api.api_v1.core.models.crud import crud, submits, users, teams
from api_versioning import versioned_api_route


router = APIRouter(route_class=versioned_api_route(1, 0))

@router.post(
    "/health",
    summary="Проверка",
)
def health():
    return 200