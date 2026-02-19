from app.database import engine, Base
from app.models.user import User
from app.models.patient import Patient, Diagnosis

print("Resetting database tables...")
# Droping all tables to ensure schema updates are applied
Base.metadata.drop_all(bind=engine)
print("  - Dropped existing tables")

# Creating all tables defined in our models
Base.metadata.create_all(bind=engine)

print("All tables created successfully!")
print("\nTables created:")
print("  - users")
print("  - patients")
print("  - diagnoses")