from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    age: Optional[int] = None
    sex: Optional[int] = None
    cp: Optional[int] = None
    trestbps: Optional[int] = None
    chol: Optional[int] = None
    fbs: Optional[int] = None
    restecg: Optional[int] = None
    thalach: Optional[int] = None
    exang: Optional[int] = None
    oldpeak: Optional[float] = None
    slope: Optional[int] = None
    ca: Optional[int] = None
    thal: Optional[int] = None