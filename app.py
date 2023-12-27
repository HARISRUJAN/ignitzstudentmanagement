from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_records.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)  
    education_level = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)


@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        education_level = request.form['education_level']
        phone_number = request.form['phone_number']

        new_student = Student(full_name=full_name, email=email, education_level=education_level, phone_number=phone_number)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_student.html')

@app.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get(id)

    if request.method == 'POST':
        student.full_name = request.form['full_name']
        student.email = request.form['email']
        student.education_level = request.form['education_level']
        student.phone_number = request.form['phone_number']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_student.html', student=student)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.get(id)

    if student:
        db.session.delete(student)
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
