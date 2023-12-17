from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text
from models.models import *
import hashlib

app = Flask(__name__)
app.secret_key="somesupersecretkey"
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:course123@localhost/mis data'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get the form values
        username = request.form['username'].lower()
        password_entered = request.form['password']
        #decrypt the password
        hash = password_entered + app.secret_key
        hash = hashlib.sha256(hash.encode())
        password = hash.hexdigest()
        #check if the user exists in the database
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{username}' and password = '{password}'"))
            account = result.fetchone()
            con.commit()

        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            msg = "Logged in successfully"
            return redirect(url_for('home', msg=msg))
        else:
            msg = "Incorrect username/password"
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get the form values
        username = request.form['username'].lower()
        cusername = request.form['cusername'].lower()
        password = request.form['password']
        cpassword = request.form['cpassword']
        if username!=cusername:
            msg = "Usernames do not match"
            return render_template('register.html', msg=msg)
        if password!=cpassword:
            msg = "Passwords do not match"
            return render_template('register.html', msg=msg)
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{username}'"))
            account = result.fetchone()
            con.commit()
        if account:
            msg = "Account already exists"
            return render_template('register.html', msg=msg)
        
        if not username or not password or not cusername or not cpassword:
                msg = "Please fill out the form"
                return render_template('register.html', msg=msg)
        else:
            #encrypt the password
            hash = password + app.secret_key
            hash = hashlib.sha256(hash.encode())
            password = hash.hexdigest()
            #insert the user into the database
            with engine.connect() as con:
                con.execute(text(f"Insert into user (username, password) values ('{username}', '{password}')"))
                con.commit()
            msg = "Account created successfully"
            return redirect(url_for('login', msg=msg))
    return render_template('register.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/profile')
def customer_information():
    return render_template('profile.html')

#The page for the customer infomation
@app.route('/customer_information', methods=['POST'])
def customer_information():
    return render_template('customerinformation.html')
     #get the data from the form
    if request.method=='POST' and 'last_name' in request.form:
        customer_last_name = request.form['last_name']
        customer_first_name = request.form['first_name']
        customer_middle_name = request.form['middle_name']
        customer_date_of_birth = request.form['dob']
        customer_Estimated_delivery_date = request.form['customer_Estimated_delivery_date']
        customer_address = request.form['Address']
        Residency_of_Customer = request.form['Residency']
        customer_state = request.form['city']
        customer_Zip = request.form['code']
        customer_telephone_number = request.form['tel']
        customer_type_of_insurance = request.form['type_of_insurance']
        customer_race = request.form['customer_race']
        hispanic = request.form['hispanic']
        customer_country_of_birth = request.form['country_of_birth']
        customer_primary_language = request.form['primary_language']
        check_if_interpreter_is_needed = request.form['check_if_interpreter_is_needed']

        #check if the unique_id is already in the database
        with engine.connect() as con:
         result = con.execute(text(f"SELECT * FROM customer_information WHERE WHERE unique_id = '{client_id}'"))
        customer = result.customer_information.fetchone()
        if client:
                msg = 'The client already exists.'
                return redirect(url_for('home', msg = msg))
        #check if all the required fields are filled

 #The page for the guarantor infomation       
@app.route('/guarantor_information')
def guarantor_information():
 return render_template('customerinformation.html')

 #get the data from the form
if request.method=='POST' and 'address' in request.form:
        guarantor_address = request.form['Address']
        guarantor_residency = request.form['Residency']
        guarantor_state = request.form['city']
        guarantor_telephone_number = request.form['tel']
        guarantor_type_of_insurance = request.form['type_of_insurance']
        guarantor_race = request.form['guarantor_race']
        guarantor_hispanic = request.form['guarantor_hispanic']
        guarantor_country_of_birth = request.form['country_of_birth']
        guarantor_primary_language = request.form['primary_language']

        #check if the unique_id is already in the database
        with engine.connect() as con:
         result = con.execute(text(f"SELECT * FROM guarantor_information WHERE guarantor_unique_id = '{client_id}'"))
        guarantor = result.guarantor_information.fetchone()
        if client:
                msg = 'The client already exists.'
                return redirect(url_for('home', msg = msg))
        #check if all the required fields are filled

#The page for the employee records
@app.route('/employee_records')
def employee_records():
    return render_template('employeerecords.html')
 #get the data from the form
    if request.method=='POST' and 'last_name' in request.form:
        employee_last_name = request.form['last_name']
        employee_first_name = request.form['first_name']
        employee_middle_name = request.form['middle_name']
        employee_date_of_birth = request.form['dob']
        employee_Estimated_delivery_date = request.form['customer_Estimated_delivery_date']
        employee_address = request.form['Address']
        Residency_of_employee = request.form['Residency']
        employee_state = request.form['city']
        employee_Zip = request.form['code']
        employee_telephone_number = request.form['tel']
        employee_type_of_insurance = request.form['type_of_insurance']
        employee_race = request.form['employee_race']
        employee_hispanic = request.form['employee_hispanic']
        employee_country_of_birth = request.form['country_of_birth']
        employee_primary_language = request.form['primary_language']
        employee_check_if_interpreter_is_needed = request.form['employee_check_if_interpreter_is_needed']

        #check if the unique_id is already in the database
        with engine.connect() as con:
         result = con.execute(text(f"SELECT * FROM employee_records WHERE unique_id = '{client_id}'"))
        employee = result.employee_records.fetchone()
        if client:
                msg = 'The client already exists.'
                return redirect(url_for('home', msg = msg))
        #check if all the required fields are filled

#The page for the financial data
@app.route('/financial_data')
def financial_data():
    return render_template('financialdata.html')
#get the data from the form
    if request.method=='POST' and 'Balance_For_January_B/D' in request.form:
        Balance_For_January_B/D = request.form['Balance_For_January_B/D']
        january_B/D = request.form['january_B/D']
        Balance_For_Feburary_B/D = request.form['Balance_For_feburary_B/D']
        Feburary_B/D = request.form['Feburary_B/D']
        Balance_For_March_B/D = request.form['Balance_For_March_B/D']
        march_B/D = request.form['march_B/D']
        Balance_For_April_B/D = request.form['Balance_For_April_B/D']
        april_B/D = request.form['april_B/D']
        Balance_For_may_B/D = request.form['Balance_For_may_B/D']
        may_B/D = request.form['may_B/D']
        Balance_For_June_B/D = request.form['Balance_For_June_B/D']
        june_B/D = request.form['june_B/D']
        Balance_For_July_B/D = request.form['Balance_For_July_B/D']
        july_B/D = request.form['july_B/D']
        Balance_For_August_B/D = request.form['Balance_For_August_B/D']
        august_B/D = request.form['august_B/D']
        Balance_For_september_B/D = request.form['Balance_For_September_B/D']
        september_B/D = request.form['september_B/D']
        Balance_For_october_B/D = request.form['Balance_For_october_B/D']
        october_B/D = request.form['october_B/D']
        Balance_For_November_B/D = request.form['Balance_For_November_B/D']
        november_B/D = request.form['november_B/D']
        Balance_For_December_B/D = request.form['Balance_For_December_B/D']
        december_B/D = request.form['december_B/D']

        #check if the unique_id is already in the database
        with engine.connect() as con:
         result = con.execute(text(f"SELECT * FROM Financial_Data WHERE unique_id = '{client_id}'"))
        financial = result.financial_data.fetchone()
        if client:
                msg = 'The client already exists.'
                return redirect(url_for('home', msg = msg))
        #check if all the required fields are filled
        
#The page for the inventory levels
@app.route('/inventory_levels')
def inventory_levels():
    return render_template('inventorylevels.html')

#get the data from the form
    if request.method=='POST' and 'Balance_For_January_inventory' in request.form:
        Balance_For_January_inventory = request.form['Balance_For_January_inventory']
        january_inventory = request.form['january_inventory']
        Balance_For_Feburary_inventory = request.form['Balance_For_feburary_inventory']
        Feburary_inventory = request.form['Feburary_inventory']
        Balance_For_March_inventory = request.form['Balance_For_March_inventory']
        march_inventory = request.form['march_inventory']
        Balance_For_April_inventory = request.form['Balance_For_April_inventory']
        april_inventory = request.form['april_inventory']
        Balance_For_may_inventory = request.form['Balance_For_may_inventory']
        may_inventory = request.form['may_inventory']
        Balance_For_June_inventory = request.form['Balance_For_June_inventory']
        june_inventory = request.form['june_inventory']
        Balance_For_July_inventory = request.form['Balance_For_July_inventory']
        july_inventory = request.form['july_inventory']
        Balance_For_August_inventory = request.form['Balance_For_August_inventory']
        august_inventory = request.form['august_inventory']
        Balance_For_september_inventory = request.form['Balance_For_September_inventory']
        september_inventory = request.form['september_inventory']
        Balance_For_october_inventory = request.form['Balance_For_october_inventory']
        october_inventory = request.form['october_inventory']
        Balance_For_November_inventory = request.form['Balance_For_November_inventory']
        november_inventory = request.form['november_inventory']
        Balance_For_December_inventory = request.form['Balance_For_December_inventory']
        december_inventory = request.form['december_inventory']

        #check if the unique_id is already in the database
        with engine.connect() as con:
         result = con.execute(text(f"SELECT * FROM inventory_levels WHERE Balance_For_January_inventory = '{Balance_For_January_inventory}'"))
        inventory = result.inventory_levels.fetchone()
        if client:
                msg = 'The client already exists.'
                return redirect(url_for('home', msg = msg))
        #check if all the required fields are filled
     
#The page for the sales figure
@app.route('/sales_figure')
def sales_figure():
    return render_template('salesfigure.html')

#get the data from the form
    if request.method=='POST' and 'Balance_For_January_sales' in request.form:
        Balance_For_January_sales = request.form['Balance_For_January_sales']
        january_sales = request.form['january_sales']
        Balance_For_Feburary_sales = request.form['Balance_For_feburary_sales']
        Feburary_sales = request.form['Feburary_sales']
        Balance_For_March_sales = request.form['Balance_For_March_sales']
        march_sales = request.form['march_sales']
        Balance_For_April_sales = request.form['Balance_For_April_sales']
        april_sales = request.form['april_sales']
        Balance_For_may_sales = request.form['Balance_For_may_sales']
        may_sales = request.form['may_sales']
        Balance_For_June_sales = request.form['Balance_For_June_sales']
        june_sales = request.form['june_sales']
        Balance_For_July_sales = request.form['Balance_For_July_sales']
        july_sales = request.form['july_sales']
        Balance_For_August_sales = request.form['Balance_For_August_sales']
        august_sales = request.form['august_sales']
        Balance_For_september_sales = request.form['Balance_For_September_sales']
        september_sales = request.form['september_sales']
        Balance_For_october_sales = request.form['Balance_For_october_sales']
        october_sales = request.form['october_sales']
        Balance_For_November_sales = request.form['Balance_For_November_sales']
        november_sales = request.form['november_sales']
        Balance_For_December_sales = request.form['Balance_For_December_sales']
        december_sales = request.form['december_sales']

        #check if the unique_id is already in the database
        with engine.connect() as con:
         result = con.execute(text(f"SELECT * FROM Sales_figure WHERE unique_id = '{client_id}'"))
        sales = result.sales_figure.fetchone()
        if client:
                msg = 'The client already exists.'
                return redirect(url_for('home', msg = msg))
        #check if all the required fields are filled


#The page for the client registration
@app.route('/register_client', methods=['POST'])
def register_client():
     #get the data from the form
    if request.method=='POST' and 'unique_id' in request.form:
        unique_id = request.form['unique_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        date_of_birth = request.form['dob']
        country_of_birth = request.form['country_of_birth']
        sex = request.form['gender']
        marital_status = request.form['marital-status']
        occupation = request.form['occupation']
        gender_identity = request.form['gender-identity']
        sexual_orientation = request.form['sexual-orientation']
        phone_number = request.form['phone']
        address = request.form['line1']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip-code']
        country = request.form['country']
        email = request.form['email']
        ethnicity = request.form['ethnicity']
        race = request.form['race']
     #check if the unique_id is already in the database
        with engine.connect() as con:
            result = con.execute(text(f"SELECT * FROM client_profile WHERE unique_id = '{unique_id}'"))
            client = result.fetchone()
            if client:
                msg = 'The client already exists.'
                return redirect(url_for('home', msg = msg))
        #check if all the required fields are filled
        
        #insert the values in the database
        created_at = datetime.now()
        updated_at = datetime.now()
        created_by = session['username']
        updated_by = session['username']
        with engine.connect() as con:
            con.execute(text(f"INSERT INTO client_profile(created_by, created_at, updated_at, updated_by, unique_id, first_name, last_name, middle_name, date_of_birth,\
                                      country_of_birth, gender, marital_status, occupation, gender_identity,\
                                      sexual_orientation, phone_number, address, city, state, zip_code, country,\
                                      email, ethnicity, race)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}', '{first_name}', '{last_name}', '{middle_name}',\
                                      '{date_of_birth}', '{country_of_birth}', '{sex}', '{marital_status}',\
                                      '{occupation}', '{gender_identity}','{sexual_orientation}', '{phone_number}',\
                                      '{address}', '{city}', '{state}', '{zip_code}', '{country}', '{email}',\
                                      '{ethnicity}', '{race}'\
                                    )"))
            
            con.execute(text(f"INSERT INTO customer_information(created_by, created_at, updated_at, updated_by, unique_id,\
                             customer_last_name, customer_first_name, customer_middle_name, customer_date_of_birth,\
                             customer_Estimated_delivery_date, customer_address, Residency_of_Customer,customer_state,\
                             customer_Zip, customer_telephone_number, customer_type_of_insurance, customer_race,hispanic,\
                             customer_country_of_birth, customer_primary_language, check_if_interpreter_is_needed)\ 
                             VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}',\
                             '{last_name}', '{first_name}', '{middle_name}', '{dob}','{customer_Estimated_delivery_date}',\
                             '{address}', '{Residency}', '{customer_state}', '{code}', '{tel}', '{type_of_insurance}', '{customer_race}', '{hispanic}',\
                             '{country_of_birth}', '{primary_language}', '{check_if_interpreter_is_needed}',\ 
                             ')"))
        
            con.execute(text(f"INSERT INTO guarantor_information(created_by, created_at, updated_at, updated_by,unique_id, guarantor_unique_id)\
                              guarantor_address, guarantor_residency, guarantor_state, guarantor_telephone_number, guarantor_type_of_insurance,\
                             guarantor_race, guarantor_hispanic, guarantor_country_of_birth, guarantor_primary_language)\ 

                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}', '{unique_id}+guarantor'
                                      '{address}', '{residency}', '{city}', '{tel}', '{type_of_insurance}',\
                                      '{guarantor_race}', '{guarantor_hispanic}', '{country_of_birth}', '{primary_language}',\ 
                                      )"))
            con.execute(text(f"INSERT INTO employee_records(created_by, created_at,updated_at, updated_by, unique_id,)\
                             employee_last_name, employee_first_name, employee_middle_name, employee_date_of_birth,\
                             employee_Estimated_delivery_date, employee_address, Residency_of_employee, employee_state,\
                             employee_Zip, employee_telephone_number, employee_type_of_insurance, employee_race, employee_hispanic,\
                             employee_country_of_birth, employee_primary_language, check_if_interpreter_is_needed)\ 
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}','{unique_id}'
                             '{last_name}', '{first_name}', '{middle_name}', '{dob}','{employee_Estimated_delivery_date}',\
                             '{address}', '{Residency}', '{city}', '{code}', '{tel}', '{type_of_insurance}', '{employee_race}', '{hispanic}',\
                             '{country_of_birth}', '{primary_language}', '{employee_check_if_interpreter_is_needed}',\ 
                             ')"))
         
                                      
    
            con.execute(text(f"INSERT INTO financial_data(created_by, created_at,updated_at, updated_by, unique_id)\
                              Balance_For_January_B/D, january_B/D, Balance_For_Feburary_B/D, Feburary_B/D, Balance_For_March_B/D,\
                              march_B/D, Balance_For_April_B/D, april_B/D, Balance_For_may_B/D, may_B/D, Balance_For_June_B/D,\
                              june_B/D, Balance_For_July_B/D, july_B/D, Balance_For_August_B/D, august_B/D, Balance_For_september_B/D,\
                             september_B/D, Balance_For_october_B/D, october_B/D, Balance_For_November_B/D, november_B/D, Balance_For_December_B/D,\
                             december_B/D)\
                            VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}'
                            '{Balance_For_January_B/D}', '{january_B/D}', '{Balance_For_Feburary_B/D}', '{Feburary_B/D}', '{Balance_For_March_B/D}',\
                              '{march_B/D}', '{Balance_For_April_B/D}', '{april_B/D}', '{Balance_For_may_B/D}', '{may_B/D}', '{Balance_For_June_B/D}',\
                              '{june_B/D}', '{Balance_For_July_B/D}', '{july_B/D}', '{Balance_For_August_B/D}', '{august_B/D}', '{Balance_For_september_B/D}',\
                             '{september_B/D}', '{Balance_For_october_B/D}', '{october_B/D}', '{Balance_For_November_B/D}', '{november_B/D}', '{Balance_For_December_B/D}',\
                             '{december_B/D}'\
                            )"))
            
            con.execute(text(f"INSERT INTO inventory_levels(created_by, created_at, updated_at, updated_by, unique_id)\
                                Balance_For_January_inventory, january_inventory, Balance_For_Feburary_inventory, Feburary_inventory, Balance_For_March_inventory,\
                              march_inventory, Balance_For_April_inventory, april_inventory, Balance_For_may_inventory, may_inventory, Balance_For_June_inventory,\
                              june_inventory, Balance_For_July_inventory, july_inventory, Balance_For_August_inventory, august_inventory, Balance_For_september_inventory,\
                             september_inventory, Balance_For_october_inventory, october_inventory, Balance_For_November_inventory, november_inventory, Balance_For_December_inventory,\
                             december_inventory)\
                            VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}'
                            '{Balance_For_January_inventory}', '{january_inventory}', '{Balance_For_Feburary_inventory}', '{Feburary_inventory}', '{Balance_For_March_inventory}',\
                              '{march_inventory}', '{Balance_For_April_inventory}', '{april_inventory}', '{Balance_For_may_inventory}', '{may_inventory}', '{Balance_For_June_inventory}',\
                              '{june_inventory}', '{Balance_For_July_inventory}', '{july_inventory}', '{Balance_For_August_inventory}', '{august_inventory}', '{Balance_For_september_inventory}',\
                             '{september_inventory}', '{Balance_For_october_inventory}', '{october_inventory}', '{Balance_For_November_inventory}', '{november_inventory}', '{Balance_For_December_inventory}',\
                             '{december_inventory}'\
                            )"))                
            con.execute(text(f"INSERT INTO sales_figure(created_by, created_at, updated_at, updated_by, unique_id)\
                            Balance_For_January_sales, january_sales, Balance_For_Feburary_sales, Feburary_sales, Balance_For_March_sales,\
                              march_sales, Balance_For_April_sales, april_sales, Balance_For_may_sales, may_sales, Balance_For_June_sales,\
                              june_sales, Balance_For_July_sales, july_sales, Balance_For_August_sales, august_sales, Balance_For_september_sales,\
                             september_sales, Balance_For_october_sales, october_sales, Balance_For_November_sales, november_sales, Balance_For_December_sales,\
                             december_sales)\
                            VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}'
                            '{Balance_For_January_sales}', '{january_sales}', '{Balance_For_Feburary_sales}', '{Feburary_sales}', '{Balance_For_March_sales}',\
                            '{march_sales}', '{Balance_For_April_sales}', '{april_sales}', '{Balance_For_may_sales}', '{may_sales}', '{Balance_For_June_sales}',\
                            '{june_sales}', '{Balance_For_July_sales}', '{july_sales}', '{Balance_For_August_sales}', '{august_sales}', '{Balance_For_september_sales}',\
                             '{september_sales}', '{Balance_For_october_sales}', '{october_sales}', '{Balance_For_November_sales}', '{november_sales}', '{Balance_For_December_sales}',\
                             '{december_sales}'\
                            )"))
        
        
            con.commit()
          if  client_profile and customer_information and guarantor_information and employees_records and inventory_levels and sales_figure:
           
                #display the client data
                  return render_template('profile.html', client = client = client_profile, customer = customer_information, guarantor = guarantor_information, employees = employees_records, inventory = inventory_levels, sales = sales_figure)
        else:
                #redirect to the home page
                msg = 'The client does not exist.'
                return redirect(url_for('home', msg = msg))
    return redirect(url_for('login'))
    
                 














       
