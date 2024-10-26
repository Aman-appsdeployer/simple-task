from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234@aman'
app.config['MYSQL_DB'] = 'uses'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    due_date = request.form['due_date']
    description = request.form['description']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (task, due_date, description) VALUES (%s, %s, %s)", (task, due_date, description))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        task = request.form['task']
        due_date = request.form['due_date']
        description = request.form['description']
        cur.execute("UPDATE tasks SET task = %s, due_date = %s, description = %s WHERE id = %s", (task, due_date, description, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM tasks WHERE id = %s", (id,))
        task_data = cur.fetchone()
        cur.close()
        return render_template('edit_task.html', task=task_data)

@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
