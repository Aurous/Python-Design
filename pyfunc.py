import uuid
import hashlib
import mysql.connector

def check(hash, text):
	_hash, salt = hash.split(':')
	return _hash == hashlib.sha256(salt.encode() + text.encode()).hexdigest()

class users:
	def new(self, id, name, email):
		return {"id":id,"name":name,"email":email,"logged":True}
		
class pyfunc:
	def __init__(self, data):
		self.con = mysql.connector.connect(
			host=data['host'],
			user=data['user'],
			passwd=data['password'],
			database=data['database']
		)
		self.cursor = self.con.cursor(buffered=True)
	
	def signup(self, users_name, users_email, users_password):
		self.cursor.execute("SELECT * FROM `users` WHERE `users_email` = %s",(users_email, ))
		results = self.cursor.fetchall()
		if(self.cursor.rowcount == 0):
			self.cursor.execute("INSERT INTO `users` (users_name, users_email, users_password) VALUES (%s, %s, %s)", (users_name, users_email, users_password))
			self.con.commit()
			if(self.cursor.rowcount == 1):
				return True
		else:
			return False
	
	def login(self, users_email, users_password):
		self.cursor.execute("SELECT * FROM `users` WHERE `users_email` = %s", (users_email, ))
		results = self.cursor.fetchall()
		if self.cursor.rowcount == 1 and check(results[0][3],users_password):
			user = users()
			return user.new(results[0][0], results[0][1], results[0][2])
		else:
			return False
	
	def logged(self, user):
		try:
			if(user['logged']):
				return True
			else:
				return False
		except:
			return False
	
	def hashing(self, text):
		salt = uuid.uuid4().hex
		return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt

class projects:
	def create(self, sql, user, name):
		sql.cursor.execute("INSERT INTO `projects` (projects_name, projects_data, users_id) VALUES (%s, %s, %s)", (name, '', user['id']))
		sql.con.commit()
		if(sql.cursor.rowcount == 1):
			return True
		else:
			return False
		
	def get(self, sql, user, all=False, id=0):
		if(all):
			sql.cursor.execute("SELECT `projects_name`, `projects_id` FROM projects WHERE users_id = %s", (user['id'], ))
			results = sql.cursor.fetchall()
			return results
		elif(id != 0):
			sql.cursor.execute("SELECT * FROM projects WHERE users_id = %s AND projects_id = %s", (user['id'], id, ))
			if(sql.cursor.rowcount == 1):
				results = sql.cursor.fetchall()
				return results[0]
			else:
				return "Unable to get project data"
		else:
			return "No defined project"
			
	def delete(self, sql, user, id):
		sql.cursor.execute("DELETE FROM `projects` WHERE `projects_id` = %s AND `users_id` = %s", (id, user['id'], ))
		sql.con.commit()
		if(sql.cursor.rowcount == 1):
			return True
		else:
			return False
		
	def update(self, sql, user, name, data, id):
		sql.cursor.execute("UPDATE `projects` SET `projects_name`= %s,`projects_data`= %s WHERE `users_id`= %s AND `projects_id`= %s", (name, data, user['id'], id))
		sql.con.commit()
		if(sql.cursor.rowcount == 1):
			return True
		else:
			return False

class shares:
	def get(self, sql, user, all=False, id=0):
		if(all):
			sql.cursor.execute("SELECT * FROM users_has_projects WHERE users_id = %s", (user['id'], ))
			if(sql.cursor.rowcount == 1):
				result = sql.cursor.fetchall()
				projects = []
				for project in result:
					sql.cursor.execute("SELECT * FROM projects WHERE projects_id = %s", (project[1], ))
					if(sql.cursor.rowcount == 1):
						results = sql.cursor.fetchall()
						full = list(results[0])
						full.append(project[2])
						projects.append(tuple(full))
				return projects
		elif(id != 0):
			sql.cursor.execute("SELECT * FROM users_has_projects WHERE users_id = %s AND projects_id = %s", (user['id'], id, ))
			if(sql.cursor.rowcount == 1):
				result = sql.cursor.fetchall()
				for project in result:
					sql.cursor.execute("SELECT * FROM projects WHERE projects_id = %s", (project[1], ))
					if(sql.cursor.rowcount == 1):
						results = sql.cursor.fetchall()
						full = list(results[0])
						full.append(project[2])
				return tuple(full)
			else:
				return "Unable to get project data"
		else:
			return "No defined project"
	
	def sharing(self):
		return "test"
	
	def add(self, sql, user, id, email, access):
		sql.cursor.execute("SELECT * FROM projects WHERE users_id = %s AND `projects_id` = %s", (user['id'], id, ))
		if(sql.cursor.rowcount == 1):
			sql.cursor.execute("SELECT * FROM users_has_projects WHERE `users_id` = %s AND `projects_id` = %s", (email, id, ))
			if(sql.cursor.rowcount == 0):
				self.cursor.execute("INSERT INTO `users_has_projects` (`users_id`, `projects_id`, `users_has_rights`) VALUES (%s, %s, %s)",(email, id, access))
				if(sql.cursor.rowcount == 1):
					return True
		return False
	
	def delete(self, sql, user, id, email, access):
		sql.cursor.execute("SELECT * FROM projects WHERE users_id = %s AND `projects_id` = %s", (user['id'], id, ))
		if(sql.cursor.rowcount == 1):
			sql.cursor.execute("SELECT * FROM users_has_projects WHERE `users_id` = %s AND `projects_id` = %s", (email, id, ))
			if(sql.cursor.rowcount == 1):
				self.cursor.execute("DELETE FROM `users_has_projects` WHERE `users_id` = '%s' AND `projects_id` = '%s' AND `users_has_rights` = '%s'",(email, id, access))
				if(sql.cursor.rowcount == 1):
					return True
		return False
	
	def id2email(self, sql, id):
		sql.cursor.execute("SELECT `users_email` FROM users WHERE users_id = %s", (id, ))
		if(sql.cursor.rowcount == 1):
			result = sql.cursor.fetchall()
			return result[0][0]
		else:
			return False
			
	def email2id(self, sql, email):
		sql.cursor.execute("SELECT `users_id` FROM users WHERE users_email = %s", (email, ))
		if(sql.cursor.rowcount == 1):
			result = sql.cursor.fetchall()
			return result[0][0]
		else:
			return False