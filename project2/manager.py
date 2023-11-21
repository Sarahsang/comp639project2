from project2 import app
from project2 import connect_proj2
from project2 import queries
from project2 import queries_manager
from project2 import routes
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from project2.db import getCursor
from datetime import datetime
from flask import flash

import mysql.connector
import bcrypt


dbconn = None
connection = None


@app.route('/manager/myapproval', methods=["GET", "POST"])
def myapproval():
    mydirectreports=''
    myapproval_pending=''
    myapproval_approved=''

    emp_selected=request.form.get('mydirectreports')
    fortnight_select=request.form.get('payrollfortnight')
  # connect to the database
    dbconn = routes.getCursor()

    if (request.form.get('mydirectreports') == 'all' and request.form.get('payrollfortnight') == 'all'):
      # query the database for the leave balance
      dbconn.execute(queries_manager.mydirectreports(),(session['id'],))
      # fetch one record and return result
      mydirectreports = dbconn.fetchall()
      dbconn.execute(queries_manager.myapproval_pending(),(session['id'],))
      myapproval_pending = dbconn.fetchall() 
      dbconn.execute(queries_manager.myapproval_approved(),(session['id'],))
      myapproval_approved = dbconn.fetchall() 

    dbconn.execute(queries.payroll_fortnight_current())
    payroll_fortnight_current = dbconn.fetchall() 
    dbconn.execute(queries.payroll_fortnight_future())
    payroll_fortnight_future = dbconn.fetchall() 
    dbconn.execute(queries.payroll_fortnight_past())
    payroll_fortnight_past = dbconn.fetchall() 
    
    return render_template("manager_myapproval.html", title="My Approval", session=session, 
                           mydirectreports=mydirectreports, 
                           myapproval_pending=myapproval_pending, 
                           myapproval_approved=myapproval_approved,
                           payroll_fortnight_current=payroll_fortnight_current,
                           payroll_fortnight_future=payroll_fortnight_future,
                           payroll_fortnight_past=payroll_fortnight_past,
                           emp_selected=emp_selected,
                           fortnight_select=fortnight_select)


@app.route('/manager/view_request/<int:request_id>', methods=["GET"])
def view_request(request_id):
    dbconn = getCursor()
    dbconn.execute(queries_manager.new_leave_requests_details(), (request_id,))
    request_details = dbconn.fetchone()
    
    if request_details is not None:
        request_details = list(request_details)
        request_details[2] = request_details[2].strftime("%d %b, %Y")  # date requested
        request_details[7] = request_details[7].strftime("%d %b, %Y")  # start date
        request_details[8] = request_details[8].strftime("%d %b, %Y")  # end date
        
    return render_template("manager_myDRrequest_details.html", title="My DR Request Details", request_details=request_details)

# the route for the manager to approve leave requests
@app.route('/approve_leave', methods=['POST'])
def approve_leave():
    
    # Obtain request_id and manager_id from the form data
    if session['role_id'] == 1:  # The role ID for admin is 1
        request_id = request.form['request_id']
        dbconn = getCursor()
        dbconn.execute(queries_manager.approve_leaves_admin(), (request_id,))
        dbconn.close()
        #send pop up message for the applicant when the leave request has been approved.
        
        
    elif session['role_id'] == 2: #The role ID for approval manager is 2
        request_id = request.form['request_id']
        manager_id = request.form['manager_id'] 
        
        dbconn = getCursor()
        dbconn.execute(queries_manager.approve_leaves_manager(), (request_id, manager_id))
        dbconn.close()   
  
    return redirect(request.referrer)

@app.route('/manager/undo_leave', methods=['POST'])
def undo_leave():
    start_date_str = request.form.get('start_date')
    start_date = datetime.strptime(start_date_str, "%d %b, %Y")
    # Check if the start date is in the past
    if start_date < datetime.now():
        # The start date is in the past, so don't approve the leave
        flash('Cannot Undo leave request because the start date is in the past')
        return redirect(request.referrer)
    
    # Obtain request_id and manager_id from the form data
    if session['role_id'] == 1:  # The role ID for admin is 1
        request_id = request.form['request_id']
        dbconn = getCursor()
        dbconn.execute(queries_manager.undo_leaves_admin(), (request_id,))
        dbconn.close()
        #send pop up message for the applicant when the leave request has been approved.
        
    elif session['role_id'] == 2: #The role ID for approval manager is 2
        request_id = request.form['request_id']
        manager_id = request.form['manager_id'] 
        
        dbconn = getCursor()
        dbconn.execute(queries_manager.undo_leaves_manager(), (request_id, manager_id))
        dbconn.close()   
  
    return redirect(request.referrer)

@app.route('/manager/withdraw_leave', methods=['POST', 'GET'])
def withdraw_leave_manager():
    # Obtain request_id and manager_id from the form data
    request_id = request.form.get('request_id')
    comment_withdrawn = request.form.get('comment_withdrawn')
    dbconn = getCursor()
    dbconn.execute(queries_manager.withdraw_leave_manager(), (comment_withdrawn, request_id))
    dbconn.close()
    return redirect(request.referrer)

# the route for the manager to reject leave requests
@app.route('/manager/reject_leave', methods=['POST', 'GET'])
def reject_leave():
    if request.method == 'POST':
    # Obtain request_id and rejection comments from the form 
        request_id = request.form.get('request_id')
        comment_rejected = request.form.get('comment_rejected')
        dbconn = getCursor()
        td_parameters = (comment_rejected, request_id)
        dbconn.execute(queries_manager.reject_leave(),td_parameters)
        dbconn.close()
    return redirect(request.referrer)

# the route for the manager to view all leave requests
@app.route('/manager/request_log', methods=['GET'])
def request_log():
    dbconn = getCursor()
    
    if session['role_id'] == 1:  # The role ID for admin is 1
        dbconn.execute(queries_manager.all_leave_requests_for_admin())
    elif session['role_id'] == 2:  #The role ID for approval manager is 2
        dbconn.execute(queries_manager.all_leave_requests_for_manager(), (session['id'],))

    request_log = dbconn.fetchall()

    count=0
    for row in request_log:
        row_list = list(row)
        row_list[0]=row_list[0].strftime("%d %b, %Y")
        row_list[5]=row_list[5].strftime("%d %b, %Y")
        row_list[6]=row_list[6].strftime("%d %b, %Y")
        print(row_list[5])
        request_log[count]=tuple(row_list)
        count=count+1
        
    return render_template("request_log.html", title="Request Log", 
                           request_log=request_log, session=session)
   

# BLW display list of my direct reports as an approval manager or an admin
@app.route('/manager/mydirectreports', methods=["GET", "POST"])
def mydirectreports():
  # connect to the database
    dbconn = routes.getCursor()
    # query the database for the leave balance
    dbconn.execute(queries_manager.mydirectreports(),(session['id'],))
    # fetch all records and return result
    mydirectreports = dbconn.fetchall()
    print(mydirectreports)
    return render_template("manager_mydirectreports.html", title="My Direct Reports", session=session, mydirectreports=mydirectreports)
# BLW display my DR leave requests for each employee
@app.route('/manager/request_log_employee', methods=['GET'])
def request_log_employee():
    emp_id=request.args.get('id')
    print(emp_id)
    # connect to the database
    dbconn = routes.getCursor()
    # query the database for the leave requests for the employee
    dbconn.execute(queries_manager.all_leave_requests_for_employee(), (emp_id,))
    # fetch all records for one employee and return result
    request_log_employee = dbconn.fetchall()
    print(request_log_employee)
# convert dates to correct format
    count=0
    for row in request_log_employee:
        row_list = list(row)
        row_list[0]=row_list[0].strftime("%d %b, %Y")
        row_list[5]=row_list[5].strftime("%d %b, %Y")
        row_list[6]=row_list[6].strftime("%d %b, %Y")
        print(row_list[5])
        request_log_employee[count]=tuple(row_list)
        count=count+1
    return render_template("manager_myDRrequest_log.html", title="Request Log Employee", 
                           request_log_employee=request_log_employee, session=session)

# BLW display my Direct Reports personal details for each employee under me as an approval manager or admin
@app.route('/manager/myDRdetail', methods=["GET", "POST"])
def myDRdetail():
    userid=request.args.get('id')
    # connect to the database
    dbconn = routes.getCursor()
    # query the database for the employee's email
    dbconn.execute(queries_manager.mydruserdetail(), (userid,))
    # fetch one record and return result
    myDRuserdetail = dbconn.fetchone()
    print(myDRuserdetail[5])
    print(myDRuserdetail[5].strftime("%d %b, %Y"))
    myDRuserdetail_list = list(myDRuserdetail)
    myDRuserdetail_list[5]=myDRuserdetail[5].strftime("%d %b, %Y")
    myDRuserdetail_list[7]=myDRuserdetail[7].strftime("%d %b, %Y")
    myDRuserdetail=tuple(myDRuserdetail_list)
    return render_template ("manager_myDRuserdetail.html", title="My DR Details", session=session, myDRuserdetail=myDRuserdetail)

# BLW display my Direct Reports currentleave balances for each employee under me as an approval manager or admin
@app.route('/manager/myDRLeaveBalance')
def myDRLeaveBalance():
    userid=request.args.get('id')
    print(userid)

  # connect to the database
    dbconn = routes.getCursor()
    # query the database for the leave balance
    dbconn.execute(queries_manager.mydrleavebalance(), (userid,))
    # fetch one record and return result
    myDRLeaveBalance = dbconn.fetchone()
    annualDays=(float(myDRLeaveBalance[3])/7.5)
    AnnualDaysDisplay= round( annualDays, 2)
    if annualDays is not None:
        AnnualDaysDisplay=round(annualDays, 2)
    else:
        AnnualDaysDisplay=0
    sickDays=(float(myDRLeaveBalance[4])/7.5)
    sickDaysDisplay= round( sickDays, 2)
    if sickDays is not None:
        sickDaysDisplay=round(sickDays, 2)
    else:
        AnnualDaysDisplay=0
    
    dbconn.execute(queries.annualleavebalance_unapproved(), (userid,))
    # fetch one record and return result
    annual_unapproved = dbconn.fetchone()
    unapprovedAnnualDays=annual_unapproved[1]
    if annual_unapproved[1] is not None:
        annual_unapprovedHours=round((float(annual_unapproved[1])*7.5), 2)
    else:
        unapprovedAnnualDays=0
        annual_unapprovedHours=0
    dbconn.execute(queries. annualleavebalance_unpaid(), (userid,))
    # fetch one record and return result
    annual_unpaid = dbconn.fetchone()
    unpaidAnnualDays=annual_unpaid[1]
    if annual_unpaid[1] is not None:
        annual_unpaidHours=round((float(annual_unpaid[1])*7.5), 2)
    else:
        unpaidAnnualDays=0
        annual_unpaidHours=0

    dbconn.execute(queries.sickleavebalance_unapproved(), (userid,))
    # fetch one record and return result
    sick_unapproved = dbconn.fetchone()
    sick_unapprovedDays=sick_unapproved[1]
    if sick_unapproved[1] is not None:
        unapprovedSickHours=round((float(sick_unapproved[1])*7.5),2 )
    else:
        unapprovedSickHours=0
        sick_unapprovedDays=0
    dbconn.execute(queries. sickleavebalance_unpaid(), (userid,))
    # fetch one record and return result
    sick_unpaid = dbconn.fetchone()
    unpaidSickDays=sick_unpaid[1]
    if sick_unpaid[1] is not None:
        sick_unpaidHours=round((float(sick_unpaid[1])*7.5),2 )
    else:
        unpaidSickDays=0
        sick_unpaidHours=0

   
    return render_template("manager_myDRLeaveBalances.html",unpaidSickDays=unpaidSickDays,  sick_unpaidHours=sick_unpaidHours, 
        sick_unapprovedDays=sick_unapprovedDays, unapprovedSickHours=unapprovedSickHours, annual_unpaidHours=annual_unpaidHours, 
        unpaidAnnualDays=unpaidAnnualDays, annual_unapprovedHours=annual_unapprovedHours, unapprovedAnnualDays=unapprovedAnnualDays, 
        sickDaysDisplay=sickDaysDisplay, AnnualDaysDisplay=AnnualDaysDisplay, myDRLeaveBalance=myDRLeaveBalance, title="My Direct Report Leave Balances", session=session)


@app.route('/manager/liabilityReport', methods=["GET", "POST"])
def liabilityReport():
    # connect to the database
    dbconn = routes.getCursor()
     # query the database for the leave balance
    if session['role_id'] == 1:  # The role ID for admin is 1
        dbconn.execute(queries_manager.leaveliabilityreportsadmin())
    elif session['role_id'] == 2:  #The role ID for approval manager is 2
        dbconn.execute(queries_manager.leaveliabilityreportsmanager(),(session['id'],))
    # fetch all records and return result
    leaveLiabilityReports = dbconn.fetchall()
    return render_template ("manager_liabilityReport.html", title="Annual Leave Liability Report", session=session, leaveLiabilityReports=leaveLiabilityReports)


@app.route('/manager/LeaveExceptionReport', methods=["GET", "POST"])
def leave_exception_report():
    # connect to the database
    dbconn = routes.getCursor()
     # query the database for the report
     
    if session['role_id'] == 1:  # The role ID for admin is 1
        dbconn.execute(queries_manager.leaveexceptionreportadmin())
    elif session['role_id'] == 2:  #The role ID for approval manager is 2
        dbconn.execute(queries_manager.leaveexceptionreportmanager(),(session['id'],))
    # fetch all records and return result
    LeaveExceptionReport = dbconn.fetchall()
    return render_template ("manager_LeaveExceptionReport.html", title="Leave Exception Report", session=session, LeaveExceptionReport=LeaveExceptionReport)

