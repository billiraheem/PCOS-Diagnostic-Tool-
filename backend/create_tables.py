from app.database import engine, Base
from app.models.user import User
from app.models.patient import Patient, Diagnosis

print("Creating database tables...")

# This creates all tables defined in our models
Base.metadata.create_all(bind=engine)

print("All tables created successfully!")
print("\nTables created:")
print("  - users")
print("  - patients")
print("  - diagnoses")