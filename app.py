from flask import Flask, request, jsonify,render_template
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


def load_student_data():
    with open('student_details.json', 'r') as file:
        student_data = json.load(file)
        return student_data


@app.route('/students', methods=['GET', 'POST'])
def get_students():
    # Read student details from the file (assuming it's in JSON format)

    if request.method == 'GET':
        student_data = load_student_data()

        page_number = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 10))

        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size

        paginated_data = student_data[start_index:end_index]

        return render_template('display_students.html', student_data=paginated_data)


@app.route('/students/filter', methods=['GET', 'POST'])
def get_students_filtered():
    error = None
    if request.method == 'POST':
        student_data = load_student_data()

        name = request.form['name']  ## which page the user is requesting
        marks = request.form['marks']
        
        filtered_data = []

        for student in student_data:
            if (name is None or student['name'].lower() == name.lower()) or \
                    (marks is None or student['total_marks'] == int(marks)):
                filtered_data.append(student)

        return render_template('display_students.html', student_data=filtered_data)

    return render_template('get_students.html', error=error)


if __name__ == '__main__':
    app.run()
