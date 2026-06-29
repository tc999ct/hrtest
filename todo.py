#!/usr/bin/env python3
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def add_task(description):
    tasks = load_tasks()
    tasks.append({'id': len(tasks) + 1, 'description': description, 'done': False})
    save_tasks(tasks)
    print(f'追加: {description}')

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print('タスクはありません。')
        return
    for t in tasks:
        status = '✓' if t['done'] else ' '
        print(f"[{status}] {t['id']}: {t['description']}")

def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['done'] = True
            save_tasks(tasks)
            print(f'完了: {t["description"]}')
            return
    print(f'ID {task_id} のタスクが見つかりません。')

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        print(f'ID {task_id} のタスクが見つかりません。')
        return
    save_tasks(new_tasks)
    print(f'削除: ID {task_id}')

def print_usage():
    print('使い方:')
    print('  todo add "タスク説明"   # タスクを追加')
    print('  todo list               # タスク一覧表示')
    print('  todo done <ID>          # タスクを完了とする')
    print('  todo rm <ID>            # タスクを削除')
    print('  todo help               # このヘルプを表示')

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    cmd = sys.argv[1]
    if cmd == 'add':
        if len(sys.argv) < 3:
            print('エラー: タスク説明が必要です。')
            return
        desc = ' '.join(sys.argv[2:])
        add_task(desc)
    elif cmd == 'list':
        list_tasks()
    elif cmd == 'done':
        if len(sys.argv) < 3:
            print('エラー: IDが必要です。')
            return
        try:
            tid = int(sys.argv[2])
        except ValueError:
            print('エラー: IDは整数で指定してください。')
            return
        complete_task(tid)
    elif cmd == 'rm' or cmd == 'remove' or cmd == 'del':
        if len(sys.argv) < 3:
            print('エラー: IDが必要です。')
            return
        try:
            tid = int(sys.argv[2])
        except ValueError:
            print('エラー: IDは整数で指定してください。')
            return
        delete_task(tid)
    elif cmd == 'help' or cmd == '-h' or cmd == '--help':
        print_usage()
    else:
        print(f'不明なコマンド: {cmd}')
        print_usage()

if __name__ == '__main__':
    main()