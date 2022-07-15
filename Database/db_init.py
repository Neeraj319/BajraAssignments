import os
import faker
import random
import dotenv
import sys
import sqlalchemy

*extras, command = sys.argv

dotenv.load_dotenv()


engine = sqlalchemy.create_engine(os.environ.get("DB_URL"))


def create_tables(connection):
    with open("schema.sql", "r") as f:
        schema = f.read()

        connection.execute(statement=schema)


def insert_manager(connection):

    for _ in range(5):
        query = f"""
        INSERT INTO "Manager" (name) values (%s);
        """
        connection.execute(query, (faker.name(),))


def insert_parent_department(connection):

    query = f"""
    INSERT INTO "ParentDepartment" (name) values ('General Management');
    """

    connection.execute(query)


def get_managers(connection):

    query = f"""
    SELECT * FROM "Manager";
    """

    return connection.execute(statement=query)


def insert_departments(connection):
    departments = ["Human Resources", "IT", "Marketing", "Sales"]

    for department, manager in zip(departments, get_managers(connection=connection)):
        query = f"""
        INSERT INTO "Department" (dept_name, parent_dept_id, manager_id) values (%s, %s, %s);
        """
        connection.execute(query, (department, 1, manager[0]))


def get_departments(connection):

    query = f"""
    SELECT * FROM "Department";
    """
    return connection.execute(query)


def insert_employees(connection):

    departments = list(get_departments(connection=connection))
    for _ in range(10):
        joined_date = faker.date_between(start_date="-5y", end_date="today")
        monthly_salary = random.randint(5000, 10000)
        query = f"""
        INSERT INTO "Employee" (first_name, last_name, join_date, monthly_salary, dept_id) values (%s, %s, %s, %s, %s);
        """
        connection.execute(
            query,
            (
                faker.first_name(),
                faker.last_name(),
                joined_date,
                monthly_salary,
                random.choice(departments)[0],
            ),
        )


def main():
    if command == "initialize":
        with engine.connect() as connection:

            create_tables(connection=connection)
            insert_manager(connection=connection)
            insert_parent_department(connection=connection)
            insert_departments(connection=connection)
            insert_employees(connection=connection)

        print("initialization complete")


if __name__ == "__main__":
    faker = faker.Faker()
    main()
