the decision to have the role type choice within the html saves on duplicating code across multiple templates and allows us to easily customize the dashboard content for different employee types
still dont have the bcrypt working 
database added to project2
23/05/03 BLW I have now got the login page working and the database connected ..now to send it somewhere.. have had two days of going around in circles with database not connecting and then playing with the bcrypt before i had the login working ... 
23/05/03 BLW now the login page works up until it gets the employees details from the database - currently i am returning only employee_id and role_id 
23/05/03 BLW bcrypt password checking is now working yay
23/05/03 BLW password incorrect testing works and message returns in login page to try again
23/05/03 BLW now all testing complete on log in page and even session works .. incorrect password incorrect email and correct both all work as they should - now to split out the dashboard landing pages
23/05/03 BLW added more employees with different roles to test login and dashboard landing page
23/05/03 BLW i couldnt work out how to pass in an employee only without assigning employee as a role so i have added employee role to the databse now - happy to revert if someone knows how to do it better
23/05/03 BLW so all logins land on employee page - need to work on how to get admin or approval manager to work - shall we consider different dashboards? answer no better for reuseability - team vote
23/05/04 BLW finally got the role choice working for the login welcome - removing the quotation marks around the role number - sessions working too just noeed to do logout
23/05/04 BLW completed some css and the logout button is working now

23/05/04 HD added Flow Chart
https://miro.com/app/board/uXjVMNudBvw=/

23/05/05 BLW outside user testing: edited the incorrect login message since stating "incorrect email" or "incorrect password" could potentially help hackers 
23/05/05 HD the original database design used AUTOINCREMENT on all ids for all entities on INSERT; the decision was made for the project to include the IDs in the insert statement because when we are trying to import data into database, auto increment won't always give us the same number in some cases and we are relying on the exact number to be reference on another table, we don't want to leave the ambiguity there to check after every rebuild. And also because when I design some of the data, I have a particular scenario that I want to test and observe. To have the id pre-defined, I can then find the record and select it. 
23/05/05 BLW have added the different buttons to the dashboard based off the MIRO chart with a suggested amendment awaiting team feedback for approval  - see github directory https://github.com/LUMasterOfAppliedComputing/comp639-2023-s1-project2-group3/blob/main/Resource/Belinda/MicrosoftTeams-image%20(2).png
23/05/05 put all the employee common buttons in the left panel and the extra buttons in the main container 
23/05/06 after discussion with Hido we need to change database leave request table to formate DATE not DATETIME as DATETIME calculation is way too complicated - Hido has added two more tables PAYROLL_PERIOD and
LEAVE_INCREMENT table 
23/05/07 make the left panel personal buttons only and the middle page for extra role buttons, moved the update leave balance to the centre - it needs to sit under the managememt button via a drop down menu as per the miro chart .. SS

# Database Design
## Table Design

### 04 May 23 - HD
#### Payroll Processed Flag on Leave Request Table
We need to add a new attribute to leave request table, which is "payroll processed". 
Every fortnight, when process payroll, 1. add increment, 2. process approved leave requests to update the leave balance table
In this way, we could identify leave requests that "new request, not approved" "request that approved but not processed by payroll" "request that approved and processed by payroll"

### 06 May 23 - HD
#### datatime format or date format
In my opinion, the date time format for start and end would be a problem in the future calculation. I suggest that we use date for start and end, then add a duration for calculation. Datetime calculation is way complicated compares to decimal calculation.


#### Payroll Period and Leave Increment
### 06 May 23 - HD
I have added two more tables.
### 08 May 23 - HD
Each payroll week is defined in db with primary key as "[Year]Wk[WeekNumber]", for example "2023Wk02".
As the increment of of leave balance is a fix number, we don't have to leave the calcuation when user request. For a given employee id, and also for a paticualr payroll fortnight, we can use a query to getthe fortnight annual leave increment.

```CREATE TABLE PAYROLL_PERIOD (
   payroll_period_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
   payroll_period_start DATETIME,
   payroll_period_end DATETIME,
   processed_by_payroll TINYINT DEFAULT FALSE
);

CREATE TABLE LEAVE_INCREMENT (
   leave_increment_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
   employee_id SMALLINT NOT NULL,
   leave_increment INT,
   payroll_period_id SMALLINT,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   CONSTRAINT LEAVE_INCREMENT_employee_id_FK FOREIGN KEY (employee_id) REFERENCES EMPLOYEE (employee_id),
   CONSTRAINT LEAVE_INCREMENT_payroll_period_id_FK FOREIGN KEY (payroll_period_id) REFERENCES PAYROLL_PERIOD (payroll_period_id)
);
```
### 06 May 23 - HD
#### Annual Leave fortnight increment
I was thinking how to add that fortnight increment to everyone. 
What to add, add to whom, how to achieve that. As it is a HR system, be'd better have kind of tracking history also

### 06 May 23 - HD
#### Leave cost
 Calculation or we can call validation I’d rather leave it at the moment submitting the leave. If the value that goes to the duration field is the value good to be used in aggregation with the leave balance, that would easier for all the steps that comes after.
 Use the query below, you could get the leave cost, considered weekends and holidays
```
SELECT SUM(leave_cost_day) FROM DATETABLE
WHERE date >= '2023-05-04' AND date <= '2023-05-08';
```

### 08 May 23 - HD
#### Decimal(6,2) Leave Balance
I have updated the leave balance hours to decimal(6,2) type in database.
In python, different from int, when aggregate the variable of decimal, we need to use "float" to add a bracket to avoid error. 

## Dummy Data
### 05 May 23 - HD
#### Insert ID in dummy data
It is because, when we are trying to import data into database, auto increment won't always give us the same number in some case.
It is because we are relying on the exact number to be reference on another table, I don't want to leave the ambiguity there to check after every rebuild.
And also because when I design some of the data, I have a particular scenario that I want to test and observe. To have the id pre-defined, I can then find the record and select it.
For example, we always want 5 to be the service department's id, it is because on the employee table, we have employee at department 5.
So when we insert data to the table, I don't want to leave it to the database to decide, which number should it assign for service department.
Use autoinc, most of the chance it would assign 5 as the id for service department, it is because that line of service department is happen to be the 5th line. 

### 08 May 23 - MT
Start working on view projected leave function for employee. It seems that our database did not contain sufficient data to support this feature. I have managed to calculate the projeted annual leave balance based on today's date. Also created a date picker for user to pick a day later than today. Will work on getting date of updating payroll day.

### 09 May 23 - MT
After discussing with the team and Product Owner, we decided to move view projected leave function to sprint 3, as this function need more data support.

### 23/05/10 - Miao
The current dashboard that I made in the prototype is quite disturbing, the RECENT and NOTIFICATIONS are similar in my eye. PO suggested we can have personal/approval manager/administrator for dashboard, but do admin need approval manager's notifications? As they might receive every new update from every employee, and don't need to do anything.
- edit the base.html to remove the drop sown menu.
### 23/05/10 - BLW
fixed logout button on dashboard side panel
added photo to login page
BLW Hido Miao had a meeting to discuss the new prototype and we discussed about displaying to the admin ALL the pending leave request for the entire uni - and decided that the admin is like the approval manager and only sees those that are delegated to him/her (shown on the dashboard) and sprint4  we will create another list to show them ALL ... but at the moment this will not show on the dashboard... 

### 10 May 23 - HD
#### Manager Page
Practice what learnt in the "How to structure flask project", I have created a separate manager.py and queries_manager.py for our project. The intention is to use these two files for routes and queries only relates to users who is approval manager.
> Discussion: In our code, we use if statement ```session['role_id'] == 2``` to check if the user logged in is a manager. If there's funtion that Admin shares with Manager, how about below? ```session['role_id'] < 3```
#### CSS
The page could not scroll up or down. After checked with Sherlyn, I removed ```overflow：hidden``` in CSS. Problem resolved.

### 10 May 23 - MT
Start working on the function of viewing leave requests for employee.Based on our prototype, we intended to fit the leave balance and leave requests onto a single page. However, I encountered difficulties in achieving this. I tried to use different CSS to fit these two parts together, but the result still not good, seems too much information on single page.

### 23/05/11 - BLW
Just tidied up CSS - removed large dashboard banner (I think it takes up too much room and looks garrish - my opinion only) - not sure why the logo disappears on the manager/myapproval page
have started my user story -display and view all my direct reports via the mydirect reports.html

### 11 May 23 - Miao
#### Prototype
- employee will have new button (under "My Leave") called **"All Leaves" or "Request Log"** Employee can view all historical Leaves that approved, rejected.
- For approval managers' dashboard, the top nav bar will change from "New requests" "All Employees" "Reports" to **"Request Log" "My Direct Reports" "Leave Reports"**
    * "Request Log" - shows all leave requests that you allowed to view( will have search bar and filters)
- Additionally, admin will have one more function that is a button called "Update Leave Balances" to update along coinciding with pay runs. (on their dashboard)

### 11 May 23 - HD
#### Request Status
After discussed with Mia earlier today, I realised that we were only have 0 or 1 status as request status for 'Pending Approval' and "Approved'. Other than these two, we still need 'reject', and maybe 'cancelled' status. 
I have added a new table of REQUEST_STATUS for this.
Leave requests that loaded in data are 0 or 1 status, there's no impact on the existing data.
Of the queries yesterday for leave request, we can modify them to join with this status table for status descriptions.
As of the status "2, 'Approved and Paid'" it might be an easier solution compare to use two attributes on the table to check 'Approved' and 'Processed by Payroll'. Open for discussion.

### 12 May 23 - Miao
- made some changes in layout, left unfinished(logos are weird).

### 15 May 23 - Miao
- My Approval table still need to adjust when notifications function available.
- My Approval table and Request Log table need to adjust the action column when the request status change.

### 12 May 23 - MT
I was working on implementing the filter function for leave requests. Initially planning to filter the table at the front-end. However, after conducting an online search, it was recommended to filter the data at the backend. So I modified my approach by fetching the filtered data from the database and transferring it to the front-end. Unfortunately, this approach also impact the data for leave balance. Finally, I decided separate the leave balance and leave request functions into two separate pages, ann I also added a dropdown menu and a link to enable easy navigation between these two pages.

### 23/05/16 - BLW
Added a return to dashboard button and clickable colour for name and more details
Created a request log for an employee "request_log_employee" function and html - query is under queries manager as this comes unde the managers functionality - the function is under manager.py

### 12 May 23 - HD
#### Filter or Search
As a manager, there's only a handful of direct reports. Rather than use search by text, to allow manager to select names from a dropdown menu would also be a good experience. 
To achieve the filtering  or search, I have researched three ways. 
1. Form submission to refresh the current page
2. Form submission to refresh a target iframe, the current page would remain
3. Search on HTML using JavaScript (https://www.w3schools.com/howto/howto_js_filter_table.asp)
I have choose to use the 3rd option. In this way, there's less queries and less redirecting the pages. Experience wise, it is really fast response after typing in the text boxes.
#### Convert Date format
In Project1, I have code a lot of logics and calculations  on JINJA-HTML. I received a feedback from an experience coder that it is a good practice to leave the front end only for presenting the data. This time, on Project2, I have tried to convert the data format in python code by manipulate the tuples after the query to fetch one or all. 
### 14 May 23 - Sherlyn
#### Apply for Leave
added a form for users to input leave type, start date, end date and comments. All PH, weekends and leave requests have been blocked and not clickable on date range picker calendar. Also created a leave calendar, so that all public holidays, approved leaves and pending leaves will be displayed.
### 16 May 23 - HD
#### Filter or Search - Cont.
When demo the search function to PO, we realised that four search fields were working separately. When typed in the second field, it ignored the value that have input into the first field. I have modified the JavaScript function  to combine four functions to one. And now, whichever fields got updated, the function would go through all the four fields and display the intersection of the searches.
#### New Leave Status: Draft Status
When employee decides to modify a leave request, such leave request would be updated to "draft" status instantly. In this way, we can prevent that the request might be approved by manager accidentally while editing.
#### Edit Leave
Instead of rewrite a page for editing leave request, we can reuse the code, especially reuse the date picker on the "apply leave" page. 

### 16 May 23 - Sherlyn
#### Apply for Leave
I fixed some bugs for current leave balance function and continued on apply for leave function. Applied css and changed layout for applyleave form. Also added some codes so that when users choose a leave type, leave balance will be displayed. 

### 16 May 23 - Miao
- minor adjustment for tables( sorting, only show unapproved leaves etc.)
- view details function for manager and admin

### 17 May 23 - BLW
- re-routed the manager direct reports employee details page to manager_myDRuserdetail to protect from teh situation of manager jumping into the employees page... 
 - tried to combine the balances into the same page but struggled - will discuss with team if this is important
  - amended the codein base html to allow  tab titles to be dynamic

### 17 May 23 - MT
Add some more comments to my code. Convert date format to NZ time format through MySQL. Modify leave request table and add requested date.

### 18 May 23 - MT
Update HTML and CSS for the function of viewing projected leave balance. Add a link to the sidebar. Add two main tables into HTML, one is to show the current leave balance, the other table is to show the projected leave balance. A calender provided for users to select a date for projecting. Not sure if we still have to hidden the weekends and holidays from the calendar. Because we have data (leave spent days) stored in our database, which can be used to caculate the projected date. Will work on this function tomorrow. Added some CSS class to main.css which is used for this page.

### 18 May 23 - Sherlyn
I changed the layout of apply for leave form and finished the confirmation page which displays selected days and hours duration, while it has not been updated in the database yet. Back button and submit button are added. Added a popup alert if The selected duration exceeds leave balance, while some css needs to be added later.

### 19 May 23 - MT
Did routes and queries for projected leave balance function to get annul leave balance, unapproved and unpaided leave balance. HTML need to update to fit for these data. Still working on caculating projected leave. 


### 19 May 23 -Sherlyn
added validation if selected days exceed leave balance. created an alert page for reminding users if yes and an confimation page if no. Retrieved all input value and will uodate them in database tomorrow. Will also add projected leave balance for alert page tomorrow and display the leave calendar on confirmation page. 

### 20 May 23 -Sherlyn
update database after users applying for a new leave. 

### 21 May 23 -Sherlyn
when users submit a new leave request, a leave calender will display with the new pending leave request being added and a back button to take users back to dashboard or another button to apply for another leave.

### 21 May 23 -MT
Get the latest payroll_date for an employee and calculate projected leave balance based on latest payroll_date and projected_date. 

### 22 May 23 -MT
Update estimated projected leave balance by calculating accrued rate (1.15/14). Did some styling and HTML structure.

### 22 May 23 -Sherlyn
I added more validation for applying leave form. When users select an end date, the selected hours or days will be displayed on the same page, with public holiday and weekends being deducted. Also after users sumbit his annual leave request, projected annual leave balance will also be displayed.

### 23 May 23 -Sherlyn
fixed wrong calculation for end date. 

### 25 May 23 -MT
Update projected leave balance considering leave approved not paid and leave not yet approved. Styling the display of table.
### 25 May 23 -Sherlyn
add more validation for applying leave form. If the dates users select overlap with an existing leave request, an alert page will be displayed
### 26 May 23 -HD
Two more comment-fields added to leave request table for adding comments for request cancellation or rejection.
#### Annual Leave Increments
Leave increments had been precalculated for each employee and for each payroll week. Such result had been saved on the table LEAVE_INCREMENT. The page for payroll process the increment is completed.
When click on the "process" button for the current week, fortnight leave increment will be added to all users. And also, leave requests, which date in the past, and which request has been approved, would be updated to approved and paid status. Additionally, leave balance will be udpated.
#### Sick Leave Increment
Sick Leave reset is more tricky than annual leave.
1. Sick Leave will be reset to 5 days at every work anniversary day
2. Sick Leave is not stackable
3. There are four check points of event: leave request applied, approved, paid, the date of anniversary. The different sequence of the four events would cause a different result in balance.

### 27 May 23 -Sherlyn
Fixed bugs for overlapped dates and updated leave types in database and also in the system

### 28 May 23 -Sherlyn
added back buttons

### 28 May 23 -Miao
- move get cursor to to separate file (db.py) for better logic and tidy things up.
- move some code to manager.py
- approve button working, admin approve button not working 
- change what admin could see, admin can see own leaves but can not act( cause lots of trouble, need restrictions and not done)
- change approve button redirect to request.referrer

### 29 May 23 -Belinda
Reject with reasons button working for approval manager

### 29 May 23 -Miao
- update all approve buttons for both manager and admin(working now)
### 29 May 23 -Sherlyn
fixed bugs for leave balance of leave not paid and leave not approved. Bug occured because leave requests are recorded in days instead of hours in database. and fixed bugs for not displaying confirmation page for several leave types. 

### 30 May 23 -Belinda
Approve button disabled once approved for approval manager
hide reasons when they have none in them
add delete button 

### 29 May 23 -Miao
- update  approve-disable button
- update withdraw button

### 30 May 23 -MT
fixed bugs for projected leave balance of leave not paid and leave not approved.

### 18 May 23 - HD
#### Draft request status Cont.
As we now have a draft status, in queries to check balance consumed on requests, we will have to make sure that such calculation would not include requests in draft status.
When checking applied leaves to prevent request to be raised on the same dates, we need to ignore the requests in draft status also.

### 22 May 23 - HD
#### Organization Chart, data manipulation in python
##### Manipulate data structure of tuple and dictionary
Data fetched from queries are in tuple structure, which normally contains the primary key of a table.
If we turn each row of the result to a tuple in format (primary_key, row_data), which would fit the structure of a dictionary (key, data)

``` 
    dbconn.execute(queries.allemployee_orgchart())
    allemployee_orgchart = dbconn.fetchall()
    allemployee_orgchart_tuple = ()
    for i in allemployee_orgchart:
        t = (i[0],i)
        allemployee_orgchart_tuple = (*allemployee_orgchart_tuple, t)
    allemployee_orgchart_dict=dict(allemployee_orgchart_tuple)
```
For example, on html, {{allemployee_orgchart_dict[uid][4]}} would display the first name for such uid.
In this way, when mapping the report line, we can focus on just employee id for every data nodes. When presenting the details on html, to call the values using dictionary.

##### Manipulate data of tuple - Modify an element
As a nature of tuple data structure, value assignment  is not supported.
Instead, we can convert the tuple to list, modify the value, then convert the list back to tuple.

##### Manipulate data of tuple - Adding tag
```
    dbconn.execute(queries.dateforcalendar())
    dateforcalendar = dbconn.fetchall()
    for i in range(len(dateforcalendar)):
        for x in dept_emp_leaverequests:
            if x[3]<=dateforcalendar[i][0] and x[4]>=dateforcalendar[i][0]:
                dateforcalendar[i] = (*dateforcalendar[i], x[2])
        if dateforcalendar[i][2] == 1:
            dateforcalendar[i] = (*dateforcalendar[i],'Holiday')
        elif dateforcalendar[i][1] == 6 or dateforcalendar[i][1]==7:
            dateforcalendar[i] = (*dateforcalendar[i],'Weekend')
        elif len(dateforcalendar[i]) < 4:
            dateforcalendar[i] = (*dateforcalendar[i],'Available')
```
Instead of modify a value in a tuple, it is easy to append the tuple in a for loop. In this way, we can by-pass the tuple-list-tuple conversion.
I have appended one element at the end of each row of tuple dateforcalendar in the code above.

### 31 May 23 -MT
Start working on Annual leave liability report for manager, set up routes and queries and basic HTML structure. Not finish yet, need to have some more adjustment.

### 31 May 23 -Sherlyn
fixed wrong overlapped dates. Bugs occured because I did not convert date string into proper date format. 

### 1 June 23 -Sherlyn
started manage leave types function. All leave types are displayed with css being applied. Edit button and add button have also been added. Used Js to add leave type on the same page. 

### 1 June 23 -Belinda
Struggled with Edit MyDr leave function for hours - went to a support session - handed task over to Hido 

### 2 June 23 -Belinda
started role type edit for admin page 

### 3 June 23 -Sherlyn
add a new leave type done. Users are able to click on the add button and type in the new leave type name and leave description on the same page. After clicking submit, the new leave type will be updated in the database and also displayed on the same leave type page. Though a confimation page needs to be added before users can submit . And I still need work on the delete for new leave types and edit function. 

### 4 June 23 -Sherlyn
delete a new leave type done. Users are able to click on the delete button and then the deleted leave type will be updated in the database and also disappear on the same leave type page.
### 5 June 23 -Sherlyn
edit a new leave type done. Users are able to click on the edit button and then users can edit on the same page. Updated leave info will be updated in the database and also appear on the same leave type page.
Though a confimation page may need to be added before users can submit . 

### 6 June 23 -MT
update calculation for projected leave balance, considering the impact of overlap leave request. By comparing start_date, end_date, payroll_day, and projected_date to get the correct projected unpaid leave. Need more testing.

### 7 June 23 -MT
fixed bugs for projected leave balance, handle situation for Nonetype results, calculate the unapproved days during the projected period. Calculate the projected balance during the projected period. Need more testing.

### 7 June 23 -Sherlyn
start alert function. The dashoard will show new approvals for last month. 
### 07 June 23 -Belinda
completed role type edit for admin page - page updates with no message just reloads and changes the role at the update click 
### 07 June 23 -Belinda
finished alerts for new approvals. Users will get an alert on the dashboard for new approvals of last monnth.  

### 8 June 23 -MT
Create Liability report, add dropdown menu for leave report. 

### 8 June 23 -Sherlyn
applied css and used javascript to make the alerts fold or unfold


### 10 June 23 -Sherlyn
displayed number of alerts for the last month

### 11 June 23 -Miao
- adjust approve reject and withdraw buttons validations
- adjust layout
- create exception report adjust queries

### 12 June 23 -Miao
- update reports

### 12 June 23 -MT
The dropdown menu for leave reports not working today, tried to debug this problem, not succeed. Create password change function, add confirm password, show and hide password, notifications for this function. 

### 12 June 23 -Sherlyn
many of my alerts function had been overwritten and it took me hours to put everything back. Applied css for my alert table.
### 12 June 23 -Belinda
fixed the bug in the update role function; improved the Back button options for My DR details page; moved the from to inside the For Role in Roles loop so the update role function works correctly - it was returning the whole list each time rather than each row in the table

### 8 June 23 - HD
#### Sick Leave Reset
We could run a schedule function in our code to check the employee anniversary against today's date. However, in this way, if there's a need for modification or for re-run, we will have to stop the entire site for a maintenance.
Instead, we could also have a route, that by visiting a specific route, it triggers the function. By doing this, we could schedule the page refresh on any machine, in a frequency of once or twice a day at midnight.

### 9 June 23 - HD
#### Page redirect upon editing
Upon submitted the edited leave request, the page will be redirected to the page where user clicked the “edit” button. From the edit page, the value of the url has been passed through three routes and templates then it becomes the url value for redirect upon leave confirmation.

### 13 June 23 - HD
#### Python Anywhere
Database query on PythonAnywhere is case sensitive. In contrary, on MySQLWorkbench, it is more flexible between uppercase and lowercase. When we deploy our code to PythonAnywhere, errors of table not found popped a lot. 
We have to perform a clean up from uppercase to lowercase on all the query related code.
In the process replacing the uppercase to lowercase, I have noticed that function names of queries have been created in style of a upper-lower-case-mixture. This is a big lessons-leanrt for us.

### 13 June 23 -Miao
- update reports(days and hours error)
- add validations for pending leaves that start at the past(approve undo button)
try to fix request log table and my approval table for pending leaves that start at the past should not have approve button
- update queries and make pending leaves that start at the past not show

### 14 June 23 -Belinda
fixed the duplicate role types in dropdown selection
put the add new holiday button to the top of the page
amend the days requested on the request log page so its not showing sick leave
amend button-active to Patricias liking