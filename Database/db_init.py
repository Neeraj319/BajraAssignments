import psycopg2
import os
import faker
import random
import dotenv
import sys

*extras, command = sys.argv

dotenv.load_dotenv()
faker = faker.Faker()


class DBConnector:
    """
    context manager for database connection
    """

    def __init__(self) -> None:
        self.connection = psycopg2.connect(os.environ.get("DB_URL"))
        self.curr = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.curr.close()
        self.connection.close()

    def close(self):
        self.curr.close()
        self.connection.close()


def create_tables():
    with open("schema.sql", "r") as f:
        schema = f.read()
        with DBConnector() as db:
            db.curr.execute(schema)
            db.connection.commit()


def insert_manager():
    with DBConnector() as db:
        for _ in range(5):
            query = f"""
            INSERT INTO "Manager" (name) values ('{faker.name()}');
            """
            db.curr.execute(query=query)
            db.connection.commit()


def insert_parent_department():
    with DBConnector() as db:
        query = f"""
        INSERT INTO "ParentDepartment" (name) values ('General Management');
        """
        db.curr.execute(query=query)
        db.connection.commit()


def get_managers():
    with DBConnector() as db:
        query = f"""
        SELECT * FROM "Manager";
        """
        db.curr.execute(query=query)
        return db.curr.fetchall()


def insert_departments():
    departments = ["Human Resources", "IT", "Marketing", "Sales"]
    with DBConnector() as db:
        for department, manager in zip(departments, get_managers()):
            query = f"""
            INSERT INTO "Department" (dept_name, parent_dept_id, manager_id) values ('{department}', 1, {manager[0]});
            """
            db.curr.execute(query=query)
            db.connection.commit()


def get_departments():
    with DBConnector() as db:
        query = f"""
        SELECT * FROM "Department";
        """
        db.curr.execute(query=query)
        return db.curr.fetchall()


def insert_employees():
    with DBConnector() as db:
        departments = get_departments()
        for _ in range(10):
            joined_date = faker.date_between(start_date="-5y", end_date="today")
            monthly_salary = random.randint(5000, 10000)
            query = f"""
            INSERT INTO "Employee" (first_name, last_name, join_date, monthly_salary, dept_id) values (%s, %s, %s, %s, %s);
            """
            db.curr.execute(
                query,
                (
                    faker.first_name(),
                    faker.last_name(),
                    joined_date,
                    monthly_salary,
                    random.choice(departments)[0],
                ),
            )
            db.connection.commit()


def main():
    if command == "initialize":
        create_tables()
        insert_manager()
        insert_parent_department()
        insert_departments()
        insert_employees()

        print("initialization complete")


if __name__ == "__main__":
    main()
