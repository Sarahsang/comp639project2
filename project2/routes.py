from project2 import app
from project2 import connect_proj2
from project2 import queries
from project2 import queries_manager
from project2 import orgchart
from flask import render_template
from flask import request, jsonify
from flask import redirect
from flask import url_for
from flask import session
from project2 import manager
from project2.db import getCursor
import mysql.connector
import bcrypt
import datetime
from decimal import Decimal
import json
from datetime import date
import re

# Custom JSON encoder class
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()  # Convert date to string in ISO format
        return super().default(obj)


# #User global variable for passing logged in user information
employee = None

#Date time global variables for queries
today=datetime.date.today()
today_string=today.strftime("%Y-%m-%d")

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your_secret_key'

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/")
def home():
    return render_template("login.html", title="login")

@app.route("/login", methods=["GET", "POST"])
def Login():
    print(session)
    # output message if something goes wrong...
    msg = ''
    # check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # connect to the database
        dbconn = getCursor()
        # query the database for the employee's email
        dbconn.execute(queries.login(), (email,))
        # fetch one record and return result
        employee = dbconn.fetchone()
        print (employee)
        # if employee exists in the database
        if employee is not None:
            passworddB = employee[2]
            if bcrypt.checkpw(password.encode('utf-8'),passworddB.encode('utf-8')):
            # If account exists in accounts table in out database
            #print the session before the new one starts
                print(session)
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = employee[0]
                session['role_id'] = employee[1]
                session['first_name'] = employee[3]
                session['last_name'] = employee[4]
                # Redirect to dashboard page
                #print the new session details
                print(session)
                return redirect(url_for('dashboard'))
            else:
                #password incorrect
                msg = 'Incorrect login! Try again.'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect login! Try again.'
    # render the login page template
    return render_template("login.html",title="login", session=session, msg=msg)

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('role_id', None)
   session.pop('first_name', None)
   session.pop('last_name', None)
   # Redirect to login page
   return redirect(url_for('Login'))


@app.route('/mydetail', methods=["GET", "POST"])
def mydetail():
    userid=request.args.get('id')
    # connect to the database
    dbconn = getCursor()
    # query the database for the employee's email
    dbconn.execute(queries.userdetail(), (userid,))
    # fetch one record and return result
    detail = dbconn.fetchone()
    print(detail[5])
    print(detail[5].strftime("%d %b, %Y"))
    detail_list = list(detail)
    detail_list[5]=detail[5].strftime("%d %b, %Y")
    detail_list[7]=detail[7].strftime("%d %b, %Y")
    detail=tuple(detail_list)

    dbconn.execute(queries.allemployee_orgchart())
    allemployee_orgchart = dbconn.fetchall()

    allemployee_orgchart_tuple = ()
    for i in allemployee_orgchart:
        t = (i[0],i)
        allemployee_orgchart_tuple = (*allemployee_orgchart_tuple, t)
    
    allemployee_orgchart_dict=dict(allemployee_orgchart_tuple)

    uid= int(userid)
    uid_s = uid
    uid_m = uid
    uid_dr = uid

    supervisor_list = []
    manager_list = []
    directreport_manager = ()
    directreport_supervisor = ()

    supervisor = allemployee_orgchart_dict[uid][1]
    manager =  allemployee_orgchart_dict[uid][2]

    while supervisor not in supervisor_list:
        supervisor_list.append(uid_s)
        supervisor = allemployee_orgchart_dict[uid_s][1]
        uid_s=int(allemployee_orgchart_dict[uid_s][1])
    supervisor_list.reverse()


    while manager not in manager_list:
        manager_list.append(uid_m)
        manager = allemployee_orgchart_dict[uid_m][2]
        uid_m=int(allemployee_orgchart_dict[uid_m][2])
    manager_list.reverse()

    for i in allemployee_orgchart:
        manager_dr=i[2]
        supervisor_dr=i[1]
        if manager_dr == uid:
            directreport_manager=(*directreport_manager,i)
        if supervisor_dr == uid:
            directreport_supervisor=(*directreport_supervisor,i)

    return render_template ("userdetail.html", title="My Details", 
                            session=session, detail=detail,
                            allemployee_orgchart_dict=allemployee_orgchart_dict,
                            supervisor_list=supervisor_list,
                            manager_list=manager_list,
                            directreport_manager=directreport_manager,
                            directreport_supervisor=directreport_supervisor)

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    print(session)
    if 'first_name' in session:
        user_name = session['first_name'] + " " + session['last_name']
        print("User Name:", user_name)
    else:
        print("User name not found in session")
        
    dbconn = getCursor()

    if session['role_id'] == 1:  # The role ID for admin is 1
        dbconn.execute(queries_manager.all_new_leave_requests_for_admin())
        new_leave_requests = dbconn.fetchall()
    elif session['role_id'] == 2: #The role ID for approval manager is 2
        dbconn.execute(queries_manager.all_new_leave_requests_for_manager(), (session['id'],))
        new_leave_requests = dbconn.fetchall()
    else:
        new_leave_requests = []
    
    count=0
    
    for row in new_leave_requests:
        row_list = list(row)
        row_list[0]=row_list[0].strftime("%d %b, %Y")
        row_list[5]=row_list[5].strftime("%d %b, %Y")
        row_list[6]=row_list[6].strftime("%d %b, %Y")
        print(row_list[5])
        new_leave_requests[count]=tuple(row_list)
        count=count+1

    #retrieve new approvals
    dbconn.execute(queries.new_approval(),(session['id'],))
    new_approval = dbconn.fetchall()
    #retrieve the number of new approvals
    length = dbconn.rowcount
    print(length)
        
    return render_template("dashboard.html", title="dashboard", user_name=user_name, length=length, new_approval=new_approval, session=session, new_leave_requests=new_leave_requests)


@app.route('/currentLeaveBalance')
def currentLeaveBalance():
    userid=request.args.get('id')
    print(userid)

  # connect to the database
    dbconn = getCursor()
    # query the database for the leave balance
    dbconn.execute(queries.leavebalance(), (userid,))
    # fetch one record and return result
    leaveBalance = dbconn.fetchone()
    annualDays=(float(leaveBalance[3])/7.5)
    AnnualDaysDisplay= round( annualDays, 2)
    if annualDays is not None:
        AnnualDaysDisplay=round(annualDays, 2)
    else:
        AnnualDaysDisplay=0
    sickDays=(float(leaveBalance[4])/7.5)
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
    dbconn.execute(queries.annualleavebalance_unpaid(), (userid,))
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
    unapprovedSickDays=sick_unapproved[1]
    if sick_unapproved[1] is not None:
        sick_unapprovedHours=round((float(sick_unapproved[1])*7.5),2 )
    else:
        unapprovedSickDays=0
        sick_unapprovedHours=0
    dbconn.execute(queries.sickleavebalance_unpaid(), (session['id'],))
    # fetch one record and return result
    sick_unpaid = dbconn.fetchone()
    unpaidSickDays=sick_unpaid[1]
    if sick_unpaid[1] is not None:
        sick_unpaidHours=round((float(sick_unpaid[1])*7.5),2 )
    else:
        unpaidSickDays=0
        sick_unpaidHours=0

   
    return render_template("currentLeaveBalance.html",unpaidSickDays=unpaidSickDays,  sick_unpaidHours=sick_unpaidHours, 
        sick_unapprovedHours=sick_unapprovedHours, unapprovedSickDays=unapprovedSickDays, annual_unpaidHours=annual_unpaidHours, 
        unpaidAnnualDays=unpaidAnnualDays, annual_unapprovedHours=annual_unapprovedHours, unapprovedAnnualDays=unapprovedAnnualDays, 
        sickDaysDisplay=sickDaysDisplay, AnnualDaysDisplay=AnnualDaysDisplay, leaveBalance=leaveBalance, title="My Leave Balance", session=session)


@app.route('/admin/addbalance', methods=["GET", "POST"])
def PayrollAddBalance():
  # connect to the database
    dbconn = getCursor()
    # query the database for the leave balance

    dbconn.execute(queries.payrollweeks())
    payrollweeks=dbconn.fetchall()

    dbconn.execute(queries.getapprovednotpaidrequests())
    approvednotpaidrequests=dbconn.fetchall()

    user_admin=request.args.get('uid')
    week=request.args.get('wk')
    action=request.args.get('action')

    cur_payrollwk=[]

    if(session['role_id']==1 and action=='1'):
        for row in range(len(payrollweeks)):
            if payrollweeks[row][0] == week and payrollweeks[row][3] == 0:
                cur_payrollwk = [payrollweeks[row][1], payrollweeks[row][2]]
                print(cur_payrollwk)
                dbconn.execute(queries.leave_increment(),(week,))
                leave_increment=dbconn.fetchall()
                for each in leave_increment:
                    dbconn.execute(queries.updateannualleavebalance(),(each[1],each[0]))
                dbconn.execute(queries.updatefortnight_toprocessed(),(1,1,week))
        dbconn.execute(queries.payrollweeks())
        payrollweeks=dbconn.fetchall()
        for r in approvednotpaidrequests:
            if r[2]==1:
                print(cur_payrollwk)
                if  r[4]<cur_payrollwk[0]:
                    dbconn.execute(queries.updateannualleavebalance(),(-r[11]*7.5,r[1]))
                    dbconn.execute(queries.updateleaverequestunpaidduration(),(-r[11],r[0]))
                    dbconn.execute(queries.updateapprovedrequesttopaid(),(1,r[0]))
                elif r[3]>cur_payrollwk[1]:
                    pass
                elif r[3]<cur_payrollwk[0] and r[4]>cur_payrollwk[1]:
                    dbconn.execute(queries.projected_leave_cost(),(cur_payrollwk[0],cur_payrollwk[1]))
                    cost=dbconn.fetchone()[0]
                    dbconn.execute(queries.updateannualleavebalance(),(-int(cost)*7.5,r[1]))
                    dbconn.execute(queries.updateleaverequestunpaidduration(),(-int(cost),r[0]))
                    dbconn.execute(queries.updateapprovedrequesttopaid(),(2,r[0]))
                elif r[3]<cur_payrollwk[0] and r[4]<=cur_payrollwk[1]:
                    dbconn.execute(queries.projected_leave_cost(),(cur_payrollwk[0],r[4]))
                    cost=dbconn.fetchone()[0]
                    hours=float(cost)*7.5
                    dbconn.execute(queries.updateannualleavebalance(),(-hours,r[1]))
                    dbconn.execute(queries.updateleaverequestunpaidduration(),(-int(cost),r[0]))
                    dbconn.execute(queries.updateapprovedrequesttopaid(),(1,r[0]))
                elif r[3]>=cur_payrollwk[0] and r[4]<=cur_payrollwk[1]:
                    dbconn.execute(queries.updateannualleavebalance(),(-r[11]*7.5,r[1]))
                    dbconn.execute(queries.updateleaverequestunpaidduration(),(-r[11],r[0]))
                    dbconn.execute(queries.updateapprovedrequesttopaid(),(1,r[0]))
                elif r[3]>=cur_payrollwk[0] and r[4]>cur_payrollwk[1]:
                    dbconn.execute(queries.projected_leave_cost(),(r[3],cur_payrollwk[1]))
                    cost=dbconn.fetchone()[0]
                    dbconn.execute(queries.updateannualleavebalance(),(-int(cost)*7.5,r[1]))
                    dbconn.execute(queries.updateleaverequestunpaidduration(),(-int(cost),r[0]))
                    dbconn.execute(queries.updateapprovedrequesttopaid(),(2,r[0]))
            elif r[2]==2 or r[2]==6:
                if  r[4]<cur_payrollwk[0]:
                    dbconn.execute(queries.updatesickleavebalance(),(-r[11]*7.5,r[1]))
                    dbconn.execute(queries.updateleaverequestunpaidduration(),(-r[11],r[0]))
                    dbconn.execute(queries.updateapprovedrequesttopaid(),(1,r[0]))
                elif r[3]>cur_payrollwk[1]:
                    pass
                elif r[3]<cur_payrollwk[0] and r[4]>cur_payrollwk[1]:
                    dbconn.execute(queries.projected_leave_cost(),(cur_payrollwk[0],cur_payrollwk[1]))
                    cost=dbconn.fetchone()[0]
                    dbconn.execute(queries.updatesickleavebalance(),(-int(cost)*7.5,r[1]))
                    dbconn.execute(queries.updateleaverequestunpaidduration(),(-int(cost),r[0]))
                    dbconn.execute(queries.updateapprovedrequesttopaid(),(2,r[0]))
                elif r[3]<cur_payrollwk[0] and r[4]<=cur_payrollwk[1]:
                    dbconn.execute(queries.projected_leave_cost(),(cur_payrollwk[0],r[4]))
                    print(cur_payrollwk[0],r[4])
                    cost=dbconn.fetchone()[0]
                    hours=float(cost)*7.5
                    dbconn.execute(queries.updatesickleavebalance(),(-hours,r[1]))
                    dbconn.execute(queries.updateleaverequestunpaidduration(),(-int(cost),r[0]))
                    dbconn.execute(queries.updateapprovedrequesttopaid(),(1,r[0]))
                elif r[3]>=cur_payrollwk[0] and r[4]<=cur_payrollwk[1]:
                    dbconn.execute(queries.updatesickleavebalance(),(-r[11]*7.5,r[1]))
                    dbconn.execute(queries.updateleaverequestunpaidduration(),(-r[11],r[0]))
                    dbconn.execute(queries.updateapprovedrequesttopaid(),(1,r[0]))
                elif r[3]>=cur_payrollwk[0] and r[4]>cur_payrollwk[1]:
                    dbconn.execute(queries.projected_leave_cost(),(r[3],cur_payrollwk[1]))
                    cost=dbconn.fetchone()[0]
                    print(r[3],cur_payrollwk[1])
                    dbconn.execute(queries.updatesickleavebalance(),(-int(cost)*7.5,r[1]))
                    dbconn.execute(queries.updateleaverequestunpaidduration(),(-int(cost),r[0]))
                    dbconn.execute(queries.updateapprovedrequesttopaid(),(2,r[0]))

    for row in range(len(payrollweeks)):
        if payrollweeks[row][3] == 1:
            payrollweeks[row] = (*payrollweeks[row], 'Processed')
        elif payrollweeks[row][3] == 0 and payrollweeks[row][2] < today:
            payrollweeks[row] = (*payrollweeks[row], 'To be Processed')
        elif payrollweeks[row][1] <= today and payrollweeks[row][2] >= today:
            payrollweeks[row] = (*payrollweeks[row], 'Up Coming Fortnight')
        else:
            payrollweeks[row] = (*payrollweeks[row], 'Future')

    dbconn.execute(queries.countpendingapproval())
    countpendingapproval=dbconn.fetchall()
    countpendingapproval_dict=dict(countpendingapproval)

    dbconn.execute(queries.leavebalance_all())
    leaveBalance_all = dbconn.fetchall()

    return render_template("payrolladdbalance.html", title="Update Balance", 
                           session=session, 
                           leaveBalance_all=leaveBalance_all,
                           payrollweeks=payrollweeks,
                           countpendingapproval_dict=countpendingapproval_dict)


@app.route('/requestleave', methods=["GET", "POST"])
def RequestLeave():
  # connect to the database
    dbconn = getCursor()
    # query the database for the leave balance
    # fetch one record and return result

    return render_template("requestleave.html", title="Request Leave", session=session)


@app.route('/projectedLeaveBalance',methods=["GET", "POST"])
def projectedLeaveBalance():
    if request.method == 'POST':
        # connect to the database
        dbconn = getCursor()
        # query the database for the leave balance
        dbconn.execute(queries.leavebalance(), (session['id'],))
        leaveBalance=dbconn.fetchone()
        annualHours = leaveBalance[3]
        if annualHours is not None:
            annualDays=round((float(annualHours)/7.5), 2)
        else:
            annualDays=0
            annualHours=0  
            
        # Get projected_date from HTML form
        projected_date = request.form['projected_date']    
        # Convert the string representations to datetime.date objects
        projected_date = datetime.datetime.strptime(projected_date, "%Y-%m-%d").date()
        # query the database for latest payroll_day
        dbconn.execute(queries.payroll_day(), (session['id'],))
        payroll_day=dbconn.fetchone()[0]
        # query the database for unpaid leave request start date
        dbconn.execute(queries.annualleave_unpaid_start_day(), (session['id'],))
        result=dbconn.fetchone()
        # handle the case when there are no results from the database query.
        unpaid_start_date=result[1] if result else None
        # query the database for unpaid leave request end date
        dbconn.execute(queries.annualleave_unpaid_end_day(), (session['id'],))
        result=dbconn.fetchone()
        # handle the case when there are no results from the database query.
        unpaid_end_date=result[1] if result else None
          
        # check if each date is not None
        if unpaid_start_date is not None and unpaid_end_date is not None:
            # compare start_date, end_date, payroll_day and projected_date to get the correct unpaidleave during projected period.
            if unpaid_start_date > payroll_day and unpaid_end_date <= projected_date:
                dbconn.execute(queries.projected_leave_cost(), (unpaid_start_date, unpaid_end_date))
                unpaidAnnualDays = dbconn.fetchone()[0]
            elif unpaid_start_date > payroll_day and unpaid_end_date > projected_date:
                dbconn.execute(queries.projected_leave_cost(), (unpaid_start_date, projected_date))
                unpaidAnnualDays = dbconn.fetchone()[0]
            elif unpaid_start_date <= payroll_day and unpaid_end_date <= projected_date:
                dbconn.execute(queries.projected_leave_cost(), (payroll_day, unpaid_end_date))
                unpaidAnnualDays = dbconn.fetchone()[0]
            elif unpaid_start_date <= payroll_day and unpaid_end_date > projected_date:
                dbconn.execute(queries.projected_leave_cost(), (payroll_day, projected_date))
                unpaidAnnualDays = dbconn.fetchone()[0]            
            else:
                unpaidAnnualDays=0
        else:
            unpaidAnnualDays=0
        # handle Nonetype for unpaidAnnualDays    
        if unpaidAnnualDays is not None:
            annual_unpaidHours=round((float(unpaidAnnualDays)*7.5), 2)
        else:
            unpaidAnnualDays=0
            annual_unpaidHours=0

        # query the database for unapproved leave request start date
        dbconn.execute(queries.annualleave_unapproved_start_day(), (session['id'],))
        result=dbconn.fetchone()
        # handle the case when there are no results from the database query.
        unapproved_start_date=result[1] if result else None
        # query the database for unapproved leave request end date
        dbconn.execute(queries.annualleave_unapproved_end_day(), (session['id'],))
        result=dbconn.fetchone()
        # handle the case when there are no results from the database query.
        unapproved_end_date=result[1] if result else None
        print(unapproved_start_date)
        print(unapproved_end_date)

        # check if each date is not None
        if unapproved_start_date is not None and unapproved_end_date is not None:
            # compare start_date, end_date, payroll day and projected_date to get the correct unapprovedleave during projected period.
            if unapproved_start_date > payroll_day and unapproved_end_date <= projected_date:
                dbconn.execute(queries.projected_leave_cost(), (unapproved_start_date, unapproved_end_date))
                unapprovedAnnualDays = dbconn.fetchone()[0]
            elif unapproved_start_date > payroll_day and unapproved_end_date > projected_date:
                dbconn.execute(queries.projected_leave_cost(), (unapproved_start_date, projected_date))
                unapprovedAnnualDays = dbconn.fetchone()[0]
            elif unapproved_start_date <= payroll_day and unapproved_end_date > projected_date:
                dbconn.execute(queries.projected_leave_cost(), (payroll_day, projected_date))
                unapprovedAnnualDays = dbconn.fetchone()[0]
            elif unapproved_start_date <= payroll_day and unapproved_end_date <= projected_date:
                dbconn.execute(queries.projected_leave_cost(), (payroll_day, unapproved_end_date))
                unapprovedAnnualDays = dbconn.fetchone()[0]
            else:
                unapprovedAnnualDays=0
        else:
            unapprovedAnnualDays=0    
        
        # handle Nonetype of UnapprovedAnuualDays
        if unapprovedAnnualDays is not None:
            annual_unapprovedHours=round((float(unapprovedAnnualDays)*7.5), 2)
        else:
            unapprovedAnnualDays=0
            annual_unapprovedHours=0

        # query the database for the leave Accrued during projected period (projected_day - payroll_day)
        dbconn.execute(queries.projected_leave_cost(), (payroll_day, projected_date))
        # fetch one record and return result
        projected_days = dbconn.fetchone()[0]
        # calculate projected accrual to projected date.
        projected_accrualdays = round(float(projected_days)*1.15/14, 2)
        projected_accrualhours = round(projected_accrualdays * 7.5, 2)
        # calculate estimated projected leave balance.
        estimated_days = annualDays + projected_accrualdays - float(unapprovedAnnualDays) - float(unpaidAnnualDays)
        estimated_days = round(estimated_days, 2)
        estimated_hours = round(estimated_days*7.5, 2)
        # convert projected_date to NZ date format
        projected_date=projected_date.strftime("%d %B %Y")
        return render_template("projectedLeaveBalance.html", 
                               title="Projected Leave Balance", 
                               leaveBalance=leaveBalance,
                               annualHours=annualHours,
                               annualDays=annualDays,
                               annual_unapprovedHours=annual_unapprovedHours,
                               unapprovedAnnualDays= unapprovedAnnualDays,
                               annual_unpaidHours = annual_unpaidHours,
                               unpaidAnnualDays=unpaidAnnualDays,
                               projected_date=projected_date,
                               projected_accrualdays=projected_accrualdays,
                               projected_accrualhours=projected_accrualhours,
                               estimated_days=estimated_days, 
                               estimated_hours=estimated_hours, 
                               session=session)
    #connect to the database
    dbconn = getCursor()
    # query the database for the leave balance
    dbconn.execute(queries.leavebalance(), (session['id'],))
    # fetch one record and return result
    leaveBalance = dbconn.fetchone()
    annualDays = float(leaveBalance[3]) / 7.5
    AnnualDaysDisplay= round( annualDays, 2)   
    return render_template("projectedLeaveBalance.html", title="My Projected Leave Balance", AnnualDaysDisplay=AnnualDaysDisplay, leaveBalance=leaveBalance, session=session)




@app.route('/applyLeave', methods=['GET'])
def applyLeave():

    request_uid = session["id"]

    startdate_today=today_string
    startdate_today=startdate_today[5:7]+"/"+startdate_today[-2:]+"/"+startdate_today[:4]
    uid=request.args.get('uid')
    edit_mode=request.args.get('edit')
    edit_rid=request.args.get('rid')
    edit_type=request.args.get('type')
    edit_start=request.args.get('start')
    edit_end=request.args.get('end')
    previous_url=request.args.get('purl')
    edit_comment=""
    edit_request=()
    
    annualDays=0

    dbconn = getCursor()

    if(edit_mode=="1"):
        edit_start=edit_start[5:7]+"/"+edit_start[-2:]+"/"+edit_start[:4]
        edit_end=edit_end[5:7]+"/"+edit_end[-2:]+"/"+edit_end[:4]
        dbconn.execute(queries.draftleave(), (edit_rid,))
        dbconn.execute(queries.editleave_select(), (edit_rid,))
        edit_request = dbconn.fetchall()
        edit_comment = edit_request[0][10]
        request_uid = edit_request[0][0]

    # query the database for the employee's name
    dbconn.execute(queries.userdetail(), (request_uid,))
    # fetch one record and return result
    detail = dbconn.fetchone()
     # query the database for leave types
    dbconn.execute(queries.leave_types())
    leaveTypes= dbconn.fetchall()
    dbconn.execute(queries.calendarholidays())
    calendarHolidays= dbconn.fetchall()
    dbconn.execute(queries.approvedleavec(), (request_uid,))
    approvedLeaveC= dbconn.fetchall()
    dbconn.execute(queries.pendingleavec(), (request_uid,))
    pendingLeaveC= dbconn.fetchall()
    dbconn.execute(queries.allrequests_nodraft(), (request_uid,))
    allRequests= dbconn.fetchall()
    dbconn = getCursor()
    # query the database for the leave balance
    dbconn.execute(queries.leavebalance(), (request_uid,))
    # fetch one record and return result
    leaveBalance = dbconn.fetchone()
    if annualDays is not None:
        annualDays=(float(leaveBalance[3])/7.5)
        AnnualDaysDisplay= round(annualDays, 2)
    if annualDays is not None:
        AnnualDaysDisplay=round(annualDays, 2)
    else:
        AnnualDaysDisplay=0
    sickDays=(float(leaveBalance[4])/7.5)
    sickDaysDisplay= round( sickDays, 2)
    if sickDays is not None:
        sickDaysDisplay=round(sickDays, 2)
    else:
        sickDaysDisplay=0
    print(approvedLeaveC)

    return render_template("applyLeave.html", 
                        leaveBalance=leaveBalance, 
                        AnnualDaysDisplay=AnnualDaysDisplay, 
                        sickDaysDisplay=sickDaysDisplay,  
                        allRequests=allRequests, 
                        approvedLeaveC=approvedLeaveC, 
                        pendingLeaveC=pendingLeaveC, 
                        calendarHolidays=calendarHolidays, 
                        leaveTypes=leaveTypes, 
                        detail=detail, 
                        edit_mode=edit_mode,
                        edit_rid=edit_rid,
                        edit_type=edit_type,
                        edit_start=edit_start,
                        edit_end=edit_end,
                        edit_comment=edit_comment,
                        edit_request=edit_request,
                        startdate_today=startdate_today,
                        title="Apply for Leave", 
                        session=session,
                        previous_url=previous_url
                        )

@app.route('/calculate', methods=['POST'])
def calculate():
    startDate = request.json['startDate']
    endDate = request.json['endDate']
    print(startDate)
    print(endDate)

    # Perform the calculation based on the start and end dates
    result = perform_calculation(startDate, endDate)
    result=(f"You are applying for {result[0]} days or {result[1]} hours of leave")
    # Return the result as JSON
    return jsonify(result=result)

def perform_calculation(startDate, endDate):
    # Query the database and calculate the result based on the start and end dates
    # ...

    start__Date = startDate.replace('/', '-')
    # Split the date string by '-'
    month, day, year = start__Date.split('-')
    # Reformat the date string
    startDate = f"{year}-{month}-{day}"
    end__Date = endDate.replace('/', '-')
    # Split the date string by '-'
    month, day, year = end__Date.split('-')
    # Reformat the date string
    endDate = f"{year}-{month}-{day}"
    dbconn = getCursor()
    dbconn.execute(queries.leavedays(), (startDate, endDate,))
    leaveDays=float(dbconn.fetchall()[0][0])
    leaveHours=float(leaveDays)*7.5
   
   
    return (leaveDays, leaveHours)
@app.route('/leaveConfirm',methods=["GET", "POST"])
def leaveConfirm():
    request_uid=request.form.get("request_uid")
    edit_mode=request.form.get("edit_mode")
    edit_rid=request.form.get("edit_rid")
    previous_url=request.form.get("previous_url")
    print(previous_url)

    leaveTypes=request.form.get("leaveTypes")
    start_date=request.form.get("start_date")
    # Convert the date format to 'yyyy-mm-dd'
    start__Date = start_date.replace('/', '-')
    # Split the date string by '-'
    month, day, year = start__Date.split('-')
    # Reformat the date string
    startDate = f"{year}-{month}-{day}"
    end_Date=request.form.get("end_date")
    end__Date = end_Date.replace('/', '-')
    # Split the date string by '-'
    month, day, year = end__Date.split('-')
    # Reformat the date string
    endDate = f"{year}-{month}-{day}"
    comments=request.form.get("comments")
    dbconn = getCursor()
    dbconn.execute(queries.leavedays(), (startDate, endDate,))
    leaveDays=dbconn.fetchall()
    leaveHours=leaveDays[0][0]*Decimal(str(7.5))
    dbconn.execute(queries.leavebalance(), (request_uid,))
    # fetch one record and return result
    leaveBalance = dbconn.fetchone()
    annualDays=(float(leaveBalance[3])/7.5)
    AnnualDaysDisplay= round(annualDays, 2)
    if annualDays is not None:
        AnnualDaysDisplay=round(annualDays, 2)
    else:
        AnnualDaysDisplay=0
    sickDays=(float(leaveBalance[4])/7.5)
    sickDaysDisplay= round( sickDays, 2)
    if sickDays is not None:
        sickDaysDisplay=round(sickDays, 2)
    else:
        sickDaysDisplay=0
    
    if request.method == 'POST':
        # connect to the database
        dbconn = getCursor()
        # query the database for the leave balance
        dbconn.execute(queries.leavebalance(), (request_uid,))
        leaveBalance=dbconn.fetchone()
        annualHours = leaveBalance[3]
        if annualHours is not None:
            annualDays=round((float(annualHours)/7.5), 2)
        else:
            annualDays=0
            annualHours=0
        dbconn.execute(queries.annualleavebalance_unapproved(), (request_uid,))
        unapprovedAnnualDays = dbconn.fetchone()[1]
        if unapprovedAnnualDays is not None:
            annual_unapprovedHours=round((float(unapprovedAnnualDays)*7.5), 2)
        else:
            annual_unapprovedHours=0
            unapprovedAnnualDays=0        
        dbconn.execute(queries.annualleavebalance_unpaid(), (request_uid,))
        unpaidAnnualDays = dbconn.fetchone()[1]
        if unpaidAnnualDays is not None:
            annual_unpaidHours=round((float(unpaidAnnualDays)*7.5), 2)
        else:
            unpaidAnnualDays=0
            annual_unpaidHours=0
          
    dbconn.execute(queries.payroll_day(), (request_uid,))
    payroll_day=dbconn.fetchone()[0]
    end_year, end_month, end_day = map(int, endDate.split('-'))
    end__Date = datetime.date(end_year, end_month, end_day)
    if payroll_day <= end__Date:
        # query the database for the leave Accrued during projected period (projected_day - payroll_day)
        dbconn.execute(queries.projected_leave_cost(), (payroll_day, end__Date))
        # fetch one record and return result
        projected_days = dbconn.fetchone()[0]
        projected_accrualdays = round(float(projected_days)*1.15/14, 2)
        projected_accrualhours = round(projected_accrualdays * 7.5, 2)
        # calculate estimated projected leave balance.
        estimated_days = annualDays + projected_accrualdays - float(unapprovedAnnualDays) -float(unpaidAnnualDays)
        estimated_days = round(estimated_days, 2)
        estimated_hours = round(estimated_days*7.5, 2)

        # convert projected_date to NZ date format
        date_obj = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        projected_date=date_obj.strftime("%d %B %Y")
    else:
        projected_date="last payroll day"
        estimated_days = AnnualDaysDisplay
        estimated_hours = leaveBalance[3]
    # query the database for all leave requests
    dbconn.execute(queries.requestsdate_nodraft(), (request_uid,))
    requestsDate= dbconn.fetchall()
    # Convert the result to JSON
    json_result = json.dumps(requestsDate, cls=DateEncoder)
    

    

    return render_template("leaveConfirm.html", leaveBalance=leaveBalance, 
            estimated_days=estimated_days, estimated_hours=estimated_hours,
            projected_date=projected_date, payroll_day=payroll_day, end__Date=end__Date,
            startDate=startDate, endDate=endDate, requestsDate=requestsDate,
            comments=comments, sickDaysDisplay=sickDaysDisplay, 
            AnnualDaysDisplay=AnnualDaysDisplay, leaveHours=leaveHours, 
            leaveTypes=leaveTypes, leaveDays=leaveDays, json_result=json_result,
            request_uid=request_uid, edit_mode=edit_mode,edit_rid=edit_rid,previous_url=previous_url)


@app.route('/leaveRequests',methods=["GET", "POST"])
def leaveRequests():
    # connect to the database
    dbconn = getCursor()
    if request.method == 'POST':
        # If POST method, fetch status from HTML form.
        status = request.form['status']
        if status:
            # If filter by one status, query from database to get data for this status.
            dbconn.execute(queries.leave_requests_status(), (session["id"],status))
            leaveRequestsStatus = dbconn.fetchall()
            return render_template("leaveRequests.html", leaveRequestsStatus=leaveRequestsStatus, title="Leave Requests", session=session)    
        else:
            # All data will be feched from database if user not filter any status.
            dbconn.execute(queries.leave_requests(), (session["id"],))
            leaveRequests = dbconn.fetchall()
            return render_template("leaveRequests.html", leaveRequests=leaveRequests, title="Leave Requests", session=session)
    uid=request.args.get('uid')
    rid=request.args.get('rid')
    withdraw=request.args.get('withdraw')
    if withdraw=="1" and int(uid)==session["id"]:
        print("delete")
        dbconn.execute(queries.withdrawleave(), (int(rid),))
    # On GET method, all leave requests data been fetched from database and transfered to front-end.
    dbconn.execute(queries.leave_requests(), (session["id"],))
    leaveRequests = dbconn.fetchall()
    return render_template("leaveRequests.html", leaveRequests=leaveRequests, title="Leave Requests", session=session)



@app.route('/leaveSubmit',methods=["GET", "POST"])
def leaveSubmit():
    # retrieve all user input value 
    edit_mode=request.form.get("edit_mode_input")
    print("edit_mode:",edit_mode)

    if edit_mode == "1":
        request_uid=request.form.get("request_uid")
        edit_rid=request.form.get("edit_rid")
        previous_url=request.form.get("previous_url")
        print("edit_rid",edit_rid)
        employee_id = request_uid
    else:
        employee_id=session['id']
    
    start_date=request.form.get("startDate")
    end_date=request.form.get("endDate")
    leaveDays=request.form.get("leaveDays")
    if len(leaveDays) == 17:
        leaveDays=leaveDays[11]
    elif len(leaveDays) == 18:
        print("leavedays",leaveDays[11:13])
        leaveDays=leaveDays[11:13]
    comments=request.form.get("comments")
    # retrieve  manager id and leae type id from database
    dbconn = getCursor()
    dbconn.execute(queries.getmanagerid(), (employee_id,))
    manager_id = dbconn.fetchall()[0][0]
    leaveTypes=request.form.get("leaveTypes")
    if leaveTypes == "Annual" or leaveTypes ==  "Sick" or leaveTypes == "Bereavement" or leaveTypes == "Unpaid":
        leavetype= f"{leaveTypes} Leave"
    elif leaveTypes == "Special":
        leavetype= f"{leaveTypes} Leave with Pay"
    else:
        leavetype= f"{leaveTypes}"
    dbconn = getCursor()
    dbconn.execute(queries.getleavetype(), (leavetype,))
    leave_type = dbconn.fetchone()[0]
    print(leave_type)
    
    #update all info in database
    dbconn = getCursor()

    if edit_mode == "1":
        dbconn.execute(queries.leaveupdate(), (leave_type, start_date,end_date , comments, leaveDays,leaveDays, edit_rid))
    else:
        dbconn.execute(queries.leavesubmit(), (employee_id, leave_type, start_date,end_date, manager_id , comments, leaveDays,leaveDays ))
    # Retrieve the ID of the last inserted row
    last_row_id = dbconn.lastrowid

    # Execute a SELECT query to retrieve the recently inserted row
    select_query = "select * from leave_request where request_id = %s"
    dbconn.execute(select_query, (last_row_id,))

    # Fetch the row
    submitDetails = dbconn.fetchone()

    if edit_mode == "1":
        print("redirect to ",previous_url)
        return redirect(previous_url)
    else:
        return redirect(url_for("applyLeave", submitDetails=submitDetails))

@app.route('/orgchart', methods=["GET"])
def orgchart():

    dbconn = getCursor()
    
    dbconn.execute(queries.allemployee_orgchart())
    allemployee_orgchart = dbconn.fetchall()

    allemployee_orgchart_tuple = ()
    for i in allemployee_orgchart:
        t = (i[0],i)
        allemployee_orgchart_tuple = (*allemployee_orgchart_tuple, t)
    
    allemployee_orgchart_dict=dict(allemployee_orgchart_tuple)

    uid=1
    uid_s = uid
    uid_m = uid
    uid_dr = uid

    supervisor_list = []
    manager_list = []
    directreport_manager = ()
    directreport_supervisor = ()

    supervisor = allemployee_orgchart_dict[uid][1]
    manager =  allemployee_orgchart_dict[uid][2]

    orgchart_supervisor= {}
    orgchart_manager= {}

    while supervisor not in supervisor_list:
        supervisor_list.append(uid_s)
        supervisor = allemployee_orgchart_dict[uid_s][1]
        uid_s=int(allemployee_orgchart_dict[uid_s][1])
    supervisor_list.reverse()


    while manager not in manager_list:
        manager_list.append(uid_m)
        manager = allemployee_orgchart_dict[uid_m][2]
        uid_m=int(allemployee_orgchart_dict[uid_m][2])
    manager_list.reverse()

    for i in allemployee_orgchart:
        manager_dr=i[2]
        supervisor_dr=i[1]
        if manager_dr == uid:
            directreport_manager=(*directreport_manager,i[0])
        if supervisor_dr == uid:
            directreport_supervisor=(*directreport_supervisor,i[0])
    
    for x in allemployee_orgchart:
        dr_manager = ()
        dr_supervisor = ()
        for y in allemployee_orgchart:
            manager_dr=y[2]
            supervisor_dr=y[1]
            if manager_dr == x[0]:
                dr_manager=(*dr_manager,y[0])
            if supervisor_dr == x[0]:
                dr_supervisor=(*dr_supervisor,y[0])
        orgchart_manager[x[0]]=dr_manager
        orgchart_supervisor[x[0]]=dr_supervisor
  
    print(orgchart_manager)
    
    return render_template("orgchart.html", title="Org Chart", 
                           allemployee_orgchart_dict=allemployee_orgchart_dict,
                           supervisor_list=supervisor_list,
                           manager_list=manager_list,
                           directreport_manager=directreport_manager,
                           directreport_supervisor=directreport_supervisor,
                           orgchart_manager=orgchart_manager,
                           orgchart_supervisor=orgchart_supervisor
                           )

@app.route('/fullcalendar', methods=["GET"])
def full_calendar():

    uid=session['id']

    dbconn = getCursor()

    dbconn.execute(queries.dept_emp_leaverequests(), (uid,))
    dept_emp_leaverequests = dbconn.fetchall()

    dbconn.execute(queries.emp_in_department(), (uid,))
    emp_in_department = dbconn.fetchall()

    dept_leaverequest = ()

    for e in emp_in_department:
        dbconn.execute(queries.emp_leaverequests(), (e[0],))
        emp_leaverequests = dbconn.fetchall()
        dbconn.execute(queries.dateforcalendar())
        dateforcalendar = dbconn.fetchall()
        for i in range(len(dateforcalendar)):
            for x in emp_leaverequests:
                if x[3]<=dateforcalendar[i][0] and x[4]>=dateforcalendar[i][0]:
                    dateforcalendar[i] = (*dateforcalendar[i], x[2])
            if dateforcalendar[i][2] == 1:
                dateforcalendar[i] = (*dateforcalendar[i],'Holiday')
            elif dateforcalendar[i][1] == 6 or dateforcalendar[i][1]==7:
                dateforcalendar[i] = (*dateforcalendar[i],'Weekend')
            elif len(dateforcalendar[i]) < 4:
                dateforcalendar[i] = (*dateforcalendar[i],'Available')
        dept_leaverequest = (*dept_leaverequest, (e[0], dateforcalendar))
    dept_leaverequest_dict = dict(dept_leaverequest)
    
    emp_dict = {}
    emp_list = []
    emp_in_department_tuple = ()
    for x in emp_in_department:
        t = (x[0],x)
        emp_list.append(x[0])
        emp_in_department_tuple = (*emp_in_department_tuple, t)
    emp_dict = dict(emp_in_department_tuple)



    return render_template("fullcalendar.html", title="Full Calendar",
                           dateforcalendar=dateforcalendar,
                           dept_emp_leaverequests=dept_emp_leaverequests,
                           emp_dict=emp_dict,
                           dept_leaverequest_dict=dept_leaverequest_dict)

    
@app.route('/admin/leaveTypes', methods=["GET", "POST"])
def leaveTypes():
     # query the database for all leave types
    dbconn = getCursor()
    dbconn.execute(queries.allleavetypes())
    leave_type = dbconn.fetchall()
    # query the database for the employee's name
    dbconn.execute(queries.userdetail(), (session["id"],))
    # fetch one record and return result
    detail = dbconn.fetchone()
    
    #get leave type and discription from input
    new_leave_name = request.form.get("leaveName")
    new_leave_description = request.form.get("leaveDescription")
    if new_leave_description:
        new_leave_description = new_leave_description
    else:
        new_leave_description = "No description"
    if new_leave_name:
            # update the added leave type
            dbconn = getCursor()
            dbconn.execute(queries.addtype(), (new_leave_name, new_leave_description, ))
            dbconn.execute(queries.allleavetypes())
            leave_type = dbconn.fetchall()
            return render_template("leaveTypes.html", detail=detail, leave_type=leave_type)
    # delete leave types
    deleted_leaveID = request.form.get("deleted_leaveID")
    if deleted_leaveID:
        dbconn = getCursor()
        dbconn.execute(queries.deletetype(), (deleted_leaveID, ))
        dbconn.execute(queries.allleavetypes())
        leave_type = dbconn.fetchall()
        return render_template("leaveTypes.html", detail=detail, leave_type=leave_type)
    #edit leave types
    leave_ID = request.form.get("leave_ID")
    editName=request.form.get("editName")
    editDescription=request.form.get("editDescription")
    if editName:
        dbconn = getCursor()
        dbconn.execute(queries.edittype(), (editName, editDescription,leave_ID,))
        dbconn.execute(queries.allleavetypes())
        leave_type = dbconn.fetchall()
        return render_template("leaveTypes.html", detail=detail, leave_type=leave_type)

    
    return render_template("leaveTypes.html", detail=detail, leave_type=leave_type)

@app.route('/admin/roles', methods=["GET", "POST"])
def change_roles():
    # if the user submits the form to change the employee's role
    if request.method == "POST":
        # get the employee's id and their new role
        employee_id = request.form.get("employee_id")
        print(employee_id)
        role_id = request.form.get("role_id")
        print(role_id)
        # update the employee's role
        dbconn = getCursor()
        dbconn.execute(queries.update_role(), (role_id, employee_id))
        dbconn.close()
        return redirect(request.referrer)

     # query the database for all employees and their roles
    dbconn = getCursor()
    dbconn.execute(queries.roles())
    roles = dbconn.fetchall()
        # query the database for role types
    dbconn.execute(queries.roleTypes())
    roleTypes = dbconn.fetchall()
    return render_template("roles.html", roles=roles, roleTypes=roleTypes, title="Admin Edit Roles", session=session)


@app.route('/admin_holiday', methods=["GET", "POST"])
def manage_holiday():

    search_year=request.args.get('year')
    if search_year is not None:
        search_year=int(search_year)
    holiday_id=request.args.get('hid')
    if holiday_id is not None:
        holiday_id=int(holiday_id)
    d=request.args.get('d')
    holiday_desc=request.args.get('desc')
    holiday_eligibility=request.args.get('e')
    delete=request.args.get('delete')
    edit=request.args.get('edit')
    update=request.args.get('update')

    id_update = request.form.get("id")
    date_update = request.form.get("date")
    description_update = request.form.get("description")
    eligibility_update = request.form.get("eligibility")

    date_new = request.form.get("newdate")
    description_new = request.form.get("newdescription")
    eligibility_new = request.form.get("neweligibility")

    print(id_update, date_update,description_update,eligibility_update)

    dbconn = getCursor()

    if date_update is not None:
        date_update = datetime.datetime.strptime(date_update, "%d-%m-%Y")
        print(date_update)
        dbconn.execute(queries.update_holiday(), (date_update,description_update,eligibility_update,id_update))

    if delete is not None:
        dbconn.execute(queries.delete_holiday(), (holiday_id,))

    if date_new is not None:
        dbconn.execute(queries.add_holiday(), (date_new,description_new,eligibility_new))

    dbconn.execute(queries.check_holiday(), (search_year,))
    check_holiday = dbconn.fetchall()

    return render_template("admin_holiday.html", title="Manage Holiday",
                           check_holiday=check_holiday,
                           search_year=search_year,
                           holiday_id=holiday_id)

@app.route('/sickleave', methods=["GET", "POST"])
def check_sickleave():

    dbconn = getCursor()
    dbconn.execute(queries.emp_anniversary())
    emp_anniversary = dbconn.fetchall()
    Message = ""
    

    for e in emp_anniversary:
        if e[1].month == today.month and e[1].day == today.day:
            if e[2] is None:
                dbconn.execute(queries.reset_sickleavebalance(),(e[0],))
                Message += str(("Sick Leave Reset to 37.5 for uid ",(e[0])))
            elif e[2] < e[1]:
                dbconn.execute(queries.reset_sickleavebalance(),(e[0],))
                Message += str(("Sick Leave Reset to 37.5 for uid ",(e[0])))
            else:
                Message += str(("Sick Leave had already been reset to 37.5 for uid ",(e[0])," on ", (e[2]),". There's no need to reset again. "))

    if Message == "":      
        Message += str(("No employee on work anniversary today."))

    return Message


@app.route('/changePassword', methods=["GET", "POST"])
def changePassword():
    msg=''
    dbconn = getCursor()
    if request.method == "POST" and 'old-password' in request.form and 'new-password' in request.form and 'confirm-password' in request.form:
        old_password=request.form.get("old-password")
        print(old_password)
        dbconn.execute(queries.user(), (session['id'], ))
        employee= dbconn.fetchone()
        passworddB=employee[5]
        print(passworddB)
        if bcrypt.checkpw(old_password.encode('utf-8'),passworddB.encode('utf-8')):
            new_password=request.form.get("new-password")
            confirm_password=request.form.get("confirm-password")
            if new_password == confirm_password:
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                print(hashed)
                dbconn.execute(queries.change_password(), (hashed, session['id'], ))
                confirm_msg = 'Your password has been changed successfully!'
                return render_template("changePassword.html", confirm_msg=confirm_msg, title="Change Password",)            
            else:
                msg="The confirmation password does not match"
        else:
            msg='Old password not correct'
    return render_template("changePassword.html", msg=msg, title="Change Password",)
    
    
