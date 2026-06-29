#!/usr/bin/env python3
"""TODO アプリ Web版 (Flask)"""
import json
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def next_id(tasks):
    return max((t['id'] for t in tasks), default=0) + 1


@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    desc = request.form.get('description', '').strip()
    if desc:
        tasks = load_tasks()
        tasks.append({'id': next_id(tasks), 'description': desc, 'done': False})
        save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['done'] = not t['done']
            break
    save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
