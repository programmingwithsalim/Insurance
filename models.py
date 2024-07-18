import mysql.connector

class Database:
    def __init__(self, app):
        self.conn = mysql.connector.connect(
            host=app.config['MYSQL_DATABASE_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_DATABASE_PASSWORD'],
            database=app.config['MYSQL_DATABASE_DB']
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def create_user(self, first_name, last_name, dob, email, username, password, occupation, next_of_kin_name, next_of_kin_relation, next_of_kin_phone):
        """/"""
        sql = "INSERT INTO users (first_name, last_name, dob, email, username, password, occupation, next_of_kin_name, next_of_kin_relation, next_of_kin_phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (first_name, last_name, dob, email, username, password, occupation, next_of_kin_name, next_of_kin_relation, next_of_kin_phone)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def check_user_exists(self, username):
        """ /"""
        sql = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(sql, (username))
        user = self.cursor.fetchone()
        return user

    def get_user_by_id(self, user_id):
        """/"""
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = self.cursor.fetchone()
        return user

    def get_user(self, username, password):
        """/"""
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(sql, (username, password))
        return self.cursor.fetchone()

    def create_life_insurance(self, insured_person, amount, period, user_id):
        """/"""
        sql = "INSERT INTO life_insurance (insured_person, amount, period, user_id) VALUES (%s, %s, %s, %s)"
        val = (insured_person, amount, period, user_id)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def create_motor_insurance(self, insured_person, amount, period, policy_type, user_id):
        """/"""
        sql = "INSERT INTO motor_insurance (insured_person, amount, period, policy_type, user_id) VALUES (%s, %s, %s, %s, %s)"
        val = (insured_person, amount, period, policy_type, user_id)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def create_property_insurance(self, property_item, amount, period, user_id):
        """/"""
        sql = "INSERT INTO property_insurance (property_item, amount, period, user_id) VALUES (%s, %s, %s, %s)"
        val = (property_item, amount, period, user_id)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def create_disability_insurance(self, insured_person, amount, period, user_id):
        """/"""
        sql = "INSERT INTO disability_insurance (insured_person, amount, period, user_id) VALUES (%s, %s, %s, %s)"
        val = (insured_person, amount, period, user_id)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def create_health_insurance(self, insured_person, amount, period, user_id):
        """/"""
        sql = "INSERT INTO health_insurance (insured_person, amount, period, user_id) VALUES (%s, %s, %s, %s)"
        val = (insured_person, amount, period, user_id)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def get_life_insurances_by_user(self, user_id):
        """/"""
        self.cursor.execute("SELECT * FROM life_insurance WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    def get_motor_insurances_by_user(self, user_id):
        """/"""
        self.cursor.execute("SELECT * FROM motor_insurance WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    def get_property_insurances_by_user(self, user_id):
        """/"""
        self.cursor.execute("SELECT * FROM property_insurance WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    def get_disability_insurances_by_user(self, user_id):
        """/"""
        self.cursor.execute("SELECT * FROM disability_insurance WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    def get_health_insurances_by_user(self, user_id):
        """/"""
        self.cursor.execute("SELECT * FROM health_insurance WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    def claim_life_insurance(self, insurance_id, user_id):
        """/"""
        self.cursor.execute("DELETE FROM life_insurance WHERE id = %s AND user_id = %s", (insurance_id, user_id))
        self.conn.commit()
