from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PatientCreate(BaseModel):
    name: str
    age: int


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Stage1Input(BaseModel):
    # Stage 1: Non-invasive screening input.
    # Required fields
    age: int = Field(..., ge=15, le=50, description="Age in years")
    weight: float = Field(..., ge=30, le=200, description="Weight in kg")
    height: float = Field(..., ge=100, le=200, description="Height in cm")
    cycle_regularity: int = Field(..., description="2=Regular, 4=Irregular")
    cycle_length: int = Field(..., ge=0, le=60, description="Cycle length in days")
    
    # Binary symptoms (0 or 1)
    weight_gain: int = Field(..., ge=0, le=1)
    hair_growth: int = Field(..., ge=0, le=1)
    skin_darkening: int = Field(..., ge=0, le=1)
    hair_loss: int = Field(..., ge=0, le=1)
    pimples: int = Field(..., ge=0, le=1)
    fast_food: int = Field(..., ge=0, le=1)
    regular_exercise: int = Field(..., ge=0, le=1)


class Stage2Input(BaseModel):
    # Stage 2: Clinical data input (updates existing diagnosis).
    # Hormonal
    fsh: float = Field(..., ge=0, description="FSH level mIU/mL")
    lh: float = Field(..., ge=0, description="LH level mIU/mL")
    amh: float = Field(..., ge=0, description="AMH level ng/mL")
    tsh: Optional[float] = Field(None, ge=0, description="TSH level mIU/L")
    
    # Ultrasound
    follicle_l: int = Field(..., ge=0, le=50, description="Follicle count left ovary")
    follicle_r: int = Field(..., ge=0, le=50, description="Follicle count right ovary")
    avg_f_size_l: float = Field(..., ge=0, description="Avg follicle size left mm")
    avg_f_size_r: float = Field(..., ge=0, description="Avg follicle size right mm")
    endometrium: Optional[float] = Field(None, ge=0, description="Endometrium thickness mm")


class ShapChartData(BaseModel):
    feature: str
    impact: float
    direction: str  # 'increases' or 'decreases'
    value: Optional[float]
    color: str


class DiagnosisResponse(BaseModel):
    id: int
    patient_id: int
    
    # Risk assessment
    probability: float
    risk_level: str  # LOW, MODERATE, HIGH
    is_confirmed: bool
    
    # SHAP explanation
    shap_chart_data: List[ShapChartData]
    
    # Recommendation based on risk
    recommendation: str
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True