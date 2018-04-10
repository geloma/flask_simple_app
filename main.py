from flask import Flask, Response, request, session, url_for, redirect, json
from src.auth import Auth
import base64


app = Flask(__name__)
app.config.update(DEBUG = True, SECRET_KEY = base64.b64encode('S3cr3t'))

@app.route("/index", methods=["GET"])
def index():
	return Response('''
		<html>
			<head>
				<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>	
				<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
				<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">
				<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>
			</head>
			<body class='container'>
				<form style='margin-top:20%' onsubmit='return false;'>
					<div class='row'>
						<div class='col-md-4 offset-md-4 text-center'>
							<h1>Sign In</h1>
						</div>
					</div>
					<div class='row'>
						<div class='col-md-4 offset-md-4'>
							<label>Username</label>
							<input type=text id="username" class="form-control">
						</div>
					</div>
					<div class='row' style='margin-top:20px;'>
						<div class='col-md-4 offset-md-4'>
							<label>Password</label>
							<input type=password id="password" class="form-control">
						</div>
					</div>
					<div class='row' style='margin-top:20px;'>
						<div class='col-md-4 offset-md-4'>
							<button id="login" class="btn btn-primary btn-block waves-effect waves-light">Sign In</button>
						</div>
					</div>
					<div class='row'>
						<div class='col-md-4 offset-md-4' style='margin-top:20px;'>
							<p class="text-center" id="response"></p>
						</div>
					</div>
				</form>
				<script>
					$(document).ready(function(){
						$('#login').click(function(){
							var username = $("#username").val();
							var password = $("#password").val();
							if(username == ""){
								$("#response").html("<b style='color: #f22;'>Empty Username</b>");
								return false;
							}
							if(password == ""){
								$("#response").html("<b style='color: #f22;'>Empty Password</b>");
								return false;
							}
							$.ajax({
								type : "POST",
								url : "/login",
								data: {user: username, pass: password},
								success: function(response) {
									if(response == 1){
										$("#response").html("<b style='color: #2f2;'>Welcome!</b>");
										setTimeout(function(){
											location = 'dashboard';
										}, 600);
									}else{
										$("#response").html("<b style='color: #f22;'>Username/Password Wrong</b>");
									}
								}
							});
						});
					});
				</script>
			</body>
        </html>
        ''')

@app.route("/login", methods=["POST"])
def login():
	username = request.form.get('user')
	password = request.form.get('pass')
	if not username or not password:
		return Response("0")
	auth = Auth(username, password)
	if auth.status:
		session['logged'] = True
		session['username'] = username
		return Response("1")
	else:
		return Response("0")


@app.route("/dashboard", methods=["GET"])
def dashboard():
	if session.get('logged') == True:
		auth = Auth("", "")
		name = auth.get_name_by_user(session.get('username'))
		role = auth.get_name_by_role(session.get('username'))
		admin = False
		style = 'style="display: none;"'
		if role == 1:
			admin = True
			style = ''
			name = "Admin "+name
		else:
			name = "User "+name
		return Response('''
			<html>
				<head>
					<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>	
					<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
					<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">
					<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>
					<link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
					<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.12.1/bootstrap-table.min.css" />
					<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.12.1/bootstrap-table.min.js"></script>
				</head>
				<body>
					<nav>
						<div class="nav-wrapper blue lighten-1">
						  <a href="dashboard" class="brand-logo" style='margin-left: 10px;'>User APP</a>
						  <ul id="nav-mobile" class="right hide-on-med-and-down">
							<li>'''+ name.upper() +'''</li>
							<li><a href="logout" ><i class='fa fa-sign-out fa-2x'></i></a></li>
						  </ul>
						</div>
					</nav>
					<div class='row' '''+ style +'''>
						<div class='col-md-8 offset-2 text-center'>
							<h4 class='grey-text'>User Administration</h4>
							<table id="userTable" 
								   data-url="service/get_users"
								   data-height="300"
								   data-search="true"
								   class='table table-striped'>
								<thead>
									<tr>
										<th data-field="id" data-formatter="table.tools" data-width="200"></th>
										<th data-field="id">ID</th>
										<th data-field="name">Name</th>
										<th data-field="user">User</th>
										<th data-field="role" data-formatter="table.role_formatter">Role</th>
									</tr>
									</thead>
							</table>
						</div>
					</div>
				</body>
				<script>
					var table = {};
					table.actions = {};
					table.actions.edit = function(id) { alert('default edit for id: ' + id); };
					table.actions.delete = function(id) { alert('default delete for id: ' + id); };
					table.role_formatter = function(value, row, index){return (value == 1)?"Administrator":"User";};
					table.tools = function(value, row, index){
						return "<a title='edit' class='btn btn-default grey darken-1 white-text' onclick='table.actions.edit("+value+");'><i class='fa fa-pencil'></i></a>"
							+ "<a title='remove' class='btn btn-danger grey darken-5 white-text' onclick='table.actions.delete("+value+");'><i class='fa fa-trash'></i></a>";
					};
					$(document).ready(function(){
						$("#userTable").bootstrapTable();
					});
				</script>
			</html>
		''')
	else:
		return redirect(url_for('index'))

@app.route("/service/get_users", methods=["GET"])
def get_users():
	if session.get('logged') == True:
		auth = Auth("", "")
		role = auth.get_name_by_role(session.get('username'))
		if role == 1:
			users = auth.get_users()
			for i in users:
				del i['salt']
				del i['pass']
			return Response(
				response=json.dumps(users),
				status=200,
				mimetype='application/json'
			)
		return redirect(url_for('dashboard'))

@app.route("/logout", methods=["GET"])
def logout():
	session['logged'] = False
	return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
