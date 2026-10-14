from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, field_validator, model_validator


class JobPosting(BaseModel):
    posting_id: str
    source: Literal["remotive", "kaggle_pk"]
    source_url: Optional[str] = None
    title: str
    description: str
    company_name: Optional[str] = None
    category: Optional[str] = None
    tags: list[str] = []
    city: Optional[str] = None
    country: Optional[str] = None
    candidate_location: Optional[str] = None
    work_mode: Literal["remote", "onsite", "hybrid", "unknown"] = "unknown"
    employment_type: Optional[str] = None
    experience: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    salary_text: Optional[str] = None
    posted_at: Optional[datetime] = None

    @field_validator("title", "description")
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be empty")
        return v

    @field_validator("salary_min", "salary_max")
    @classmethod
    def non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("salary must not be negative")
        return v

    @field_validator("posted_at")
    @classmethod
    def not_in_future(cls, v):
        if v is None:
            return v
        now = datetime.now(v.tzinfo) if v.tzinfo else datetime.now()
        if v > now:
            raise ValueError("posted_at is in the future")
        return v

    @model_validator(mode="after")
    def salary_order(self):
        if self.salary_min is not None and self.salary_max is not None:
            if self.salary_min > self.salary_max:
                raise ValueError("salary_min is greater than salary_max")
        return self