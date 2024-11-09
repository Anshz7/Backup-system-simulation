import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import os

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASSWORD = 'anshdb'
DB_NAME = 'hospital_management'
BACKUP_DIR = 'C:/Users/Ansh Shrivastava/Desktop/ism/hospital_backups'


def create_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def restore_table_from_csv(csv_file, table_name, is_patient_table=False):
    df = pd.read_csv(csv_file)
    conn = create_db_connection()

    try:
        cursor = conn.cursor()

        if not is_patient_table:
            cursor.execute("SET foreign_key_checks = 0;")

        engine = create_engine(
            f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
        if is_patient_table:
            df.to_sql(table_name, engine, if_exists='append', index=False)
        else:
            df.to_sql(table_name, engine, if_exists='replace', index=False)

        if not is_patient_table:
            cursor.execute("SET foreign_key_checks = 1;")

        conn.commit()
        cursor.close()
        conn.close()

        print(f"Restored {table_name} from {csv_file}")

    except Exception as e:
        print(f"Error restoring {table_name}: {e}")
        conn.rollback()
        cursor.close()
        conn.close()


def full_restore():
    backup_files = os.listdir(BACKUP_DIR)

    for backup_file in backup_files:
        if 'patients' in backup_file:
            restore_table_from_csv(os.path.join(
                BACKUP_DIR, backup_file), 'patients', is_patient_table=True)

    for backup_file in backup_files:
        if 'appointments' in backup_file:
            restore_table_from_csv(os.path.join(
                BACKUP_DIR, backup_file), 'appointments')


if __name__ == "__main__":
    print("Starting full restore...")
    full_restore()
    print("Full restore completed.")
