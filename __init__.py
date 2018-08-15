from flask import Flask, request, url_for, render_template, redirect
from pyfunc import pyfunc, users, projects
sql = pyfunc("localhost","py.ryansdesign","H2$8XKgnmRQ644!7a","py.ryansdesign")
sql.project = projects()
app = Flask(__name__)
app.config['DEBUG'] = True
@app.route("/")
def index():
	return render_template("index.html")
if __name__ == "__main__":
    app.debug = True
    app.run()

@app.route("/login",methods = ['POST', 'GET'])
def login():
	error = ''
	if request.method == 'POST':
		if(sql.login(request.form['email'], request.form['password'])):
			return redirect(url_for('home'))
		else:
			error = "Failed to Login"
	return render_template("login.html", error=error)
	
@app.route("/home")
def home():
	return render_template("home.html")