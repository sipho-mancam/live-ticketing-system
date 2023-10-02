
select * from live_ticketing_db.department;
select * from live_ticketing_db.employees;
select * from live_ticketing_db.tasks;
select * from live_ticketing_db.tickets;

delete from live_ticketing_db.department where dept_id > 0;
delete from live_ticketing_db.employees where employees_id > 0;

drop table live_ticketing_db.department;
truncate table live_ticketing_db.employees;
create table live_ticketing_db.department (dept_id int primary key auto_increment, dept_name VARCHAR(255) Not NULL, manager int not null); 

INSERT INTO live_ticketing_db.department (dept_name, manager) VALUES
('Finance', 1),
('Human Resources', 2),
('Marketing', 3),
('Operations', 4),
('IT', 5),
('Research and Development', 6),
('Customer Service', 7),
('Sales', 8);


INSERT INTO live_ticketing_db.employees (name, email, department, position)
VALUES
('Manager1', 'manager1@example.com', 1, 'Manager'),
('Manager2', 'manager2@example.com', 2, 'Manager'),
('Manager3', 'manager3@example.com', 3, 'Manager'),
('Manager4', 'manager4@example.com', 4, 'Manager'),
('Manager5', 'manager5@example.com', 5, 'Manager'),
('Manager6', 'manager6@example.com', 6, 'Manager'),
('Manager7', 'manager7@example.com', 7, 'Manager'),
('Manager8', 'manager8@example.com', 8, 'Manager'),
('Employee1', 'employee1@example.com', 1, 'Employee'),
('Employee2', 'employee2@example.com', 2, 'Employee'),
('Employee3', 'employee3@example.com', 3, 'Employee'),
('Employee4', 'employee4@example.com', 4, 'Employee');


INSERT INTO tickets (assigned_to, status, start_date, close_date, department, description)
VALUES
(1, 0, '2023-10-02 10:00:00', '2023-10-02 12:00:00', 1, 'Issue with financial report'),
(2, 1, '2023-10-03 14:00:00', '2023-10-03 16:30:00', 2, 'Employee onboarding assistance needed'),
(3, 2, '2023-10-04 09:30:00', '2023-10-04 11:45:00', 3, 'Marketing campaign analysis'),
(4, 0, '2023-10-05 13:00:00', '2023-10-05 15:15:00', 4, 'Network connectivity issue'),
(5, 1, '2023-10-06 11:30:00', '2023-10-06 14:00:00', 5, 'Software installation request'),
(6, 2, '2023-10-07 10:45:00', '2023-10-07 12:30:00', 6, 'Research data analysis assistance'),
(7, 0, '2023-10-08 09:00:00', '2023-10-08 11:00:00', 7, 'Customer feedback analysis'),
(8, 1, '2023-10-09 13:45:00', '2023-10-09 15:45:00', 8, 'Sales target review');


INSERT INTO live_ticketing_db.tasks (description, ticket_id, status, assigned_to, assigned_date)
VALUES
('Task 1 for ticket 1', 1, 0, 1, '2023-10-02 10:30:00'),
('Task 2 for ticket 1', 1, 1, 2, '2023-10-02 11:00:00'),
('Task 3 for ticket 1', 1, 2, 3, '2023-10-02 11:30:00'),
('Task 4 for ticket 1', 1, 0, 4, '2023-10-02 12:00:00'),
('Task 5 for ticket 1', 1, 1, 5, '2023-10-02 12:30:00');

INSERT INTO tasks (description, ticket_id, status, assigned_to, assigned_date)
VALUES
('Task 1 for ticket 1', 2, 0, 1, '2023-10-02 10:30:00'),
('Task 2 for ticket 1', 2, 1, 2, '2023-10-02 11:00:00'),
('Task 3 for ticket 1', 2, 2, 3, '2023-10-02 11:30:00'),
('Task 4 for ticket 1', 2, 0, 4, '2023-10-02 12:00:00'),
('Task 5 for ticket 1', 2, 1, 5, '2023-10-02 12:30:00');

CALL populate_tasks_for_tickets();