import flask
import csv
import io


app = flask.Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return flask.jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        flask.abort(404)
    return flask.jsonify({'task': task[0]})


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks.csv', methods=['GET'])
def get_tasks_csv():
    f = io.StringIO()
    writer = csv.DictWriter(f, fieldnames=['id', 'title', 'description', 'done'])
    writer.writeheader()
    for t in tasks:
        writer.writerow(t)
    response = flask.Response(f.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = u'attachment; filename=tasks.csv'
    return response


@app.route('/')
def index():
    return "Hello!"


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = flask.url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(debug=True)
