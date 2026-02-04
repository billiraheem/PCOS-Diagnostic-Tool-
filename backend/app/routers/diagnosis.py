from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.patient import Patient, Diagnosis
from app.schemas.diagnosis import (
    Stage1Input, Stage2Input, DiagnosisResponse,
    PatientCreate, PatientResponse
)
from app.routers.auth import get_current_user
from app.services.ml_service import ml_service
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.services.pdf_service import pdf_service
from app.services.ml_service import ml_service

router = APIRouter(prefix="/api/diagnosis", tags=["Diagnosis"])

@router.post("/patient", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_patient = Patient(
        name=patient_data.name,
        date_of_birth=patient_data.date_of_birth,
        phone=patient_data.phone,
        email=patient_data.email,
        address=patient_data.address,
        clinician_id=current_user.id
    )
    
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    
    return new_patient


@router.get("/patients", response_model=List[PatientResponse])
def get_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patients = db.query(Patient).filter(
        Patient.clinician_id == current_user.id
    ).all()
    return patients


@router.post("/stage1/{patient_id}", response_model=DiagnosisResponse)
def stage1_screening(
    patient_id: int,
    input_data: Stage1Input,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify patient belongs to this clinician
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.clinician_id == current_user.id
    ).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Determine age to use: input override or patient's current age
    actual_age = input_data.age if input_data.age else patient.age
    
    if not actual_age:
        raise HTTPException(status_code=400, detail="Unable to determine patient age")
    
    # Prepare input for ML model
    ml_input = input_data.model_dump()
    ml_input['age'] = actual_age  # Ensure correct age is used
    
    # Get prediction with SHAP explanation
    result = ml_service.predict_stage1(ml_input)
    
    # Calculate BMI
    bmi = input_data.weight / ((input_data.height / 100) ** 2)
    
    # Create diagnosis record
    diagnosis = Diagnosis(
        patient_id=patient_id,
         age_at_diagnosis=actual_age,  # Store the age used
        weight=input_data.weight,
        height=input_data.height,
        bmi=bmi,
        cycle_regularity=input_data.cycle_regularity,
        cycle_length=input_data.cycle_length,
        weight_gain=bool(input_data.weight_gain),
        hair_growth=bool(input_data.hair_growth),
        skin_darkening=bool(input_data.skin_darkening),
        hair_loss=bool(input_data.hair_loss),
        pimples=bool(input_data.pimples),
        fast_food=bool(input_data.fast_food),
        regular_exercise=bool(input_data.regular_exercise),
        stage1_probability=result['probability'],
        risk_level=result['risk_level'],
        is_confirmed=False,
        shap_values=result['shap_chart_data']
    )
    
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    
    return DiagnosisResponse(
        id=diagnosis.id,
        patient_id=patient_id,
        probability=result['probability'],
        risk_level=result['risk_level'],
        is_confirmed=False,
        shap_chart_data=result['shap_chart_data'],
        recommendation=result['recommendation'],
        created_at=diagnosis.created_at,
        updated_at=diagnosis.updated_at
    )


@router.put("/stage2/{diagnosis_id}", response_model=DiagnosisResponse)
def stage2_confirmation(
    diagnosis_id: int,
    input_data: Stage2Input,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get existing diagnosis
    diagnosis = db.query(Diagnosis).join(Patient).filter(
        Diagnosis.id == diagnosis_id,
        Patient.clinician_id == current_user.id
    ).first()
    
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    
    # Build complete input (Stage 1 + Stage 2 data)
    ml_input = {
        'age': diagnosis.patient.age,
        'weight': diagnosis.weight,
        'height': diagnosis.height,
        'cycle_regularity': diagnosis.cycle_regularity,
        'cycle_length': diagnosis.cycle_length,
        'weight_gain': int(diagnosis.weight_gain),
        'hair_growth': int(diagnosis.hair_growth),
        'skin_darkening': int(diagnosis.skin_darkening),
        'hair_loss': int(diagnosis.hair_loss),
        'pimples': int(diagnosis.pimples),
        'fast_food': int(diagnosis.fast_food),
        'regular_exercise': int(diagnosis.regular_exercise),
        # Add Stage 2 clinical data
        **input_data.model_dump()
    }
    
    # Get new prediction with full data
    result = ml_service.predict_stage2(ml_input)
    
    # Update diagnosis record
    diagnosis.fsh = input_data.fsh
    diagnosis.lh = input_data.lh
    diagnosis.amh = input_data.amh
    diagnosis.tsh = input_data.tsh
    diagnosis.follicle_l = input_data.follicle_l
    diagnosis.follicle_r = input_data.follicle_r
    diagnosis.avg_f_size_l = input_data.avg_f_size_l
    diagnosis.avg_f_size_r = input_data.avg_f_size_r
    diagnosis.endometrium = input_data.endometrium
    diagnosis.stage2_probability = result['probability']
    diagnosis.risk_level = result['risk_level']
    diagnosis.is_confirmed = True
    diagnosis.shap_values = result['shap_chart_data']
    
    db.commit()
    db.refresh(diagnosis)
    
    return DiagnosisResponse(
        id=diagnosis.id,
        patient_id=diagnosis.patient_id,
        probability=result['probability'],
        risk_level=result['risk_level'],
        is_confirmed=True,
        shap_chart_data=result['shap_chart_data'],
        recommendation=result['recommendation'],
        created_at=diagnosis.created_at,
        updated_at=diagnosis.updated_at
    )

# Get a single patient with all their diagnoses.
@router.get("/patient/{patient_id}")
def get_patient_detail(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.clinician_id == current_user.id
    ).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Get all diagnoses for this patient
    diagnoses = db.query(Diagnosis).filter(
        Diagnosis.patient_id == patient_id
    ).order_by(Diagnosis.created_at.desc()).all()
    
    # Format diagnoses
    diagnosis_list = []
    for d in diagnoses:
        diagnosis_list.append({
            "id": d.id,
            "probability": d.stage2_probability if d.is_confirmed else d.stage1_probability,
            "risk_level": d.risk_level,
            "is_confirmed": d.is_confirmed,
            "shap_chart_data": d.shap_values,
            "created_at": d.created_at,
            "updated_at": d.updated_at,
            # Include input data
            "weight": d.weight,
            "height": d.height,
            "bmi": d.bmi,
            "cycle_regularity": d.cycle_regularity,
            "cycle_length": d.cycle_length,
            # Stage 2 data (if available)
            "fsh": d.fsh,
            "lh": d.lh,
            "amh": d.amh,
            "follicle_l": d.follicle_l,
            "follicle_r": d.follicle_r,
        })
    
    return {
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "created_at": patient.created_at,
        "clinician_id": patient.clinician_id,
        "diagnoses": diagnosis_list,
        "latest_diagnosis": diagnosis_list[0] if diagnosis_list else None
    }

# Get a single diagnosis with all details.
@router.get("/diagnosis/{diagnosis_id}")
def get_diagnosis_detail(
    diagnosis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    diagnosis = db.query(Diagnosis).join(Patient).filter(
        Diagnosis.id == diagnosis_id,
        Patient.clinician_id == current_user.id
    ).first()
    
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    
    return {
        "id": diagnosis.id,
        "patient_id": diagnosis.patient_id,
        "patient_name": diagnosis.patient.name,
        "patient_age": diagnosis.patient.age,
        "probability": diagnosis.stage2_probability if diagnosis.is_confirmed else diagnosis.stage1_probability,
        "risk_level": diagnosis.risk_level,
        "is_confirmed": diagnosis.is_confirmed,
        "shap_chart_data": diagnosis.shap_values,
        # All input data
        "weight": diagnosis.weight,
        "height": diagnosis.height,
        "bmi": diagnosis.bmi,
        "cycle_regularity": diagnosis.cycle_regularity,
        "cycle_length": diagnosis.cycle_length,
        "weight_gain": diagnosis.weight_gain,
        "hair_growth": diagnosis.hair_growth,
        "skin_darkening": diagnosis.skin_darkening,
        "hair_loss": diagnosis.hair_loss,
        "pimples": diagnosis.pimples,
        "fast_food": diagnosis.fast_food,
        "regular_exercise": diagnosis.regular_exercise,
        # Stage 2 clinical data
        "fsh": diagnosis.fsh,
        "lh": diagnosis.lh,
        "amh": diagnosis.amh,
        "tsh": diagnosis.tsh,
        "follicle_l": diagnosis.follicle_l,
        "follicle_r": diagnosis.follicle_r,
        "avg_f_size_l": diagnosis.avg_f_size_l,
        "avg_f_size_r": diagnosis.avg_f_size_r,
        "endometrium": diagnosis.endometrium,
        # Timestamps
        "created_at": diagnosis.created_at,
        "updated_at": diagnosis.updated_at,
    }

# Dashboard summary - optimized endpoint for patient list
@router.get("/dashboard")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patients = db.query(Patient).filter(
        Patient.clinician_id == current_user.id
    ).all()
    
    dashboard_data = []
    
    for patient in patients:
        # Get the latest diagnosis for this patient
        latest_diagnosis = db.query(Diagnosis).filter(
            Diagnosis.patient_id == patient.id
        ).order_by(Diagnosis.created_at.desc()).first()
        
        patient_data = {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "created_at": patient.created_at,
            "has_diagnosis": latest_diagnosis is not None,
        }
        
        if latest_diagnosis:
            patient_data.update({
                "latest_diagnosis_id": latest_diagnosis.id,
                "probability": latest_diagnosis.stage2_probability if latest_diagnosis.is_confirmed else latest_diagnosis.stage1_probability,
                "risk_level": latest_diagnosis.risk_level,
                "is_confirmed": latest_diagnosis.is_confirmed,
                "diagnosis_date": latest_diagnosis.updated_at,
            })
        else:
            patient_data.update({
                "latest_diagnosis_id": None,
                "probability": None,
                "risk_level": None,
                "is_confirmed": False,
                "diagnosis_date": None,
            })
        
        dashboard_data.append(patient_data)
    
    return {
        "total_patients": len(patients),
        "patients": dashboard_data
    }


# PDF Report Download
@router.get("/{diagnosis_id}/report")
def download_report(
    diagnosis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get the diagnosis with patient info
    diagnosis = db.query(Diagnosis).join(Patient).filter(
        Diagnosis.id == diagnosis_id,
        Patient.clinician_id == current_user.id
    ).first()
    
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    
    probability = diagnosis.stage2_probability if diagnosis.is_confirmed else diagnosis.stage1_probability
    risk_level = diagnosis.risk_level   

    # Generate recommendation on-the-fly
    recommendation = ml_service._get_detailed_recommendation(risk_level, diagnosis.is_confirmed)

    # Prepare data for PDF generation
    diagnosis_data = {
        "patient_name": diagnosis.patient.name,
        "patient_age": diagnosis.patient.age,
        "probability": probability,
        "risk_level": risk_level,
        "is_confirmed": diagnosis.is_confirmed,
        "shap_chart_data": diagnosis.shap_values or [],
        "recommendation": recommendation,
        "created_at": diagnosis.created_at,
    }
    
    # Generate PDF
    pdf_bytes = pdf_service.generate_report(diagnosis_data)
    
    # Create filename
    filename = f"PCOS_Report_{diagnosis.patient.name.replace(' ', '_')}_{diagnosis.created_at.strftime('%Y%m%d')}.pdf"
    
    # Return as downloadable file
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )