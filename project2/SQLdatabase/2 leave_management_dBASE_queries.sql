select * from employee;

select * from leave_balance;

select * from leave_request;

-- calculate leave cost days between two dates --
select sum(leave_cost_day) from datetable
where date >= '2023-05-24' and date <= '2023-05-27';

select * from leave_increment
where employee_id=1;



-- query returns all the employees with their position names, dept names, supervisor and approval manager names
select 
  e.employee_id, 
  e.employee_title, 
  e.employee_fname, 
  e.employee_lname, 
  e.employee_email, 
  e.date_joined,
  p.position_name, 
  e.position_start_date, 
  d.department_name, 
  e.supervisor_id, 
  s.employee_fname as supervisor_fname, 
  s.employee_lname as supervisor_lname, 
  s.employee_email as supervisor_email, 
  e.approval_manager_id, 
  am.employee_fname as manager_fname, 
  am.employee_lname as manager_lname, 
  am.employee_email as manager_email
from 
  employee as e
  left join employee_role as er on e.employee_id = er.employee_id 
  left join position as p on e.position_id = p.position_id
  left join department as d on e.department_id = d.department_id
  left join employee as s on e.supervisor_id = s.employee_id
  left join employee as am on e.approval_manager_id = am.employee_id
;

select lb.employee_id, lb.annual_leave_balance, e.date_joined
from leave_balance as lb
left join employee as e on lb.employee_id=e.employee_id
where e.employee_status=1;

-- as a manager, query out all the direct reports --
select e.employee_id, e.employee_title, e.employee_fname, e.employee_lname, e.employee_email
from employee as e
where e.approval_manager_id = 18;

-- as a manager, my approval in pending status --
select lr.request_id, e1.employee_email, lt.leave_type, lr.start_date, lr.end_date, 'pending approval' as status_approval, lr.comment, lr.duration_days, lr.created_at
from leave_request as lr
left join employee as e1 on lr.employee_id=e1.employee_id
left join leave_type as lt on lr.leave_type_id=lt.leave_type_id
where lr.status_approval=0 and lr.employee_id in (
select e2.employee_id 
from employee as e2
where e2.approval_manager_id = 18)
;

-- as a manager, my approval in approved status --
select lr.request_id, e1.employee_email, lt.leave_type, lr.start_date, lr.end_date, 'approved' as status_approval, lr.comment, lr.duration_days, lr.created_at
from leave_request as lr
left join employee as e1 on lr.employee_id=e1.employee_id
left join leave_type as lt on lr.leave_type_id=lt.leave_type_id
where lr.status_approval=1 and lr.employee_id in (
select e2.employee_id 
from employee as e2
where e2.approval_manager_id = 18)
;

select payroll_fortnight_id, start, end
from payroll_fortnight;

-- fortnights in the past --
select payroll_fortnight_id, start, end, status
            from payroll_fortnight
            where end<=curdate()
            order by start desc
;

-- fortnights in the future --
select payroll_fortnight_id, start, end, status
            from payroll_fortnight
            where start>=curdate()
            order by start desc
;

-- fortnights current --
select payroll_fortnight_id, start, end, status
            from payroll_fortnight
            where start<=curdate() and end>=curdate()
            order by start desc
;

select getdate();

-- withdraw a leave reqeust --
update leave_request 
set status_approval=1-2
where request_id=78
;

select * from leave_request
where request_id=78
;


select e.employee_id,e.employee_fname, e.employee_lname,lr.leave_type_id,lt.leave_type,
              date_format(lr.start_date,'%d %b %y'),date_format(lr.end_date,'%d %b %y'), 
              lr.approval_manager_id,am.employee_fname as manager_fname, am.employee_lname as manager_lname, 
              lr.comment, rs.status_approval_description,lr.duration_days,
              date_format(lr.created_at, '%d %b %y') as 'date requested', lr.request_id, lr.start_date, lr.end_date
              from leave_request lr
              left join employee e on lr.employee_id = e.employee_id
              left join leave_type lt on lr.leave_type_id = lt.leave_type_id
              left join request_status rs on lr.status_approval = rs.status_approval_id
              left join employee as am on lr.approval_manager_id=am.employee_id
              where lr.request_id = 18;
              
select start_date, end_date from leave_request where employee_id=29 and status_approval<>3 ;

select employee_id, supervisor_id, approval_manager_id, employee_title, employee_fname, employee_lname, employee_email, department_id, position_name
from employee
join position on employee.position_id=position.position_id;

select datetable.date, day_num, eligibility as holiday, '' as tag
from datetable
left join holiday on datetable.date=holiday.date
where datetable.date>='2023-01-01';

select e.department_id, lr.employee_id, rs.status_approval_description, lr.start_date, lr.end_date
from leave_request as lr
left join request_status as rs on lr.leave_type_id=rs.status_approval_id
left join employee as e on lr.employee_id=e.employee_id
where lr.status_approval>=0 and lr.status_approval<=2
order by e.department_id, lr.employee_id;

select pf.payroll_fortnight_id, pf.start, pf.end, pf.status, pf.process_date, e.employee_fname, e.employee_lname
from payroll_fortnight as pf
left join employee as e on pf.by_admin=e.employee_id
where pf.start>'2023-01-01';

select employee_id, leave_increment, payroll_fortnight_id
from leave_increment
where payroll_fortnight_id='2023wk19';

select * from leave_balance;

update leave_balance 
set annual_leave_balance = annual_leave_balance + -1
where employee_id = 1;

update payroll_fortnight 
set status = 1
where payroll_fortnight_id = '2023wk21';

select *
from payroll_fortnight;

select count(request_id), employee_id
from leave_request
where status_approval = 1 and processed_by_payroll = 0 and end_date < curdate()
group by employee_id;

select * 
from leave_request
where status_approval = 1 and processed_by_payroll = 0 and end_date < curdate();

select *
from holiday
where year(date)=2019;

select id,date_format(date,'%d %m %y'), holiday_desc, eligibility
    from holiday
    where year(date)=2019;
    
delete from holiday where id=1
;

select e.department_id, lr.employee_id, lt.leave_type, lr.start_date, lr.end_date
        from leave_request as lr
        left join request_status as rs on lr.leave_type_id=rs.status_approval_id
        left join employee as e on lr.employee_id=e.employee_id
        left join leave_type as lt on lr.leave_type_id=lt.leave_type_id
        where lr.status_approval>=0 and lr.status_approval<=2 and e.department_id in (select department_id from employee where employee_id = 1 )
        order by e.department_id, lr.employee_id;
        
select e.employee_id, e.employee_title, e.employee_fname, e.employee_lname, e.employee_email, d.department_name from employee as e
left join department as d on e.department_id=d.department_id
where e.department_id in (select department_id from employee where employee_id = 1 );


select e.department_id, lr.employee_id, lt.leave_type, lr.start_date, lr.end_date
        from leave_request as lr
        left join request_status as rs on lr.leave_type_id=rs.status_approval_id
        left join employee as e on lr.employee_id=e.employee_id
        left join leave_type as lt on lr.leave_type_id=lt.leave_type_id
        where lr.status_approval>=0 and lr.status_approval<=2 and lr.employee_id = 1
        order by e.department_id, lr.employee_id;
        
select e.employee_id, e.date_joined, lb.sl_reset_date 
from employee as e
left join leave_balance as lb on e.employee_id=lb.employee_id;

select * from leave_balance;

update leave_balance set sick_leave_balance = 37.5, sl_reset_date = curdate() where employee_id = 1;

update employee set date_joined = '2020-06-16' where employee_id = 5;


select * from leave_request where request_id=95;

select * from leave_request where employee_id =5;

update leave_request set leave_type_id = 2
where request_id = 95;

select * 
        from leave_request
        where status_approval = 1 and processed_by_payroll = 0 and start_date < curdate();
        
select * from datetable;

select * from leave_request where status_approval=1;