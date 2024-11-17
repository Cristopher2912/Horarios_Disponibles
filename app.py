from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Base de datos simulada
users = {
    "admin": {"password": "1234", "leader": "Administrador"}
}
schedules = [
    {"day": "Lunes", "start_time": "13:00", "end_time": "15:00", "groups_registered": []},
    {"day": "Lunes", "start_time": "15:00", "end_time": "17:00", "groups_registered": []},
    {"day": "Martes", "start_time": "15:00", "end_time": "17:00", "groups_registered": []},
    {"day": "Martes", "start_time": "17:00", "end_time": "19:00", "groups_registered": []},
    {"day": "Miércoles", "start_time": "15:00", "end_time": "17:00", "groups_registered": []},
    {"day": "Miércoles", "start_time": "17:00", "end_time": "19:00", "groups_registered": []},
    {"day": "Jueves", "start_time": "13:00", "end_time": "15:00", "groups_registered": []},
    {"day": "Jueves", "start_time": "15:00", "end_time": "17:00", "groups_registered": []},
    {"day": "Jueves", "start_time": "17:00", "end_time": "19:00", "groups_registered": []},
    {"day": "Viernes", "start_time": "13:00", "end_time": "15:00", "groups_registered": []},
    {"day": "Viernes", "start_time": "15:00", "end_time": "17:00", "groups_registered": []},
    {"day": "Viernes", "start_time": "17:00", "end_time": "19:00", "groups_registered": []},
]

# Modelo de usuario
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Rutas principales
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)

        if user and user['password'] == password:
            login_user(User(username))
            return redirect(url_for('view_schedule'))
        else:
            flash('Credenciales inválidas', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        leader = request.form.get('leader')

        if username in users:
            flash('El usuario ya existe', 'error')
        else:
            users[username] = {"password": password, "leader": leader}
            flash('Registro exitoso', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/view_schedule')
@login_required
def view_schedule():
    return render_template('view_schedule.html', schedules=schedules)

@app.route('/reserve_schedule', methods=['POST'])
@login_required
def reserve_schedule():
    day = request.form.get('day')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    for schedule in schedules:
        if schedule['day'] == day and schedule['start_time'] == start_time and schedule['end_time'] == end_time:
            if len(schedule['groups_registered']) < 4:
                schedule['groups_registered'].append({
                    "group": current_user.id,
                    "leader": users[current_user.id]['leader']
                })
                flash('Horario reservado con éxito', 'success')
            else:
                flash('El horario ya está lleno', 'error')
            break
    else:
        flash('Horario no encontrado', 'error')

    return redirect(url_for('view_schedule'))

if __name__ == '__main__':
    app.run(debug=True)
