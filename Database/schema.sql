CREATE TABLE IF NOT EXISTS "Manager"  (
	m_id SERIAL NOT NULL PRIMARY KEY, 
	name VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS "ParentDepartment"(
	pd_id SERIAL NOT NULL PRIMARY KEY, 
	name VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS "Department"  (
	d_id SERIAL NOT NULL PRIMARY KEY, 
	dept_name VARCHAR(50) NOT NULL,
	dept_code VARCHAR(50),
	parent_dept_id INT, 
	manager_id INT,
	description VARCHAR(100),
	active BOOLEAN,
	
	FOREIGN KEY(manager_id) REFERENCES "Manager"(m_id) 
	  ON DELETE SET NULL,	
	FOREIGN KEY(parent_dept_id) REFERENCES "ParentDepartment"(pd_id) 
	  ON DELETE CASCADE

);


CREATE TABLE IF NOT EXISTS "Employee" (
	emp_id SERIAL NOT NULL PRIMARY KEY,
	first_name VARCHAR(20) NOT NULL,
	middle_name VARCHAR(20),
	last_name VARCHAR(20) NOT NULL,
	join_date DATE,
	monthly_salary FLOAT,
	dept_id INT,
	
	FOREIGN KEY(dept_id) REFERENCES "Department"(d_id) 
	  ON DELETE CASCADE
);
