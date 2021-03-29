import sqlite3
import markdown
from flask import Flask, render_template, request, flash, redirect, url_for

def db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Letmein123!'

@app.route('/')
def index():
    conn = db_connection()
    db_notes = conn.execute('SELECT id, created, content FROM notes;').fetchall()
    conn.close()

    notes = []
    for note in db_notes:
       note = dict(note)
       note['content'] = markdown.markdown(note['content'])
       notes.append(note)

    return render_template('index.html', notes=notes)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    conn = db_connection()

    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Content is required!')
            return redirect(url_for('index'))
        conn.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit(note_id):

    if request.method == 'GET':
        conn = db_connection()
        # note = conn.execute('SELECT id, created, content FROM notes WHERE id = 1;').fetchall()
        note = conn.execute('SELECT * FROM notes WHERE id = ?;', (note_id,)).fetchone()
        conn.close()

        note = dict(note)

        return render_template('edit.html', note=note)

    if request.method == 'POST':
        conn = db_connection()
        content = request.form['content']
        if not content:
            flash('Content is required!')
            return redirect(url_for('index'))

        conn.execute('DELETE FROM notes where id =?;', (note_id,))
        conn.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

@app.route('/delete/<int:note_id>', methods=['GET'])
def delete(note_id):
    conn = db_connection()
    conn.execute('DELETE FROM notes where id =?;', (note_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))
