# PCOS Diagnostic Tool

An AI-powered web application for early detection of **Polycystic Ovarian Syndrome (PCOS)** using Explainable Machine Learning. The system provides clinicians with not just a prediction, but a visual explanation of _why_ a diagnosis was made using **SHAP (SHapley Additive exPlanations)**.

---

## Features

- **Two-Stage Diagnostic Flow**
  - **Stage 1 (Non-Invasive Screening):** Symptoms + vitals → initial risk assessment
  - **Stage 2 (Clinical Confirmation):** Lab results + ultrasound → confirmed diagnosis

- **Explainable AI (XAI)**
  - SHAP-based feature impact visualization showing which factors drove the prediction
  - Color-coded bar charts: red = increases risk, green = decreases risk

- **Role-Based Access Control (RBAC)**
  - **Clinician:** Manage patients, run screenings, view results, download reports
  - **Admin:** All clinician features + user management (roles, status)

- **PDF Report Generation**
  - Downloadable diagnostic reports with patient info, risk assessment, SHAP chart, and recommendations

- **Theme Switching**
  - 19 DaisyUI themes (Valentine default) with persistent selection

---

## Tech Stack

### Backend

| Technology                | Purpose                     |
| ------------------------- | --------------------------- |
| **FastAPI**               | REST API framework          |
| **SQLAlchemy**            | ORM for database models     |
| **PostgreSQL (Supabase)** | Cloud-hosted database       |
| **Pydantic**              | Request/response validation |
| **python-jose**           | JWT authentication          |
| **scikit-learn**          | ML model (Random Forest)    |
| **SHAP**                  | Model explainability        |
| **ReportLab**             | PDF report generation       |

### Frontend

| Technology                  | Purpose                                |
| --------------------------- | -------------------------------------- |
| **Next.js 14 (App Router)** | React framework with server components |
| **TypeScript**              | Type-safe JavaScript                   |
| **Tailwind CSS + DaisyUI**  | Styling + component library            |
| **Formik + Yup**            | Form handling + validation             |
| **Axios**                   | HTTP client with interceptors          |
| **Recharts**                | SHAP visualization charts              |
| **React Hot Toast**         | Toast notifications                    |
| **Lucide React**            | Icon library                           |

### Machine Learning

| Technology                      | Purpose                                           |
| ------------------------------- | ------------------------------------------------- |
| **Random Forest Classifier**    | PCOS prediction model                             |
| **SHAP TreeExplainer**          | Feature importance explanations                   |
| **scikit-learn StandardScaler** | Feature normalization                             |
| **Dynamic Imputation**          | Handles missing Stage 2 data using training means |

---

## Project Structure

```
Najeebah/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # App entry point, CORS, routers
│   │   ├── config.py          # Environment settings
│   │   ├── database.py        # SQLAlchemy engine & session
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── user.py        # User model (with role field)
│   │   │   └── patient.py     # Patient & Diagnosis models
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── user.py        # Auth request/response schemas
│   │   │   └── diagnosis.py   # Stage1/Stage2/Diagnosis schemas
│   │   ├── routers/           # API routes
│   │   │   ├── auth.py        # Login, register, JWT, admin guard
│   │   │   ├── admin.py       # User management (admin only)
│   │   │   └── diagnosis.py   # Patients, diagnoses, dashboard, PDF
│   │   ├── services/          # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── ml_service.py  # ML prediction + SHAP
│   │   │   └── pdf_service.py # PDF report generation
│   │   └── ml/                # ML model files
│   │       └── models/        # Trained model artifacts
│   ├── .env                   # Environment variables
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Next.js 14 frontend
│   ├── src/
│   │   ├── app/               # App Router pages
│   │   │   ├── layout.tsx     # Root layout (AuthProvider + Toaster)
│   │   │   ├── page.tsx       # Root redirect → /dashboard
│   │   │   ├── (auth)/        # Auth route group (centered layout)
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── register/page.tsx
│   │   │   └── (main)/        # Protected route group (sidebar layout)
│   │   │       ├── layout.tsx # Auth guard + sidebar + navbar
│   │   │       ├── dashboard/page.tsx
│   │   │       ├── patients/
│   │   │       │   ├── page.tsx         # Patient list
│   │   │       │   ├── new/page.tsx     # Create patient
│   │   │       │   └── [id]/page.tsx    # Patient detail
│   │   │       └── diagnosis/
│   │   │           ├── stage1/[patientId]/page.tsx
│   │   │           ├── stage2/[diagnosisId]/page.tsx
│   │   │           └── [id]/page.tsx    # Result view
│   │   ├── components/        # Reusable components
│   │   │   ├── ui/            # Input, Select, Button, Loading, etc.
│   │   │   ├── layout/        # Sidebar, Navbar
│   │   │   ├── auth/          # LoginForm, RegisterForm
│   │   │   ├── dashboard/     # StatsCards, PatientTable
│   │   │   ├── patients/      # PatientForm
│   │   │   └── diagnosis/     # Stage1Form, Stage2Form, ShapChart, ResultCard
│   │   ├── context/           # AuthContext (global auth state)
│   │   ├── hooks/             # Custom React hooks
│   │   ├── interfaces/        # TypeScript type definitions
│   │   ├── services/          # API service functions
│   │   ├── utils/             # Constants, helper functions
│   │   └── validations/       # Yup validation schemas
│   ├── .env.local             # Frontend environment variables
│   └── tailwind.config.ts     # DaisyUI theme configuration
│
├── ml/                         # Machine Learning
│   ├── notebooks/             # Jupyter notebooks (EDA, training)
│   ├── data/                  # Training datasets
│   ├── models/                # Trained model artifacts
│   │   ├── pcos_random_forest.pkl
│   │   ├── scaler.pkl
│   │   ├── training_means.json
│   │   ├── model_info.json
│   │   └── explainer_config.json
│   └── scripts/               # Training scripts
│
└── Dataset3/                   # Raw PCOS dataset
```

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL** (or a Supabase account)
- **Git**

---

### 1. Clone the Repository

```bash
git clone https://github.com/billiraheem/PCOS-Diagnostic-Tool-.git
cd PCOS-Diagnostic-Tool-
```

---

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database (replace with your PostgreSQL connection string)
DATABASE_URL=postgresql://user:password@host:port/database

# JWT Secret (generate your own: openssl rand -hex 32)
SECRET_KEY=your-secret-key-here

# App Settings
DEBUG=True
CORS_ORIGINS=["http://localhost:3000"]
```

#### Create Database Tables

```bash
python create_tables.py
```

#### Start the Backend Server

```bash
uvicorn app.main:app --reload
```

The API will be available at **http://localhost:8000**. Swagger docs at **http://localhost:8000/docs**.

---

### 3. Frontend Setup

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install
```

#### Configure Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Start the Frontend Dev Server

```bash
npm run dev
```

The app will be available at **http://localhost:3000**.

---

### 4. First-Time Usage

1. Visit `http://localhost:3000` → redirects to login
2. Click **"Create one"** to register a clinician account
3. Log in with your new credentials
4. Create a patient → Run Stage 1 screening → View results with SHAP explanation
5. Optionally run Stage 2 with lab/ultrasound data for confirmed diagnosis
6. Download PDF report from the result page

---

## API Endpoints

### Authentication

| Method | Endpoint               | Description         |
| ------ | ---------------------- | ------------------- |
| POST   | `/api/auth/register`   | Register new user   |
| POST   | `/api/auth/login/json` | Login (returns JWT) |
| GET    | `/api/auth/me`         | Get current user    |

### Diagnosis

| Method | Endpoint                               | Description                    |
| ------ | -------------------------------------- | ------------------------------ |
| POST   | `/api/diagnosis/patient`               | Create patient                 |
| GET    | `/api/diagnosis/patients`              | List all patients              |
| GET    | `/api/diagnosis/patient/{id}`          | Get patient detail + diagnoses |
| POST   | `/api/diagnosis/stage1/{patient_id}`   | Run Stage 1 screening          |
| PUT    | `/api/diagnosis/stage2/{diagnosis_id}` | Run Stage 2 confirmation       |
| GET    | `/api/diagnosis/diagnosis/{id}`        | Get diagnosis detail           |
| GET    | `/api/diagnosis/dashboard`             | Dashboard summary              |
| GET    | `/api/diagnosis/{id}/report`           | Download PDF report            |

### Admin (requires admin role)

| Method | Endpoint                       | Description        |
| ------ | ------------------------------ | ------------------ |
| GET    | `/api/admin/users`             | List all users     |
| PUT    | `/api/admin/users/{id}/role`   | Update user role   |
| PUT    | `/api/admin/users/{id}/status` | Toggle user status |

---

## ML Model Details

- **Algorithm:** Random Forest Classifier
- **Features:** 40+ features including symptoms, vitals, hormonal levels, and ultrasound data
- **Dynamic Imputation:** Missing Stage 2 features are filled with training dataset means
- **Explainability:** SHAP TreeExplainer generates per-prediction feature importance
- **Risk Levels:**
  - **HIGH (≥ 70%):** Presumptive PCOS positive
  - **MODERATE (30–70%):** Ambiguous — further testing recommended
  - **LOW (< 30%):** Low risk of PCOS

---

## License

This project is for academic purposes as part of a final year project.

---

## Author

**Balikis Abdulraheem**
