
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class PropertyIn(BaseModel):
    id: int
    address: str
    city: str
    price: int = Field(ge=0)
    bedrooms: int = Field(ge=0)
    description: Optional[str] = None

class Property(PropertyIn):
    pass

class LeadIn(BaseModel):
    id: int
    name: str
    email: EmailStr
    budget_min: int = Field(ge=0)
    budget_max: int = Field(ge=0)
    preferred_city: str

class Lead(LeadIn):
    pass

class MatchResult(BaseModel):
    lead_id: int
    matched_property_ids: List[int]

class ProgressionUpdate(BaseModel):
    status: str
