from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'tasks.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            module TEXT,
            deadline TEXT,
            complete INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return """
    <h1>Smart Study Tracker API</h1>
    <p>Available routes:</p>
    <ul>
        <li>GET /tasks</li>
        <li>POST /tasks</li>
        <li>PUT /tasks/&lt;id&gt;</li>
        <li>DELETE /tasks/&lt;id&gt;</li>
    </ul>
    """

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    rows = c.fetchall()
    conn.close()

    tasks = []
    for r in rows:
        tasks.append({
            'id': r[0],
            'title': r[1],
            'module': r[2],
            'deadline': r[3],
            'complete': bool(r[4])
        })

    return jsonify(tasks)


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        INSERT INTO tasks (title, module, deadline, complete)
        VALUES (?, ?, ?, ?)
    ''', (data['title'], data['module'], data['deadline'], 0))

    conn.commit()
    task_id = c.lastrowid
    conn.close()

    return jsonify({
        "message": "Task added",
        "task": {
            "id": task_id,
            "title": data['title'],
            "module": data['module'],
            "deadline": data['deadline'],
            "complete": False
        }
    })

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE tasks
        SET title=?, module=?, deadline=?, complete=?
        WHERE id=?
    ''', (data['title'], data['module'], data['deadline'], data['complete'], id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task updated"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id=?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted"})

@app.route('/tasks/<int:id>/toggle', methods=['PATCH'])
def toggle_task(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE tasks SET complete = NOT complete WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task toggled"})

@app.route('/add-real')
def add_real():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("INSERT INTO tasks (title, module, deadline, complete) VALUES (?, ?, ?, ?)",
              ("Foundations of Computation", "Comp5001", "2026-01-12", 0))

    c.execute("INSERT INTO tasks (title, module, deadline, complete) VALUES (?, ?, ?, ?)",
              ("Enterprise Engineering", "Comp5046", "2026-04-07", 0))

    conn.commit()
    conn.close()

    return "Real tasks added"

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE id=?', (id,))
    r = c.fetchone()
    conn.close()

    if r:
        return jsonify({
            'id': r[0],
            'title': r[1],
            'module': r[2],
            'deadline': r[3],
            'complete': bool(r[4])
        })
    else:
        return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)