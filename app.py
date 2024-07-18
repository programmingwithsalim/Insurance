from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import Database

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'passwd'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


db = Database(app)


# Home route
@app.route('/')
def index():
    """/"""
    if 'userid' not in session:
        return redirect(url_for('login'))
    
    return render_template('login.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """/"""
    if "userid" in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        # Get form data
        print(request.form)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        occupation = request.form['occupation']
        kin_name = request.form['kin_name']
        kin_relation = request.form['kin_relation']
        kin_phone = request.form['kin_phone']

        user_exists = db.check_user_exists(username)

        if user_exists:
            flash('This user already exists!')
            return redirect(url_for('login'))
        
        # Save user to database
        db.create_user(first_name, last_name, dob, email, username, password, occupation, kin_name, kin_relation, kin_phone)
        flash("User created successfully.")
        return redirect(url_for('login'))
    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """/"""
    if "userid" in session:
        return redirect(url_for("dashboard"))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user(username, password)
        print(user)

        if user:
            session['userid'] = user['id']
            flash("Login successful")
            return redirect(url_for('dashboard'))
        
        flash('Invalid credentials')

    return render_template('login.html')

#Logout route
@app.route("/logout")
def logout():
    """/"""
    session.pop("userid", None)
    flash("Logout Successful")
    return redirect(url_for("login"))
    

# User dashboard route
@app.route('/dashboard')
def dashboard():
    """/"""
    if "userid" not in session:
        return redirect(url_for("login"))

    return render_template('dashboard.html')

# Profile
@app.route('/profile')
def profile():
    """/"""
    if "userid" not in session:
        return redirect(url_for("login"))

    user_id = session["userid"]
    user = db.get_user_by_id(user_id)
    
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("dashboard"))
    
    return render_template("profile.html", user=user)



# Claim Insurance
@app.route('/claim_insurance', methods=['GET', 'POST'])
def claim_insurance():
    """/"""
    if "userid" not in session:
        return redirect(url_for("login"))

    user_id = session["userid"]
    life_insurances = db.get_life_insurances_by_user(user_id)
    motor_insurances = db.get_motor_insurances_by_user(user_id)
    property_insurances = db.get_property_insurances_by_user(user_id)
    disability_insurances = db.get_disability_insurances_by_user(user_id)
    health_insurances = db.get_health_insurances_by_user(user_id)

    return render_template('claim_insurance.html', 
                            life_insurances=life_insurances,
                            motor_insurances=motor_insurances,
                            property_insurances=property_insurances,
                            disability_insurances=disability_insurances,
                            health_insurances=health_insurances)

# Claim single insurance
@app.route('/claim_life_insurance/<int:id>')
def claim_life_insurance(id):
    """/"""
    if "userid" not in session:
        return redirect(url_for("login"))

    user_id = session["userid"]
    db.claim_life_insurance(id, user_id)
    flash("Life insurance claimed successfully, you'll receive an sms confirmation shortly.", "success")
    return redirect(url_for("claim_insurance"))

# Life insurance route
@app.route('/life_insurance', methods=['GET', 'POST'])
def life_insurance():
    """/"""
    if "userid" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        insured_person = request.form.get('insured_person')
        amount = request.form.get('amount')
        period = request.form.get('period')
        user_id = session["userid"]

        if not insured_person or not amount or not period:
            flash('All fields are required!', 'danger')
        elif int(amount) < 50 or int(amount) > 200:
            flash("Amount can only be between 50 and 200")
        else:
            db.create_life_insurance(insured_person, amount, period, user_id)
            flash('Life Insurance created successfully!', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('life_insurance.html')

@app.route('/motor_insurance', methods=['GET', 'POST'])
def motor_insurance():
    """/"""
    if "userid" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        insured_person = request.form.get('insured_person')
        amount = request.form.get('amount')
        period = request.form.get('period')
        policy_type = request.form.get('policy_type')
        user_id = session["userid"]

        if not insured_person or not amount or not period or not policy_type:
            flash('All fields are required!', 'danger')
        elif int(amount) < 50 or int(amount) > 200:
            flash("Amount can only be between 50 and 200")
        else:
            db.create_motor_insurance(insured_person, amount, period, policy_type, user_id)
            flash('Motor Insurance created successfully!', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('motor_insurance.html')

@app.route('/property_insurance', methods=['GET', 'POST'])
def property_insurance():
    """/"""
    if "userid" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        property_item = request.form.get('property_item')
        amount = request.form.get('amount')
        period = request.form.get('period')
        user_id = session["userid"]

        if not property_item or not amount or not period:
            flash('All fields are required!', 'danger')
        elif int(amount) < 50 or int(amount) > 200:
            flash("Amount can only be between 50 and 200")
        else:
            db.create_property_insurance(property_item, amount, period, user_id)
            flash('Property Insurance created successfully!', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('property_insurance.html')

@app.route('/disability_insurance', methods=['GET', 'POST'])
def disability_insurance():
    """/"""
    if "userid" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        insured_person = request.form.get('insured_person')
        amount = request.form.get('amount')
        period = request.form.get('period')
        user_id = session["userid"]

        if not insured_person or not amount or not period:
            flash('All fields are required!', 'danger')
        elif int(amount) < 50 or int(amount) > 200:
            flash("Amount can only be between 50 and 200")
        else:
            db.create_disability_insurance(insured_person, amount, period, user_id)
            flash('Disability Insurance created successfully!', 'success')
            return redirect(url_for('dashboard'))

    return render_template('disability_insurance.html')

@app.route('/health_insurance', methods=['GET', 'POST'])
def health_insurance():
    """/"""
    if "userid" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        insured_person = request.form.get('insured_person')
        amount = request.form.get('amount')
        period = request.form.get('period')
        user_id = session["userid"]

        if not insured_person or not amount or not period:
            flash('All fields are required!', 'danger')
        elif int(amount) < 50 or int(amount) > 200:
            flash("Amount can only be between 50 and 200")
        else:
            db.create_health_insurance(insured_person, amount, period, user_id)
            flash('Health Insurance created successfully!', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('health_insurance.html')

if __name__ == '__main__':
    app.run(debug=True)
