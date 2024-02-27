from flask import Flask, render_template, request, redirect, url_for, flash,session
import mysql.connector
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'       
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'bigmart'   

mysql = MySQL(app)
app.secret_key = 'SALES@123'


@app.route("/")
def default():
    if 'email' in session:
        return render_template('home.html')
    return render_template("index.html")

@app.route("/predict")
def predict():
    if 'email' in session:
        return render_template('sales_prediction.html')
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'email' in session:
        # If user is already logged in, redirect to home page or another appropriate page
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

         # Validate that none of the fields are empty
        if not username or not email or not password:
            flash('Please fill in all the fields.', 'danger')
            return redirect(url_for('register'))


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (username, email,password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful! Please log in.', 'success')

        return redirect(url_for('default'))

    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        # If user is already logged in, redirect to home page or another appropriate page
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['email'] = email  # Store the email in session to indicate user is logged in
            flash('Login successful!', 'success')
            # Redirect to some page after successful login
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')




@app.route("/home")
def home():
    if 'email' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route("/about")
def about():
    if 'email' in session:
        return render_template('components/auth_about.html')
    return render_template("about.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Validate that none of the fields are empty
        if not name or not email or not message:
            flash('Please fill in all the fields.', 'danger')
            return redirect(url_for('contact'))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        mysql.connection.commit()
        cur.close()

        flash('Your message has been sent successfully!', 'success')

        return redirect(url_for('contact'))  # Redirect to the contact page after successful submission
    if 'email' in session:
        return render_template('components/auth_contact.html')
    return render_template('contact.html')

@app.route("/logout")
def logout():
    session.pop('email', None)  # Remove email from session to log out the user
    return redirect(url_for('login'))

# main driver function
if __name__ == '__main__':
    app.run(debug=True)
