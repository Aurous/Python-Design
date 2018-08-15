import mysql.connector

class users:
	def __init__(self, id, name, email):
		self.id = id
		self.name = name
		self.email = email
		self.logged = True
		
class pyfunc:
	def __init__(self, host, user, passwd, database):
		self.con = mysql.connector.connect(
			host=host,
			user=user,
			passwd=passwd,
			database=database
		)
		self.cursor = self.con.cursor()
	#def signup(self, users_name, users_email, users_password):
	def signup(self, users_name, users_email, users_password):
		self.cursor.execute("SELECT * FROM `users` WHERE `users_email` = %s",(users_email, ))
		results = self.cursor.fetchall()
		if(self.cursor.rowcount == 0):
			self.cursor.execute("INSERT INTO `users` (users_name, users_email, users_password) VALUES (%s, %s, %s)", (users_name, users_email, users_password))
			self.con.commit()
			print("User Added")
		else:
			print("Email Already In Use")
	def login(self, users_email, users_password):
		self.cursor.execute("SELECT * FROM `users` WHERE `users_email` = %s AND `users_password` = %s", (users_email, users_password, ))
		results = self.cursor.fetchall()
		if(self.cursor.rowcount == 1):
			print("Logged In")
			self.user = users(results[0][0], results[0][1], results[0][2])
			#print(self.user)\
			return True
		else:
			print("Failed Logging In")
			return False
	def logged(self):
		try:
			if(user.logged):
				return True
			else:
				return False
		except:
			return False
	def logout(self):
		#try:
		if(self.user.logged):
			try:
				self.user.logged = False
			except:
				print("Error logging out")

class projects:
	def create(self, sql, user, name):
		sql.cursor.execute("INSERT INTO `projects` (projects_name, projects_data, users_id) VALUES (%s, %s, %s)", (name, '', user.id))
		sql.con.commit()
		if(sql.cursor.rowcount == 1):
			print("Project Added")
		
	def get(self, sql, user, all=False, id=0):
		if(all):
			sql.cursor.execute("SELECT `projects_name`, `projects_id` FROM projects WHERE users_id = %s", (user.id, ))
			results = sql.cursor.fetchall()
			return results
		else:
			sql.cursor.execute("SELECT * FROM projects WHERE users_id = %s AND projects_id = %s", (user.id, id, ))
			results = sql.cursor.fetchall()
			return results
			
	def delete(self, sql, user, id):
		sql.cursor.execute("DELETE FROM `projects` WHERE `projects_id` = %s AND `users_id` = %s", (id, user.id, ))
		sql.con.commit()
		if(sql.cursor.rowcount == 1):
			print("Project Deleted")
		
	def update(self, sql, user, name, data, id):
		sql.cursor.execute("UPDATE `projects` SET `projects_name`= %s,`projects_data`= %s WHERE `users_id`= %s AND `projects_id`= %s", (name, data, user.id, id))
		sql.con.commit()
		if(sql.cursor.rowcount == 1):
			print("Project Updated")
		
		
		