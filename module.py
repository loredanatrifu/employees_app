import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="postgres",
    password="postgres")

with conn:
    query = """
    select
        e.id,  concat(e.first_name, ' ', e.last_name) as "Name", e.age,
        e.job, e.salary_euro, e.bonus, e.total_salary
        from employees e;
"""
    c = conn.cursor()
    c.execute(query)
    records = c.fetchall()

with conn:
    query = """
    select
        e.id,  concat(e.first_name, ' ', e.last_name) as "Name", e.age,
        e.job, e.salary_euro, e.bonus, e.total_salary,
        d.id, d.department_name
        from employees e
        join "departments" d on e.departments_id = d.id;
"""
    c = conn.cursor()
    c.execute(query)
    departments = c.fetchall()
    # print(departments)


def show_employees():
    """ Shows the employees data
    """

    for r in records:
        print("Employee Id: ", r[0])
        print("Employee Name: ", r[1])
        print("Employee Age: ", r[2])
        print("Employee Job: ", r[3])
        print("Employee Salary: ", r[4])


def display_departments():
    """ Display the company departments
    """

    for d in departments:
        print("Company departments: ", d[8])


def department_HR():
    """ Display the employers in HR departments
        """

    with conn:
        query_one = """
        select
            concat(e.first_name, ' ', e.last_name) as "Name", e.job, 
            d.id, d.department_name
            from employees e
            join "departments" d on e.departments_id = d.id
            where e.departments_id = 1;
    """
        c = conn.cursor()
        c.execute(query_one)
        hr = c.fetchall()

        for e in hr:
            print("The employees in HR department are: ", e[0], '-', e[1])


def department_AC():
    """ Display the employers in accounting departments
        """

    with conn:
        query_two = """
        select
            concat(e.first_name, ' ', e.last_name) as "Name", e.job, 
            d.id, d.department_name
            from employees e
            join "departments" d on e.departments_id = d.id
            where e.departments_id = 2;
    """
        c = conn.cursor()
        c.execute(query_two)
        ac = c.fetchall()

        for e in ac:
            print("The employees in HR department are: ", e[0], '-', e[1])


def department_IT():
    """ Display the employers in IT departments
        """

    with conn:
        query_three = """
        select
            concat(e.first_name, ' ', e.last_name) as "Name", e.job, 
            d.id, d.department_name
            from employees e
            join "departments" d on e.departments_id = d.id
            where e.departments_id = 3;
    """
        c = conn.cursor()
        c.execute(query_three)
        it = c.fetchall()

        for e in it:
            print("The employees in HR department are: ", e[0], '-', e[1])


def department_management():
    """ Display the employers in management departments
        """

    with conn:
        query_two = """
        select
            concat(e.first_name, ' ', e.last_name) as "Name", e.job, 
            d.id, d.department_name
            from employees e
            join "departments" d on e.departments_id = d.id
            where e.departments_id = 4;
    """
        c = conn.cursor()
        c.execute(query_two)
        mg = c.fetchall()

        for e in mg:
            print("The employees in HR department are: ", e[0], '-', e[1])


def apply_bonus():
    id = int(input("Enter Employee Id : "))
    salary = int(input('Enter the employee salary: '))

    if salary < 1500:
        bonus = 0.1 * salary
    if 1500 > salary < 2000:
        bonus = 0.2 * salary
    else:
        bonus = 0.3 * salary

    data = (salary, id)
    sql = 'insert into employees(bonus) values(%s) where id=%s'
    c = conn.cursor()
    c.execute(sql, data)
    print('Employee bonus is: ', bonus)


def user_menu():
    print("Press")
    print("1 to Add Employee")
    print("2 to Remove Employee ")
    print("3 to Apply Bonus")
    print("4 to Display Employees")

    user_input = int(input("Enter your Choice "))
    if user_input == 1:
        add_employee()

    elif user_input == 2:
        remove_employee()

    elif user_input == 3:
        apply_bonus()

    elif user_input == 4:
        show_employees()

    else:
        print("Invalid Choice")
        user_menu()


def add_employee():
    id = int(input("Enter Employee Id : "))
    first_name = input("Enter Employee First Name : ")
    last_name = input("Enter Employee Last Name : ")
    age = int(input("Enter Employee Age : "))
    job = input("Enter Employee Job : ")
    salary_euro = input("Enter Employee Salary : ")
    bonus = input("Enter Employee Bonus : ")
    departments_id = int(input("Enter Employee Department ID : "))
    total_salary = bonus + salary_euro
    data = (id, first_name, last_name, age, job, salary_euro, bonus, total_salary, departments_id)

    sql = 'insert into employees values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    c = conn.cursor()
    c.execute(sql, data)
    print("Employee Added Successfully ")
    user_menu()


def remove_employee():
    id = int(input("Enter Employee Id : "))
    data = (id,)
    sql = 'delete from employees where id=%s'
    c = conn.cursor()
    c.execute(sql, data)
    print("Employee removed")
    user_menu()


def search_employee():
    first_name = input("Enter employee first name: ")
    last_name = input("Enter employee last name: ")
    with conn:
        c = conn.cursor()
        query_five = """
            select e.id, e.first_name, e.last_name, 
            d.department_name, d.id
            from employees e
            join "departments" d on e.departments_id = d.id
            where s.first_name = %s and s.last_name = %s;
        """

        c.execute(query_five, (first_name, last_name))
        record = c.fetchone()
        print(record)
        if first_name or last_name in record:
            department_name = record[1]
            print(f'Employee {first_name} {last_name} is in department {department_name}.')


def text_invoice():
    with conn:
        query = """
            select 
                e.first_name as "First Name", e.last_name as "Last Name", e.age, e.job, e.salary_euro,
                d.department_name
                from employees e
                join "departments" d on e.departments_id = d.id;
        """
        c = conn.cursor()
        c.execute(query)

        records = c.fetchall()

        with open('employee_invoice.txt', 'w') as file:
            print(f"{'First Name':20} {'Last Name':20} {'Age':5} {'Job':10} {'Salary':10} {'Department name':15}", file=file)
            print('-' * 47, file=file)
            for r in records:
                print(f'{r[0]:20} {r[1]:20} {r[2]:>5} {r[3]:>10} {r[4]:>10} {r[5]:>15}', file=file)

        c.close()

    conn.close()

text_invoice()