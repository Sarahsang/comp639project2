drop database leave_management_dBase;
create database if not exists leave_management_dBase;
use leave_management_dBase;

CREATE TABLE department (
	department_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);


CREATE TABLE position (
	position_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    position_name VARCHAR(20) NOT NULL
);

CREATE TABLE role (
	role_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(20) NOT NULL
);


CREATE TABLE employee (
	employee_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    employee_title VARCHAR(10) NOT NULL,
    employee_fname VARCHAR(20) NOT NULL,
    employee_lname VARCHAR(20) NOT NULL,
    employee_email VARCHAR(100) NOT NULL,
    employee_password VARCHAR(255) NOT NULL,
    employee_status TINYINT DEFAULT TRUE,
    date_joined DATE,
    position_id SMALLINT NOT NULL, 
    position_start_date DATE,
    department_id SMALLINT NOT NULL,
    supervisor_id SMALLINT NOT NULL, 
    approval_manager_id SMALLINT NOT NULL,
    CONSTRAINT employee_position_id_FK FOREIGN KEY (position_id) REFERENCES position (position_id),
    CONSTRAINT employee_department_id_FK FOREIGN KEY (department_id) REFERENCES department (department_id)
);

CREATE TABLE employee_role (
	employee_role_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    employee_id	 SMALLINT NOT NULL,
    role_id	 SMALLINT NOT NULL,
    CONSTRAINT employee_role_employee_id_FK FOREIGN KEY (employee_id) REFERENCES employee (employee_id),
    CONSTRAINT employee_role_role_id_FK FOREIGN KEY (role_id) REFERENCES role (role_id)
);

CREATE TABLE leave_type (
	leave_type_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    leave_type VARCHAR(30) NOT NULL,
    leave_discription VARCHAR(500)
);

CREATE TABLE request_status (
	status_approval_id SMALLINT PRIMARY KEY,
    status_approval_description VARCHAR(20)
);

CREATE TABLE leave_request (
	request_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    employee_id SMALLINT NOT NULL,
    leave_type_id SMALLINT NOT NULL,
    start_date DATE,
    end_date DATE,
    status_approval SMALLINT DEFAULT FALSE,
    approval_manager_id SMALLINT NOT NULL,
    comment VARCHAR(255),
    comment_withdrawn VARCHAR(255),
    comment_rejected VARCHAR(255),
    processed_by_payroll TINYINT DEFAULT FALSE,
    duration_days TINYINT,
    unpaid_duration_days TINYINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT leave_request_employee_id_FK FOREIGN KEY (employee_id) REFERENCES employee (employee_id),
    CONSTRAINT leave_request_leave_type_id_FK FOREIGN KEY (leave_type_id) REFERENCES leave_type (leave_type_id),
    CONSTRAINT leave_request_status_approval_FK FOREIGN KEY (status_approval) REFERENCES request_status (status_approval_id)
);

CREATE TABLE leave_balance (
	leave_balance_id SMALLINT AUTO_INCREMENT PRIMARY KEY, 
    employee_id SMALLINT NOT NULL,
    annual_leave_balance decimal(6,2), 
    sick_leave_balance decimal(6,2),
    sl_reset_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT leave_balance_employee_id_FK FOREIGN KEY (employee_id) REFERENCES employee (employee_id)
);
    
CREATE TABLE datetable (
date DATE,
year YEAR,
quarter CHAR(2),
month TINYINT,
wk_num TINYINT,
leave_cost_day TINYINT,
day_num TINYINT,
PRIMARY KEY (date)
);

CREATE TABLE holiday (
id SMALLINT AUTO_INCREMENT PRIMARY KEY,
date DATE,
holiday_desc VARCHAR(255),
eligibility TINYINT DEFAULT TRUE
);

CREATE TABLE payroll_fortnight (
payroll_fortnight_id VARCHAR(8) PRIMARY KEY,
start date,
end date,
status TINYINT DEFAULT FALSE,
process_date date,
by_admin SMALLINT,
CONSTRAINT payroll_fortnight_by_admin_FK FOREIGN KEY (by_admin) REFERENCES employee (employee_id)
);

CREATE TABLE leave_increment (
	leave_increment_id SMALLINT AUTO_INCREMENT PRIMARY KEY, 
    employee_id SMALLINT NOT NULL,
    leave_increment decimal(6,2), 
    payroll_fortnight_id VARCHAR(8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT leave_increment_employee_id_FK FOREIGN KEY (employee_id) REFERENCES employee (employee_id),
    CONSTRAINT leave_increment_payroll_fortnight_id_FK FOREIGN KEY (payroll_fortnight_id) REFERENCES payroll_fortnight (payroll_fortnight_id)
);