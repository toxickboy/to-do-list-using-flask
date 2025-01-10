from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database to store tasks
tasks = []

# Helper function to find task by ID
def find_task(task_id):
    return next((task for task in tasks if task['id'] == task_id), None)

# Create a task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

# Retrieve a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if task:
        return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

# Update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task(task_id)
    if task:
        data = request.json
        task['title'] = data.get('title', task['title'])
        task['description'] = data.get('description', task['description'])
        task['completed'] = data.get('completed', task['completed'])
        return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if task:
        tasks.remove(task)
        return jsonify({'message': 'Task deleted'}), 200
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
