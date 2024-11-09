import pandas as pd
import os
from datetime import datetime
from sqlalchemy import create_engine

DB_USERNAME = 'root'
DB_PASSWORD = 'anshdb'
DB_NAME = 'hospital_management'
DB_HOST = '127.0.0.1'

BACKUP_DIR = "hospital_backups"

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")


def full_backup():
    with engine.connect() as conn:
        patients_df = pd.read_sql("SELECT * FROM patients", conn)
        patients_backup_path = os.path.join(
            BACKUP_DIR, f"patients_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        patients_df.to_csv(patients_backup_path, index=False)
        print(f"Full backup of patients table saved to {patients_backup_path}")

        appointments_df = pd.read_sql("SELECT * FROM appointments", conn)
        appointments_backup_path = os.path.join(
            BACKUP_DIR, f"appointments_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        appointments_df.to_csv(appointments_backup_path, index=False)
        print(f"Full backup of appointments table saved to {appointments_backup_path}")


def incremental_backup(last_backup_time):
    with engine.connect() as conn:
        patients_query = f"SELECT * FROM patients WHERE updated_at > '{last_backup_time}'"
        patients_df = pd.read_sql(patients_query, conn)
        patients_backup_path = os.path.join(
            BACKUP_DIR, f"patients_incremental_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        patients_df.to_csv(patients_backup_path, index=False)
        print(f"Incremental backup of patients table saved to {patients_backup_path}")

        appointments_query = f"SELECT * FROM appointments WHERE updated_at > '{last_backup_time}'"
        appointments_df = pd.read_sql(appointments_query, conn)
        appointments_backup_path = os.path.join(
            BACKUP_DIR, f"appointments_incremental_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        appointments_df.to_csv(appointments_backup_path, index=False)
        print(f"Incremental backup of appointments table saved to {appointments_backup_path}")


full_backup()

last_backup_time = '2024-11-01 00:00:00'
incremental_backup(last_backup_time)
