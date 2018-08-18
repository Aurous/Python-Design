from flask import Flask, request, url_for, render_template, redirect, session
import json
from pyfunc import pyfunc, users, projects
with open('settings.json') as jsonvars:
    data = json.load(jsonvars)

app = Flask(__name__)
app.debug = True
app.secret_key = data['app.key']

sql = pyfunc(data['sql.settings'])
sql.project = projects()
@app.route("/",methods = ['POST', 'GET'])
def index():
	return render_template("index.html")
	
@app.route("/signup",methods = ['POST', 'GET'])
def signup():
	error = request.args.get('error') if request.args.get('error') is not None else ''
	return render_template("signup.html", error=error)
	
@app.route("/login",methods = ['POST', 'GET'])
def login():
	error = ''
	if request.method == 'POST':
		session['user'] = sql.login(request.form['email'], request.form['password'])
		if(session['user'] != False):
			return redirect(url_for('home'))
		else:
			error = "Failed to Login"
	return render_template("login.html", error=error)

@app.route("/logout",methods = ['POST', 'GET'])
def logout():
	try:
		if(session['user'].logged):
			session['user'].logged = False
	except:
		return redirect(url_for('index'))
	return redirect(url_for('index'))

@app.route("/home", methods = ['POST', 'GET'])
def home():
	error = request.args.get('error') if request.args.get('error') is not None else ''
	success = request.args.get('success') if request.args.get('success') is not None else ''
	try:
		if(session['user']['logged']):
			if request.method == 'POST':
				if(sql.project.create(sql, session['user'], request.form['name'])):
					return redirect(url_for('edit', id=sql.cursor.lastrowid))
			return render_template("home.html", projects=sql.project.get(sql, session['user'], all=True), error=error, success=success)
	except:
		return redirect(url_for('index'))
	return redirect(url_for('index'))
		
@app.route("/project", methods = ['POST', 'GET'])
def project():
	return request.args.get('id')
	
@app.route("/delete", methods = ['POST', 'GET'])
def delete():
	try:
		if(session['user']['logged']):
			if request.method == "POST":
				if request.args.get('id').isdigit():
					if(sql.project.delete(sql, session['user'], request.args.get('id'))):
						return redirect(url_for('home', success="Project Deleted Sucessfully"))
	except:
		return redirect(url_for('home', error="Error Deleting Project"))
	return render_template("delete.html", project=sql.project.get(sql, session['user'], id=request.args.get('id')))

@app.route("/view",methods = ['POST', 'GET'])
def view():
	return render_template('view.html', project=sql.project.get(sql, session['user'], id=request.args.get('id')))
	
@app.route("/edit",methods = ['POST', 'GET'])
def edit():
	return render_template('edit.html', project=sql.project.get(sql, session['user'], id=request.args.get('id')))
	
#@app.route("/test")
#def test():
#	return render_template("test.html")
if __name__ == "__main__":
    app.debug = True
    app.run()