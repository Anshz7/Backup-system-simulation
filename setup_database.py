import mysql.connector
from mysql.connector import errorcode
from faker import Faker

config = {
    'user': 'root',
    'password': 'anshdb',
    'host': '127.0.0.1',
    'database': 'hospital_management',
    'raise_on_warnings': True
}

fake = Faker()

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        contact VARCHAR(50)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        date DATE,
        reason VARCHAR(255),
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
    )
    ''')

    for _ in range(10):
        name = fake.name()
        age = fake.random_int(min=20, max=80)
        contact = fake.phone_number()
        cursor.execute(
            "INSERT INTO patients (name, age, contact) VALUES (%s, %s, %s)", (name, age, contact))

    for _ in range(20):
        patient_id = fake.random_int(min=1, max=10)
        date = fake.date_this_year()
        reason = fake.sentence(nb_words=4)
        cursor.execute(
            "INSERT INTO appointments (patient_id, date, reason) VALUES (%s, %s, %s)", (patient_id, date, reason))

    conn.commit()
    print("Database setup complete!")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
