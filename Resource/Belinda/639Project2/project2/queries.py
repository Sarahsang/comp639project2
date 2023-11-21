 # login employee role query  
def login():
    query= ("""
            SELECT e.employee_id, r.role_name AS role_name
            FROM employee e
            JOIN employee_role er ON e.employee_id = er.employee_id
            JOIN role r ON er.role_id = r.role_id
            WHERE e.employee_email = %s and e.employee_password = %s
        """)
    return query
