 # login employee role query  
def login():
    query= ("""
            select e.employee_id, r.role_id as role_id, e.employee_password, employee_fname, employee_lname
            from employee e
            join employee_role er on e.employee_id = er.employee_id
            join role r on er.role_id = r.role_id
            where e.employee_email = %s
        """)
    return query

def userdetail():
    query= (
        ''' select e.employee_id, e.employee_title, e.employee_fname, e.employee_lname, e.employee_email, e.date_joined, p.position_name, e.position_start_date, d.department_name,
        e.supervisor_id, s.employee_fname as supervisor_fname, s.employee_lname as supervisor_lname, s.employee_email as supervisor_email, e.approval_manager_id, am.employee_fname as manager_fname,
        am.employee_lname as manager_lname, am.employee_email as manager_email
            from employee as e
            left join employee_role as er on e.employee_id=er.employee_id 
            left join position as p on e.position_id=p.position_id
            left join department as d on e.department_id=d.department_id
            left join employee as s on e.supervisor_id=s.employee_id
            left join employee as am on e.approval_manager_id=am.employee_id
            where e.employee_id = %s
            ; '''
    )
    return query

def user():
    query=('select * from employee where employee_id =%s;')
    return query

def leavebalance():
    query=('''select leave_balance.employee_id, employee.employee_fname as firstname, employee.employee_lname as lastname,
            leave_balance.annual_leave_balance as annuallb,  leave_balance.sick_leave_balance as sicklb
            from leave_balance left join employee on leave_balance.employee_id=employee.employee_id where employee.employee_id =%s
            ;''')
    return query

def annualleavebalance_unapproved():
    query=('''select employee_id,  sum(duration_days) from leave_request where employee_id=%s and status_approval=0 and leave_type_id=1;''')
    return query

def annualleavebalance_unpaid():
    query=('''select employee_id,  sum(duration_days) from leave_request where employee_id=%s and status_approval=1 and processed_by_payroll=0 and leave_type_id=1;''')
    return query

def sickleavebalance_unapproved():
    query=('''select employee_id,  sum(duration_days) from leave_request where employee_id=%s and status_approval=0 and leave_type_id=2;''')
    return query

def sickleavebalance_unpaid():
    query=('''select employee_id,  sum(duration_days) from leave_request where employee_id=%s and status_approval=1 and processed_by_payroll=0 and leave_type_id=2;''')
    return query


def leavebalance_all():
    query=('''select lb.employee_id, lb.annual_leave_balance, e.date_joined, lb.sick_leave_balance
            from leave_balance as lb
            left join employee as e on lb.employee_id=e.employee_id
            where e.employee_status=1
            ;'''
           )
    return query

def update_leave():
    query=('''update leave_balance
            set annual_leave_balance = %s
            where employee_id = %s
            ;'''
           )
    return query


def payroll_day():
    query=('''select max(pf.end) as payroll_day
              from  leave_increment li
              join payroll_fortnight pf on li.payroll_fortnight_id = pf.payroll_fortnight_id
              join leave_request lr on lr.employee_id = li.employee_id
              where lr.employee_id=%s and pf.status=1;'''
           )
    return query

def projected_leave_cost():
    query=('''select sum(leave_cost_day) from datetable
              where date >= %s and date <= %s;'''
           )
    return query

def annualleave_unpaid_end_day():
    query=('''select employee_id,  end_date from leave_request where employee_id=%s and status_approval=1 and processed_by_payroll=0 and leave_type_id=1;''')
    
    return query

def annualleave_unpaid_start_day():
    query=('''select employee_id,  start_date from leave_request where employee_id=%s and status_approval=1 and processed_by_payroll=0 and leave_type_id=1;''')
    
    return query

def annualleave_unapproved_end_day():
    query=('''select employee_id,  end_date from leave_request where employee_id=%s and status_approval=0 and leave_type_id=1;''')
    return query

def annualleave_unapproved_start_day():
    query=('''select employee_id,  start_date from leave_request where employee_id=%s and status_approval=0 and leave_type_id=1;''')
    return query


def leave_types():
    query=('''select * from leave_type;'''
           )
    return query

def leave_requests():
    query= ( '''select e.employee_id,e.employee_fname, e.employee_lname,lr.leave_type_id,lt.leave_type,
              date_format(lr.start_date,'%d %b %Y'),date_format(lr.end_date,'%d %b %Y'), 
              lr.approval_manager_id,am.employee_fname as manager_fname, am.employee_lname as manager_lname, 
              lr.comment, rs.status_approval_description,lr.duration_days,
              date_format(lr.created_at, '%d %b %Y') as 'date requested', lr.request_id, lr.start_date, lr.end_date
              from leave_request lr
              left join employee e on lr.employee_id = e.employee_id
              left join leave_type lt on lr.leave_type_id = lt.leave_type_id
              left join request_status rs on lr.status_approval = rs.status_approval_id
              left join employee as am on lr.approval_manager_id=am.employee_id
              where e.employee_id = %s
              order by lr.start_date desc;'''
           )
    return query

def leave_requests_status():
    query= ( '''select e.employee_id,e.employee_fname, e.employee_lname,lr.leave_type_id, lt.leave_type,
              date_format(lr.start_date,'%d %b %Y'),date_format(lr.end_date,'%d %b %Y'), 
              lr.approval_manager_id,am.employee_fname as manager_fname, am.employee_lname as manager_lname, 
              lr.comment, rs.status_approval_description,lr.duration_days, 
              date_format(lr.created_at, '%d %b %Y') as 'date requested', lr.request_id, lr.start_date, lr.end_date
              from leave_request lr
              left join employee e on lr.employee_id = e.employee_id
              left join leave_type lt on lr.leave_type_id = lt.leave_type_id
              left join request_status rs on lr.status_approval = rs.status_approval_id
              left join employee as am on lr.approval_manager_id=am.employee_id
              where e.employee_id = %s and rs.status_approval_description=%s
              order by lr.start_date desc;'''
           )
    return query


def payroll_fortnight_past():
    query= ( '''
            select payroll_fortnight_id, start, end, status
            from payroll_fortnight
            where end<=curdate()
            order by start desc
            ;''')
    return query

def payroll_fortnight_future():
    query= ( '''
            select payroll_fortnight_id, start, end, status
            from payroll_fortnight
            where start>=curdate()
            order by start desc
;
            ;''')
    return query

def payroll_fortnight_current():
    query= ( '''
            select payroll_fortnight_id, start, end, status
            from payroll_fortnight
            where start<=curdate() and end>=curdate()
            order by start desc
            ;''')
    return query
def calendarholidays():
    query= ( '''
        select date, holiday_desc from holiday where eligibility=1;''')
    return query

def approvedleavec():
    query= ( '''
        select lr.employee_id, lr.leave_type_id, lt.leave_type, lr.start_date, lr.end_date, lr.duration_days 
        from leave_request as lr left join leave_type as lt 
        on lt.leave_type_id= lr.leave_type_id where (status_approval=1 or status_approval=2) and employee_id=%s ;''')
    return query

def pendingleavec():
    query= ( '''
        select lr.employee_id, lr.leave_type_id, lt.leave_type, lr.start_date, lr.end_date, lr.duration_days 
        from leave_request as lr left join leave_type as lt 
        on lt.leave_type_id= lr.leave_type_id where status_approval=0 and employee_id=%s ;''')
    return query

def allrequests():
    query= ( '''
        select lr.employee_id, lr.leave_type_id, lt.leave_type, lr.start_date, lr.end_date, lr.duration_days 
        from leave_request as lr left join leave_type as lt 
        on lt.leave_type_id= lr.leave_type_id where employee_id=%s ;''')
    return query

def allrequests_nodraft():
    query= ( '''
        select lr.employee_id, lr.leave_type_id, lt.leave_type, lr.start_date, lr.end_date, lr.duration_days 
        from leave_request as lr left join leave_type as lt 
        on lt.leave_type_id= lr.leave_type_id where employee_id=%s and lr.status_approval<>3 ;''')
    return query

def leavedays():
    query= ('''select sum(leave_cost_day) as leavedays from datetable 
        where date>= %s and date <=%s;''')
    return query


def withdrawleave():
    query= ('''update leave_request 
        set status_approval=-1
        where request_id=%s
        ;''')
    return query

def draftleave():
    query= ('''update leave_request 
        set status_approval=3
        where request_id=%s
        ;''')
    return query
    
def editleave_select():
    query= ('''select e.employee_id,e.employee_fname, e.employee_lname,lr.leave_type_id,lt.leave_type,
              date_format(lr.start_date,'%d %b %Y'),date_format(lr.end_date,'%d %b %Y'), 
              lr.approval_manager_id,am.employee_fname as manager_fname, am.employee_lname as manager_lname, 
              lr.comment, rs.status_approval_description,lr.duration_days,
              date_format(lr.created_at, '%d %b %Y') as 'date requested', lr.request_id, lr.start_date, lr.end_date
              from leave_request lr
              left join employee e on lr.employee_id = e.employee_id
              left join leave_type lt on lr.leave_type_id = lt.leave_type_id
              left join request_status rs on lr.status_approval = rs.status_approval_id
              left join employee as am on lr.approval_manager_id=am.employee_id
              where lr.request_id = %s
              ;''')
    return query

def leavesubmit():
    query= ('''insert into leave_request (employee_id, leave_type_id, start_date, end_date, status_approval, 
            approval_manager_id, comment, 
            processed_by_payroll, duration_days,unpaid_duration_days) 
            values (%s, %s, %s, %s, 0, %s, %s, 0, %s, %s)
        ;''')
    return query

def leaveupdate():
    query= ('''update leave_request set leave_type_id = %s, start_date = %s, end_date = %s, status_approval = 0, comment = %s, duration_days = %s , unpaid_duration_days=%s
            where request_id = %s;''')
    return query

def getleavetype():
    query= ('''select leave_type_id from leave_type where leave_type= %s
        ;''')
    return query

def getmanagerid():
    query= ('''select approval_manager_id from employee where employee_id=%s
        ;''')
    return query

def requestsdate_nodraft():
    query= ( '''
        select start_date, end_date from leave_request where employee_id=%s and status_approval<>3 ;''')
    return query


def allemployee_orgchart():
    query= ('''select employee_id, supervisor_id, approval_manager_id, employee_title, employee_fname, employee_lname, employee_email, department_id, position_name
        from employee
        join position on employee.position_id=position.position_id;''')
    return query

def dateforcalendar():
    query= ('''select datetable.date, day_num, eligibility as holiday
        from datetable
        left join holiday on datetable.date=holiday.date
        where datetable.date>='2023-01-01';''')
    return query

def dept_emp_leaverequests():
    query= ('''select e.department_id, lr.employee_id, lt.leave_type, lr.start_date, lr.end_date
        from leave_request as lr
        left join request_status as rs on lr.leave_type_id=rs.status_approval_id
        left join employee as e on lr.employee_id=e.employee_id
        left join leave_type as lt on lr.leave_type_id=lt.leave_type_id
        where lr.status_approval>=0 and lr.status_approval<=2 and e.department_id IN (select department_id from employee where employee_id = %s )
        order by e.department_id, lr.employee_id, lr.start_date;''')
    return query

def emp_leaverequests():
    query= ('''select e.department_id, lr.employee_id, lt.leave_type, lr.start_date, lr.end_date
        from leave_request as lr
        left join request_status as rs on lr.leave_type_id=rs.status_approval_id
        left join employee as e on lr.employee_id=e.employee_id
        left join leave_type as lt on lr.leave_type_id=lt.leave_type_id
        where lr.status_approval>=0 and lr.status_approval<=2 and lr.employee_id = %s
        order by e.department_id, lr.employee_id, lr.start_date;''')
    return query

def payrollweeks():
    query= ('''select pf.payroll_fortnight_id, pf.start, pf.end, pf.status, pf.process_date, e.employee_fname, e.employee_lname
        from payroll_fortnight as pf
        left join employee as e on pf.by_admin=e.employee_id
        where pf.start>'2023-01-01' and pf.end < date_add(curdate(), interval 28 day);''')
    return query

def leave_increment():
    query = ('''select employee_id, leave_increment, payroll_fortnight_id
        from leave_increment
        where payroll_fortnight_id= %s ;''')
    return query

def updateannualleavebalance():
    query = ('''update leave_balance 
        set annual_leave_balance = annual_leave_balance + %s
        where employee_id = %s;''')
    return query

def updateleaverequestunpaidduration():
    query = ('''update leave_request 
        set unpaid_duration_days = unpaid_duration_days + %s
        where request_id = %s;''')
    return query

def updatesickleavebalance():
    query = ('''update leave_balance 
        set sick_leave_balance = sick_leave_balance + %s
        where employee_id = %s;''')
    return query

def updatefortnight_toprocessed():
    query = ('''update payroll_fortnight 
        set status = %s, by_admin = %s, process_date = curdate()
        where payroll_fortnight_id = %s;''')
    return query

def countpendingapproval():
    query = ('''select employee_id, count(request_id)
        from leave_request
        where status_approval = 1 and processed_by_payroll = 0 and end_date < curdate()
        GROUP BY employee_id;
        ''')
    return query

def getapprovednotpaidrequests():
    query = ('''select * 
        from leave_request
        where status_approval >=1 and status_approval <=2 and processed_by_payroll != 1 and start_date < curdate();''')
    return query

def updateapprovedrequesttopaid():
    query = ('''update leave_request 
        set status_approval = 2, processed_by_payroll = %s
        where request_id = %s;''')
    return query

def allleavetypes():
    query = ('''select * from leave_type;''')
    return query

def roles():
    query=('''select e.employee_id, employee_title as Title, 
    employee_fname as First, employee_lname as last, 
    r.role_id, role_name as role
    from employee as e
    join employee_role as er on er.employee_id=e.employee_id
    join role as r on r.role_id=er.role_id
    ;'''
           )
    return query

def roleTypes():
    query=('''select * from role;''')
    return query


def update_role():
    query=('''update employee_role
    SET role_id = %s
    WHERE employee_id = %s;''')
    return query

def check_holiday():
    query = ('''select id, date_format(date,'%d-%m-%Y'), holiday_desc, eligibility
    from holiday
    where year(date)=%s
    order by date;''')
    return query

def update_holiday():
    query = ('''update holiday
    set date = %s, holiday_desc = %s, eligibility = %s
    where id= %s;''')
    return query

def delete_holiday():
    query = ('''delete from holiday where id=%s;''')
    return query

def add_holiday():
    query = ('''insert into holiday (date, holiday_desc, eligibility) values (%s, %s, %s);''')
    return query

def addtype():
    query = ('''insert into leave_type(leave_type, leave_discription) values(%s, %s);''')
    return query

def deletetype():
    query = ('''delete from leave_type where leave_type_id = %s''')
    return query

def edittype():
    query = ('''update leave_type set leave_type = %s, leave_discription = %s where leave_type_id= %s;''')
    return query

def emp_in_department():
    query = ('''select e.employee_id, e.employee_title, e.employee_fname, e.employee_lname, e.employee_email, d.department_name from employee as e
    left join department as d on e.department_id=d.department_id
    where e.department_id IN (select department_id from employee where employee_id = %s );''')
    return query

def emp_anniversary():
    query = ('''select e.employee_id, e.date_joined, lb.sl_reset_date 
    from employee as e
    left join leave_balance as lb on e.employee_id=lb.employee_id;''')
    return query

def reset_sickleavebalance():
    query = ('''update leave_balance set sick_leave_balance = 37.5, sl_reset_date = curdate() where employee_id = %s;''')
    return query

def new_approval():
    query = ('''select e.employee_id,e.employee_fname, e.employee_lname,lr.leave_type_id,lt.leave_type,
              date_format(lr.start_date,'%d %b %Y'),date_format(lr.end_date,'%d %b %Y'), 
              lr.approval_manager_id,am.employee_fname as manager_fname, am.employee_lname as manager_lname, 
              lr.comment, rs.status_approval_description,lr.duration_days,
              date_format(lr.updated_at, '%d %b %Y') as 'date updated', lr.request_id, lr.start_date, lr.end_date, lr.comment_rejected
              from leave_request lr
              left join employee e on lr.employee_id = e.employee_id
              left join leave_type lt on lr.leave_type_id = lt.leave_type_id
              left join request_status rs on lr.status_approval = rs.status_approval_id
              left join employee as am on lr.approval_manager_id=am.employee_id
              where e.employee_id = %s and (lr.status_approval=1 OR lr.status_approval=-2) and lr.updated_at >= date_sub(curdate(), interval 1 month)
              order by lr.start_date desc;''')
    return query

def change_password():
    query=('update employee set employee_password = %s where employee_id =%s;')
    return query