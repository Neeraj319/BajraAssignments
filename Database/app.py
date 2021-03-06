import db_init
import pandas as pd


def print_total_earnings(connection):
    """
    connection -> sql alchemy db connection object

    prints out the total earnings of employees grouped by departments
    with proper formatting
    """

    query = f"""
    SELECT d.dept_name as "department name", SUM (e.monthly_salary * 
    (EXTRACT(year FROM age(now():: DATE, e.join_date)) 
    * 12 + EXTRACT(month FROM age(now():: DATE, e.join_date))))
    AS "total salaries of employees" FROM
    "Department" d LEFT JOIN "Employee"
    e on e.dept_id = d.d_id
    GROUP BY d.dept_name; 
    """

    fetched_data = pd.io.sql.read_sql(query, connection)
    print(fetched_data)


def print_employees_belonging_to_sales(connection):
    """
    connection -> sql alchemy db connection object

    prints out all employees belonging to a department sales with service length more than 6 months
    """

    query = """
    SELECT e.* FROM "Employee" e 
    INNER JOIN "Department" d on d.dept_name = 'Sales'
    WHERE EXTRACT(year FROM age(now():: DATE, e.join_date)) 
    * 12 + EXTRACT(month FROM age(now():: DATE, 
    e.join_date)) > 6 and e.dept_id = 4;
    """

    fetched_data = pd.read_sql(query, connection)
    print(fetched_data)


def print_employees_with_department_name(connection):
    """
    connection -> sql alchemy db connection object

    prints out all employees with their department name and manager name
    """

    query = """
    SELECT e.first_name, e.last_name,d.dept_name, m."name" as 
    department_manager_name, 
    m.m_id as department_manager_id
    FROM "Employee" e LEFT JOIN "Department" d 
    on d.d_id = e.dept_id  
    LEFT JOIN "Manager" m on 
    d.manager_id = m.m_id;
    """

    fetched_data = pd.read_sql(query, connection)
    print(fetched_data)


def main():
    options = [
        "1) show total earnings of employees grouped by departments",
        "2) show all employees belonging to a department sales with service length more than 6 months",
        "3) list employees with their department name and manager",
    ]
    user_input = int(input("\n".join(options) + "\n"))
    with db_init.engine.connect() as db:
        while True:
            match user_input:
                case 1:
                    print_total_earnings(connection=db)
                case 2:
                    print_employees_belonging_to_sales(connection=db)
                case 3:
                    print_employees_with_department_name(connection=db)
                case _:
                    print("Invalid input")
            user_input = int(input("\n\n".join(options) + "\n"))


if __name__ == "__main__":
    main()
