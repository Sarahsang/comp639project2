
def mydirectreports():
    query=('''select leave_balance.employee_id, employee.employee_title, employee.employee_fname as firstname, employee.employee_lname as lastname, employee.employee_email,
            p.position_name, employee.position_start_date, d.department_name, se.employee_fname as supervisor_fname, se.employee_lname as supervisor_lname, se.employee_email as supervisor_email,
            leave_balance.annual_leave_balance as annuallb,  leave_balance.sick_leave_balance as sicklb
            from leave_balance 
            left join employee on leave_balance.employee_id=employee.employee_id 
            left join position as p on employee.position_id=p.position_id
            left join department as d on employee.department_id=d.department_id
            left join employee as se on employee.supervisor_id=se.employee_id
            where employee.approval_manager_id=%s
            ;''')
    return query
# a query to return the direct report employee selected details (selected by the manager)
def mydruserdetail():
    query= (
        ''' select e.employee_id, e.employee_title, e.employee_fname, e.employee_lname, e.employee_email, e.date_joined, p.position_name, e.position_start_date, d.department_name,
        e.supervisor_id, s.employee_fname as supervisor_fname, s.employee_lname as supervisor_lname, s.employee_email as supervisor_email, e.approval_manager_id, am.employee_fname as manager_fname,
        am.employee_lname as manager_lname, am.employee_email as manager_email
            from employee as e
            left join employee_ROLE as er on e.employee_id=er.employee_id 
            left join position as p on e.position_id=p.position_id
            left join department as d on e.department_id=d.department_id
            left join employee as s on e.supervisor_id=s.employee_id
            left join employee as am on e.approval_manager_id=am.employee_id
            where e.employee_id = %s
            ; '''
    )
    return query
# a query to return the direct report employee selected leave balance (selected by the manager)
def mydrleavebalance():
    query=('''select leave_balance.employee_id, employee.employee_fname as firstname, employee.employee_lname as lastname,
            leave_balance.annual_leave_balance as annuallb,  leave_balance.sick_leave_balance as sicklb
            from leave_balance left join employee on leave_balance.employee_id=employee.employee_id where employee.employee_id =%s
            ;''')
    return query
# a query to return all leave requests for a specific employee - can be used by the approval manager, the admin or the employee themselves
def all_leave_requests_for_employee():
    query = ('''select lr.created_at as 'date requested', 
                e.employee_fname, 
                e.employee_lname,
                case lr.status_approval
                    when 0 then 'pending'
                    when 1 then 'approved'
                    when 2 then 'approved and paid'
                    when -1 then 'withdrawn'
                    when -2 then 'rejected'
                    else 'unknown status'
                end as 'status',
                lt.leave_type as 'leave type',
                lr.start_date as 'start date',
                lr.end_date as 'end date',
                lr.duration_days as 'days requested',
                lb.annual_leave_balance as 'annual leave balance',
                lb.sick_leave_balance as 'sick leave balance',
                lr.request_id,
                lr.approval_manager_id,
                processed_by_payroll
                from leave_request lr
                inner join employee e on e.employee_id = lr.employee_id
                inner join leave_type lt on lt.leave_type_id = lr.leave_type_id
                inner join leave_balance lb on lb.employee_id = e.employee_id
                where lr.employee_id = %s
                order by case lr.status_approval when 0 then 1 else 2 end,
                lr.created_at desc, 
                lr.start_date desc;''')
    return query

def myapproval_pending():
    query= ("""
            select lr.request_id, e1.employee_email, lt.leave_type, lr.start_date, lr.end_date, 'Pending Approval' as status_approval, lr.comment, lr.duration_days, lr.created_at
            from leave_request as lr
            left join employee as e1 on lr.employee_id=e1.employee_id
            left join leave_type as lt on lr.leave_type_id=lt.leave_type_id
            where lr.status_approval=0 and lr.employee_id in (
            select e2.employee_id 
            from employee as e2
            where e2.approval_manager_id = %s)
            ;
        """)
    return query

def myapproval_approved():
    query= ("""
            select lr.request_id, e1.employee_email, lt.leave_type, lr.start_date, lr.end_date, 'Approved' as status_approval, lr.comment, lr.duration_days, lr.created_at
            from leave_request as lr
            left join employee as e1 on lr.employee_id=e1.employee_id
            left join leave_type as lt on lr.leave_type_id=lt.leave_type_id
            where lr.status_approval=1 and lr.employee_id in (
            select e2.employee_id 
            from employee as e2
            where e2.approval_manager_id = %s)
            ;
        """)
    return query

def new_leave_requests_details():
    query = ('''select lr.request_id as 'request id',
                lr.employee_id as 'employee id',
                lr.created_at as 'date requested',
                e.employee_fname as 'first name',
                e.employee_lname as 'last name',
                case
                    when lr.status_approval = 0 then 'pending'
                    when lr.status_approval = 1 then 'approved'
                    when lr.status_approval = 2 then 'approved and paid'
                    when lr.status_approval = 3 then 'draft'
                    when lr.status_approval = -1 then 'withdrawn'
                    when lr.status_approval = -2 then 'rejected'
                    else 'unknown status'
                end as 'status',
                lt.leave_type as 'leave type',
                lr.start_date as 'start date',
                lr.end_date as 'end date',
                lr.duration_days as 'days requested',
                lb.annual_leave_balance as 'annual leave balance',
                lb.sick_leave_balance as 'sick leave balance',
                concat(am.employee_fname, ' ', am.employee_lname) as 'approval manager name',
                lr.comment as 'reason',
                lr.comment_withdrawn as 'reason withdrawn',
                lr.comment_rejected as 'reason rejected',
                lr.approval_manager_id as 'manager_id',
                lr.duration_days * 7.5 as 'hours requested',
                lr.start_date, lr.end_date,
                processed_by_payroll
                from 
                leave_request lr
                inner join employee e on e.employee_id = lr.employee_id
                inner join leave_type lt on lt.leave_type_id = lr.leave_type_id
                inner join leave_balance lb on lb.employee_id = e.employee_id
                inner join employee am on am.employee_id = lr.approval_manager_id
                where lr.request_id = %s;'''
            )
    return query  

# when manager approves leave the status is updated to approved
def approve_leaves_manager():
    query = ('''update leave_request 
             set status_approval = 1,
            updated_at = current_timestamp
            where request_id = %s
            and approval_manager_id = %s;'''
            )
    return query

# when admin approves leave the status is updated to approved
def approve_leaves_admin():
    query = ('''update leave_request 
             set status_approval = 1,
            updated_at = current_timestamp
            where request_id = %s;'''
            )
    return query

def undo_leaves_manager():
    query = ('''update leave_request 
             set status_approval = 0,
             comment_withdrawn = null,
             comment_rejected = null,
            updated_at = current_timestamp
            where request_id = %s
            and approval_manager_id = %s;'''
            )
    return query
def undo_leaves_admin():
    query = ('''update leave_request 
             set status_approval = 0,
             comment_withdrawn = null,
             comment_rejected = null,
            updated_at = current_timestamp
            where request_id = %s;'''
            )
    return query

# when manager rejects leave the status is updated to rejected
def reject_leave():
    query = ('''
            update leave_request 
            set status_approval = -2, comment_rejected = %s, updated_at = current_timestamp
            where request_id = %s
            ;'''
            )
    return query

# when manager edits the direct reports leave the status is updated to draft (3)
def edit_mydrrequest_details():
    query = ('''
            update leave_request 
            set leave_type_id = %s, start_date = %s, end_date = %s, status_approval=3, 
            comment = %s, duration_days = %s, comment_rejected = %s, updated_at = current_timestamp
            where request_id = %s
            ;'''
            )
    return query

def withdraw_leave_manager():
    query= ('''
            update leave_request 
            set status_approval= -1, comment_withdrawn = %s,
            updated_at = current_timestamp
            where request_id=%s;'''
            )
    return query


def all_new_leave_requests_for_admin():
    query = ('''select lr.created_at as 'date requested', 
                e.employee_fname, 
                e.employee_lname,
                case lr.status_approval
                    when 0 then 'pending'
                    when 1 then 'approved'
                    when 2 then 'approved and paid'
                    when 3 then 'draft'
                    when -1 then 'withdrawn'
                    when -2 then 'rejected' 
                    else 'unknown status'
                end as 'status',
                lt.leave_type as 'leave type',
                lr.start_date as 'start date',
                lr.end_date as 'end date',
                lr.duration_days as 'days requested',
                lb.annual_leave_balance as 'annual leave balance',
                lb.sick_leave_balance as 'sick leave balance',
                lr.request_id,
                lr.employee_id,
                lr.duration_days * 7.5 as 'hours requested'
                from leave_request lr
                inner join employee e on e.employee_id = lr.employee_id
                inner join leave_type lt on lt.leave_type_id = lr.leave_type_id
                inner join leave_balance lb on lb.employee_id = e.employee_id
                where lr.processed_by_payroll = 0
                and lr.status_approval = 0 
                AND (lr.status_approval != 0 OR lr.start_date >= CURDATE())                
                order by sTATUs desc, lr.start_date asc, lr.created_at asc;'''
            )
    return query

def all_new_leave_requests_for_manager():
    query = ('''select lr.created_at as 'date requested', 
                e.employee_fname, 
                e.employee_lname,
                case lr.status_approval
                    when 0 then 'pending'
                    when 1 then 'approved'
                    when 2 then 'approved and paid'
                    when 3 then 'draft'
                    when -1 then 'withdrawn'
                    when -2 then 'rejected'
                    else 'unknown status'
                end as 'status',
                lt.leave_type as 'leave type',
                lr.start_date as 'start date',
                lr.end_date as 'end date',
                lr.duration_days as 'days requested',
                lb.annual_leave_balance as 'annual leave balance',
                lb.sick_leave_balance as 'sick leave balance',
                lr.request_id,
                lr.approval_manager_id,
                lr.duration_days * 7.5 as 'hours requested',
                lr.employee_id
                from leave_request lr
                inner join employee e on e.employee_id = lr.employee_id
                inner join leave_type lt on lt.leave_type_id = lr.leave_type_id
                inner join leave_balance lb on lb.employee_id = e.employee_id
                where lr.processed_by_payroll = 0
                and lr.status_approval = 0
                and lr.approval_manager_id = %s
                AND (lr.status_approval != 0 OR lr.start_date >= CURDATE())
                order by sTATUs desc, lr.start_date asc, lr.created_at asc;'''
            )
    return query

          

def all_leave_requests_for_admin():
    query = ('''select lr.created_at as 'date requested', 
                e.employee_fname, 
                e.employee_lname,
                case lr.status_approval
                    when 0 then 'pending'
                    when 1 then 'approved'
                    when 2 then 'approved and paid'
                    when 3 then 'draft'
                    when -1 then 'withdrawn'
                    when -2 then 'rejected'
                    else 'unknown status'
                end as 'status',
                lt.leave_type as 'leave type',
                lr.start_date as 'start date',
                lr.end_date as 'end date',
                lr.duration_days as 'days requested',
                lb.annual_leave_balance as 'annual leave balance',
                lb.sick_leave_balance as 'sick leave balance',
                lr.request_id,
                lr.employee_id,
                processed_by_payroll
                from leave_request lr
                inner join employee e on e.employee_id = lr.employee_id
                inner join leave_type lt on lt.leave_type_id = lr.leave_type_id
                inner join leave_balance lb on lb.employee_id = e.employee_id
                WHERE lr.status_approval != 0 OR lr.start_date >= CURDATE()              
                order by case lr.status_approval when 0 then 1 else 2 end,
                lr.created_at desc, 
                lr.start_date desc;'''
            )
    return query

def all_leave_requests_for_manager():
    query = ('''select lr.created_at as 'date requested', 
                e.employee_fname, 
                e.employee_lname,
                case lr.status_approval
                    when 0 then 'pending'
                    when 1 then 'approved'
                    when 2 then 'approved and paid'
                    when 3 then 'draft'
                    when -1 then 'withdrawn'
                    when -2 then 'rejected'
                    else 'unknown status'
                end as 'status',
                lt.leave_type as 'leave type',
                lr.start_date as 'start date',
                lr.end_date as 'end date',
                lr.duration_days as 'days requested',
                lb.annual_leave_balance as 'annual leave balance',
                lb.sick_leave_balance as 'sick leave balance',
                lr.request_id,
                lr.approval_manager_id,
                processed_by_payroll
                from leave_request lr
                inner join employee e on e.employee_id = lr.employee_id
                inner join leave_type lt on lt.leave_type_id = lr.leave_type_id
                inner join leave_balance lb on lb.employee_id = e.employee_id
                where lr.approval_manager_id = %s
                AND (lr.status_approval != 0 OR lr.start_date >= CURDATE())
                order by case lr.status_approval when 0 then 1 else 2 end,
                lr.created_at desc, 
                lr.start_date desc;'''
            )
    return query

def leaveliabilityreportsmanager():
    query=('''select leave_balance.employee_id, employee.employee_title, employee.employee_fname as firstname, employee.employee_lname as lastname, p.position_name, d.department_name, 
            round(leave_balance.annual_leave_balance, 1) as annuallbhour, round(leave_balance.annual_leave_balance/7.5, 2) as annuallb
            from leave_balance 
            left join employee on leave_balance.employee_id=employee.employee_id 
            left join position as p on employee.position_id=p.position_id
            left join department as d on employee.department_id=d.department_id
            where employee.approval_manager_id=%s
            order by firstname, lastname
            ;''')
    return query

def leaveliabilityreportsadmin():
    query=('''select leave_balance.employee_id, employee.employee_title, employee.employee_fname as firstname, employee.employee_lname as lastname, p.position_name, d.department_name, 
            round(leave_balance.annual_leave_balance, 1) as annuallbhour, round(leave_balance.annual_leave_balance/7.5, 2) as annuallb
            from leave_balance 
            left join employee on leave_balance.employee_id=employee.employee_id 
            left join position as p on employee.position_id=p.position_id
            left join department as d on employee.department_id=d.department_id
            order by firstname, lastname
            ;''')
    return query

def leaveexceptionreportmanager():
    query=('''select leave_balance.employee_id, employee.employee_title, employee.employee_fname as firstname, employee.employee_lname as lastname, p.position_name, d.department_name, 
            round(leave_balance.annual_leave_balance, 1) as annuallbhour, round(leave_balance.annual_leave_balance/7.5, 2) as annuallb
            from leave_balance 
            left join employee on leave_balance.employee_id=employee.employee_id 
            left join position as p on employee.position_id=p.position_id
            left join department as d on employee.department_id=d.department_id
            where employee.approval_manager_id=%s
            and leave_balance.annual_leave_balance/7.5 >=30
            order by annuallbhour desc
            ;''')
    return query

def leaveexceptionreportadmin():
    query=('''select leave_balance.employee_id, employee.employee_title, employee.employee_fname as firstname, employee.employee_lname as lastname, p.position_name, d.department_name, 
            round(leave_balance.annual_leave_balance, 1) as annuallbhour, round(leave_balance.annual_leave_balance/7.5, 2) as annuallb
            from leave_balance 
            left join employee on leave_balance.employee_id=employee.employee_id 
            left join position as p on employee.position_id=p.position_id
            left join department as d on employee.department_id=d.department_id
            where leave_balance.annual_leave_balance/7.5 >=30
            order by annuallbhour desc
            ;''')
    return query