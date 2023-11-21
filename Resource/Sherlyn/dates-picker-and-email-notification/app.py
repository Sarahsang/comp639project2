from flask import Flask, render_template, request
from datetime import datetime, timedelta
from flask_mail import Mail, Message


app = Flask(__name__)

with app.app_context():
    # 在应用程序上下文中访问 current_app
    print(app.config['DEBUG'])

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'duanxuexing1990723@gmail.com'
app.config['MAIL_PASSWORD'] = 'mjpe nnyx ylcr ccno'

mail = Mail(app)



@app.route('/')
def index():
    min_startdate = datetime.today() + timedelta(days=1)
    max_startdate =datetime.today() + timedelta(days=30)
    return render_template('datepicker.html',min_startdate=min_startdate, max_startdate=max_startdate)

@app.route('/dateRangePicker')
def dateRangePicker():
    return render_template('dateRangePicker.html')

@app.route("/process_dates", methods=["POST"])
def process_dates():
  # Print out the contents of the request object
  print(request)
  
  # Extract selected dates from request parameters
  try:
    start_date = request.form["start_date"]
  except KeyError:
    start_date = None
  try:
    end_date = request.form["end_date"]
  except KeyError:
    end_date = None
  
  # Print out the extracted date values
  print("start_date:", start_date)
  print("end_date:", end_date)
  
  # Process selected dates as needed
  # ...
  
  return "Dates processed successfully!"

@app.route('/emailNotification')
def emailNotification():
    return render_template('emailNotification.html')

@app.route('/send_email', methods=["POST"])
def send_email():
   
    # get user email from the form
    user_email = request.form.get('user_email')
    with app.app_context():
        msg = Message('Notification Subject', sender='duanxuexing1990723@gmail.com', recipients=[user_email])
        msg.body = 'Notification Message'
        mail.send(msg)
    
    return render_template('emailsuccess.html', recipients=user_email )

if __name__ == '__main__':
    app.run(debug=True)