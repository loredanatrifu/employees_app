create table "departments" (
	id serial not null,
	department_name varchar (20),
	constraint dep_pkey primary key (id)
);

insert into departments(department_name) values
('HR'),
('Accounting'),
('IT'),
('Management');

create table "employees" (
	id serial not null,
	first_name varchar (50) not null,
	last_name varchar (50) not null,
	age int not null,
	job varchar (20) not null,
	salary_euro int not null,
	bonus float,
	total_salary float,
	departments_id int not null,
	foreign key (departments_id) references departments(id)
);

insert into employees(first_name,last_name,age,job,salary_euro,departments_id) values
('Loredana', 'Trifu', 34, 'Developer', 1500, 3),
('Ion', 'Popescu', 50, 'Economist', 1000, 2),
('Elena', 'Sora', 27, 'Recruiter', 1700, 1),
('Razvan', 'Moga', 48, 'Project Manager', 1200, 4);