"""
This is an employee REST API
Created by: Akiva Shor
Last edited: 2022-03-25
"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# Constants
from sqlalchemy.orm import validates

POST_METHOD = 'POST'
GET_METHOD = 'GET'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
ID_NUMBER = 'id_number'
BASE_URL = 'http://127.0.0.1:5000'
EMPLOYEES = 'employees'
EMPLOYEES_ROUTE = f'/{EMPLOYEES}'

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Employee(db.Model):
    """
    An employee class inherited from the db.Model
    """
    id_number = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)

    @validates(FIRST_NAME, LAST_NAME)
    def convert_capital(self, key, value):
        value = ''.join([i for i in value if i.isalpha()])  # Remove non letters chars
        return value.capitalize()

    def __repr__(self):
        return f'Employee: {self.first_name} {self.last_name}'

    def get_instance_dict(self):
        instance_dict = {key: value for key, value in self.__dict__.items() if
                         not key.startswith('_') and not callable(key)}
        return instance_dict


@app.route('/')
def index():
    return 'Congrats - You have reached the main url index'


@app.route(EMPLOYEES_ROUTE, methods=[GET_METHOD])
def get_employees():
    """
    Get a list of all get_employees dictionaries from the db
    :return: employees_json : A dict holding all of the employees data dicts
    :rtype: Dict
    """
    all_employees = Employee.query.all()
    data_list = []
    for employee in all_employees:
        employee_dict = employee.get_instance_dict()
        data_list.append(employee_dict)
    employees_json = {EMPLOYEES: data_list}
    return employees_json


@app.route(f'{EMPLOYEES_ROUTE}/<id_number>')
def get_single_worker(id_number):
    """
    Get a specific employee data by id number
    :param id_number: The wanted employee id number
    :type id_number: Int
    :return: employee_dict
    :rtype: Dict
    """
    employee = Employee.query.filter(Employee.id_number == id_number).first()
    employee_dict = employee.get_instance_dict()
    return employee_dict


@app.route(EMPLOYEES_ROUTE, methods=[POST_METHOD])
def add_employee():
    """
    This will post a new employee to the db.
    The request must include: first_name, last_name and id_number.
    It returns the employee data from the db to verify it was posted successfully
    :return: employee_dict
    :rtype: Dict
    """
    print(request.json)
    employee = Employee(first_name=request.json[FIRST_NAME],
                        last_name=request.json[LAST_NAME],
                        id_number=request.json[ID_NUMBER])
    db.session.add(employee)
    db.session.commit()
    employee_dict = get_single_worker(request.json[ID_NUMBER])
    return employee_dict


def main():
    """
    Create the db and tables(if the don't exist) and run the app
    """
    db.create_all()
    app.run()


if __name__ == '__main__':
    main()
