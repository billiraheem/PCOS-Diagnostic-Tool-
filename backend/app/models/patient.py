from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    clinician_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    clinician = relationship("User", back_populates="patients")
    diagnoses = relationship("Diagnosis", back_populates="patient")


class Diagnosis(Base):
    __tablename__ = "diagnoses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # Stage 1: Non-invasive data
    weight = Column(Float)
    height = Column(Float)
    bmi = Column(Float)
    cycle_regularity = Column(Integer)  # 2=Regular, 4=Irregular
    cycle_length = Column(Integer)
    weight_gain = Column(Boolean)
    hair_growth = Column(Boolean)
    skin_darkening = Column(Boolean)
    hair_loss = Column(Boolean)
    pimples = Column(Boolean)
    fast_food = Column(Boolean)
    regular_exercise = Column(Boolean)
    
    # Stage 2: Clinical data (nullable - filled later)
    fsh = Column(Float, nullable=True)
    lh = Column(Float, nullable=True)
    amh = Column(Float, nullable=True)
    tsh = Column(Float, nullable=True)
    follicle_l = Column(Integer, nullable=True)
    follicle_r = Column(Integer, nullable=True)
    avg_f_size_l = Column(Float, nullable=True)
    avg_f_size_r = Column(Float, nullable=True)
    endometrium = Column(Float, nullable=True)
    
    # Results
    stage1_probability = Column(Float, nullable=True)
    stage2_probability = Column(Float, nullable=True)
    risk_level = Column(String(20), nullable=True)  # LOW, MODERATE, HIGH
    is_confirmed = Column(Boolean, default=False)
    shap_values = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    patient = relationship("Patient", back_populates="diagnoses")