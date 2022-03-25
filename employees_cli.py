import argparse
import json
import sys
import requests
from employees_app import FIRST_NAME, LAST_NAME, ID_NUMBER, BASE_URL, EMPLOYEES, EMPLOYEES_ROUTE


def post_employee(first_name, last_name, id_number):
    """
    Post a new employee request
    :param first_name: The employee first name
    :type first_name: Str
    :param last_name: The employee last name
    :type last_name: Str
    :param id_number: The employee identification number
    :type id_number: Int
    :return: response_json
    :rtype: Dict
    """
    url = BASE_URL + EMPLOYEES_ROUTE
    post_dict = {FIRST_NAME: first_name,
                 LAST_NAME: last_name,
                 ID_NUMBER: id_number}
    response = requests.post(url, json=post_dict)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        return response_json


def get_all_employees():
    """
    Send a get request to get all employees data
    :return: employees_data
    :rtype: Dict
    """
    url = BASE_URL + EMPLOYEES_ROUTE
    response = requests.get(url)
    if response.status_code == 200:
        employees_data = json.loads(response.text)
        return employees_data


def get_employee(id_number):
    """
    Send a get request to retreive a specific employee info by id
    :param id_number: The wanted employee id
    :type id_number: Int
    :return: employee_data
    :rtype: Dict
    """
    url = BASE_URL + EMPLOYEES_ROUTE + f'/{id_number}'
    response = requests.get(url)
    if response.status_code == 200:
        employee_data = json.loads(response.text)
        return employee_data


def valid_id(id_number):
    """
    Verify that the id argument is a valid int string and parse it as an int
    :param id_number: The id number argument
    :type id_number: Str
    :return: id_number
    :rtype: Int
    """
    try:
        id_number = int(id_number)
        return id_number
    except ValueError:
        msg = f'Not a valid id number: {id_number}'
        raise argparse.ArgumentTypeError(msg)


def parse_arguments():
    """
    Parse the arguments from the user. If no arguments were given print usage.
    :return: args
    :rtype: argparse.ArgumentParser()
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--get-employees', help="Print a list of all employees", action='store_true')
    parser.add_argument('-get-employee', help="Print employee info by employee ID")
    parser.add_argument('--add-employee', help="Add employee (must specify -employee-name and -employee-id)",
                        action='store_true')
    parser.add_argument('-employee-name', help="The new employee first and last name", nargs=2)
    parser.add_argument('-employee-id', help="The new employee id number", type=valid_id)
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()
    if args.employee_name:
        args.first_name = args.employee_name[0]
        args.last_name = args.employee_name[1]
    return args


def print_all_employees_info():
    """
    call the get function and print the employees info
    """
    employees = get_all_employees()[EMPLOYEES]
    print('Current employees:')
    for employee in employees:
        print(f'{employee[FIRST_NAME]} {employee[LAST_NAME]}, {ID_NUMBER}: {employee[ID_NUMBER]}')


def print_specific_employee_info(id_number):
    """
    Call the get function for a specific employee id and print out the employee details
    :param id_number: The wanted employee id number
    :type id_number: Int
    """
    employee_dict = get_employee(id_number)
    if employee_dict:
        print(f'{employee_dict[FIRST_NAME]} {employee_dict[LAST_NAME]}, {ID_NUMBER}: {employee_dict[ID_NUMBER]}')
    else:
        print(f'Unable to find an employee with id number {id_number}')


def add_new_employee(first_name, last_name, id_number):
    """
    Call the post request to add a new emploee and print out the result of the request
    :param first_name: Employee first name
    :type first_name: Str
    :param last_name: Employee last name
    :type last_name: Str
    :param id_number: Employee id number
    :type id_number: Int
    """
    employee_dict = post_employee(first_name, last_name, id_number)
    if employee_dict:
        print('New employee added:')
        print(f'{employee_dict[FIRST_NAME]} {employee_dict[LAST_NAME]}, {ID_NUMBER}: {employee_dict[ID_NUMBER]}')
    else:
        print('Unable to add new employee to database')


def main():
    args = parse_arguments()
    if args.get_employees:
        print_all_employees_info()
    elif args.get_employee:
        print_specific_employee_info(args.get_employee)
    elif args.add_employee:
        add_new_employee(args.first_name, args.last_name, args.employee_id)


if __name__ == '__main__':
    main()
