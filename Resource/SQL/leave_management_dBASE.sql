drop database leave_management_dBase;
create database if not exists leave_management_dBase;
use leave_management_dBase;

CREATE TABLE DEPARTMENT (
	department_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);


CREATE TABLE POSITION (
	position_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    position_name VARCHAR(20) NOT NULL
);

CREATE TABLE ROLE (
	role_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(20) NOT NULL
);


CREATE TABLE EMPLOYEE (
	employee_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    employee_title VARCHAR(10) NOT NULL,
    employee_fname VARCHAR(20) NOT NULL,
    employee_lname VARCHAR(20) NOT NULL,
    employee_email VARCHAR(100) NOT NULL,
    employee_password VARCHAR(20) NOT NULL,
    date_joined DATE,
    position_id SMALLINT NOT NULL, 
    position_start_date DATE,
    department_id SMALLINT NOT NULL,
    supervisor_id SMALLINT NOT NULL, 
    approval_manager_id SMALLINT NOT NULL,
    CONSTRAINT EMPLOYEE_position_id_FK FOREIGN KEY (position_id) REFERENCES POSITION (position_id),
    CONSTRAINT EMPLOYEE_department_id_FK FOREIGN KEY (department_id) REFERENCES DEPARTMENT (department_id)
);

CREATE TABLE EMPLOYEE_ROLE (
	employee_role_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    employee_id	SMALLINT NOT NULL,
    role_id	SMALLINT NOT NULL,
    CONSTRAINT EMPLOYEE_ROLE_employee_id_FK FOREIGN KEY (employee_id) REFERENCES EMPLOYEE (employee_id),
    CONSTRAINT EMPLOYEE_ROLE_role_id_FK FOREIGN KEY (role_id) REFERENCES ROLE (role_id)
);

CREATE TABLE LEAVE_TYPE (
	leave_type_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    leave_type VARCHAR(20) NOT NULL
);

CREATE TABLE LEAVE_REQUEST (
	request_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    employee_id SMALLINT NOT NULL,
    leave_type_id SMALLINT NOT NULL,
    start_datetime DATETIME,
    end_datetime DATETIME,
    status_approval TINYINT DEFAULT FALSE,
    approval_manager_id SMALLINT NOT NULL,
    reasons VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT LEAVE_REQUEST_employee_id_FK FOREIGN KEY (employee_id) REFERENCES EMPLOYEE (employee_id),
    CONSTRAINT LEAVE_REQUEST_leave_type_id_FK FOREIGN KEY (leave_type_id) REFERENCES LEAVE_TYPE (leave_type_id)
);

CREATE TABLE LEAVE_BALANCE (
	leave_balance_id SMALLINT AUTO_INCREMENT PRIMARY KEY, 
    employee_id SMALLINT NOT NULL,
    annual_leave_balance INT, 
    sick_leave_balance INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT LEAVE_BALANCE_employee_id_FK FOREIGN KEY (employee_id) REFERENCES EMPLOYEE (employee_id)
);
    
    