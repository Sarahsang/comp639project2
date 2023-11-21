INSERT INTO DEPARTMENT (department_id, department_name)
VALUES (1, 'School of Landscape Architecture'), (2, 'Department of Tourism, Sport and Society'), (3, 'Department of Wine, Food and Molecular Biosciences'), (4, 'Department of Pest Management and Conservation'),	(5, 'Department of Corporate Services')
;

INSERT INTO POSITION (position_id, position_name)
VALUES (1, 'Professor'), (2, 'Associate Professor'), (3, 'Lecturer'), (4, 'Tutor'), (5, 'Vice-Chancellor'), (6, 'Director')
;

INSERT INTO ROLE (role_id, role_name)
VALUES (1, 'administrator'), (2, 'approval manager')
;

INSERT INTO EMPLOYEE (employee_id, employee_title, employee_fname, employee_lname, employee_email,
employee_password, date_joined, position_id, position_start_date, department_id, supervisor_id, approval_manager_id)
VALUES (1, 'Miss', 'Sherlyn', 'Duan', 'sherlyn.duan@lincolnuni.ac.nz', 'password', '2004-05-08', 5, '2022-02-23', 5, 2, 2),
(2, 'Mr', 'Steven', 'Rawley', 'steven.rawley@lincolnuni.ac.nz', 'password', '1988-02-08', 6, '2019-01-09', 5, 1, 1)
;

INSERT INTO EMPLOYEE_ROLE (employee_id, role_id)
VALUES (1,1), (2,1)
;

INSERT INTO LEAVE_TYPE (leave_type_id, leave_type)
VALUES (1, 'Annual Leave'), (2, 'Sick Leave'), (3, 'Bereavement Leave'), (4, 'Public Holiday'), (5, 'Unpaid Leave')
;

INSERT INTO LEAVE_REQUEST (employee_id, leave_type_id, start_datetime, end_datetime, status_approval, approval_manager_id, reasons)
VALUES (1, 1, '2023-08-01', '2023-08-20', 0, 2, 'too busy'), (2, 2, '2023-04-28', '2023-04-28', 1, 1, 'covid')
;

INSERT INTO LEAVE_BALANCE (employee_id, annual_leave_balance, sick_leave_balance)
VALUES (1, 500, 40), (2, -10, 40)
;
