import os
import faker
import random
import dotenv
import sys
import sqlalchemy

*extras, command = sys.argv

dotenv.load_dotenv()


engine = sqlalchemy.create_engine(os.environ.get("DB_URL"))


def create_tables():
    with open("schema.sql", "r") as f:
        schema = f.read()
        with engine.connect() as connection:
            connection.execute(statement=schema)


def insert_manager():
    with engine.connect() as connection:
        for _ in range(5):
            query = f"""
            INSERT INTO "Manager" (name) values (%s);
            """
            connection.execute(query, (faker.name(),))


def insert_parent_department():

    query = f"""
    INSERT INTO "ParentDepartment" (name) values ('General Management');
    """
    with engine.connect() as connection:
        connection.execute(query)


def get_managers():

    query = f"""
    SELECT * FROM "Manager";
    """
    with engine.connect() as connection:
        return connection.execute(statement=query)


def insert_departments():
    departments = ["Human Resources", "IT", "Marketing", "Sales"]
    with engine.connect() as connection:
        for department, manager in zip(departments, get_managers()):
            query = f"""
            INSERT INTO "Department" (dept_name, parent_dept_id, manager_id) values (%s, %s, %s);
            """
            connection.execute(query, (department, 1, manager[0]))


def get_departments():

    query = f"""
    SELECT * FROM "Department";
    """
    with engine.connect() as connection:
        return connection.execute(query)


def insert_employees():

    departments = list(get_departments())
    with engine.connect() as connection:
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

        create_tables()
        insert_manager()
        insert_parent_department()
        insert_departments()
        insert_employees()

        print("initialization complete")


if __name__ == "__main__":
    faker = faker.Faker()
    main()
