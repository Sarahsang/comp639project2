import os
import sys

PATH_MAC = os.getenv('HOME')
PATH_WIN = sys.path

print("Mac PATH is "+str(PATH_MAC))
print("Win PATH is "+str(PATH_WIN))

# These details are available on the first MySQL Workbench screen

if PATH_MAC == "/Users/MacbookAir": #If it is Sherlyn's path, use Sherlyn's database config
# Usually called 'Local Instance'
    dbuser = "root" #PUT YOUR MySQL username here - usually root
    dbpass = "Dxx1990723" #PUT YOUR PASSWORD HERE
    dbhost = "localhost" 
    dbport = "3306"
    dbname = "leave_management_dBase"
    #DB Server
    #dbuser = "root"
    #dbpass = "Saoiesf3"
    #dbhost = "150.230.9.92" 
    #dbport = "3308"
    #dbname = "leave_management_dBase"
elif PATH_MAC == "/Users/hido": #If it is Hido's path, use Hido's database config
    if True:
        #Local Config
        dbuser = "root" #PUT YOUR MySQL username here - usually root
        dbpass = "HQ0McFySgAkMPdmnQ" #PUT YOUR PASSWORD HERE
        dbhost = "localhost" 
        dbport = "3306"
        dbname = "leave_management_dBase"
    elif False:
        #DB Server
        dbuser = "root"
        dbpass = "Saoiesf3"
        dbhost = "150.230.9.92" 
        dbport = "3308"
        dbname = "leave_management_dBase"
elif PATH_MAC == "/home/hidodai":
        #pythonanywhere
        dbuser = "hidodai" #PUT YOUR MySQL username here - usually root
        dbpass = "HQ0McFySgAkMPdmnQ" #PUT YOUR PASSWORD HERE
        dbhost = "hidodai.mysql.pythonanywhere-services.com" 
        dbport = "3306"
        dbname = "hidodai$leave_management_dBase"
elif "belin" in str(PATH_WIN): #If it is Belinda's path, use Belinda's database config
    #Local Config
    # Enter your database connection details below
    dbhost = 'localhost'
    dbuser = 'root'
    dbpass = '!E!3VDG7zM569557!'
    dbname = 'leave_management_dBase'
    dbport = '3306'
    #DB Server

elif PATH_WIN == None: #If it is Miao's path, use Mia's database config
    print(PATH_WIN)
    #Local Config
    dbuser = "root" #PUT YOUR MySQL username here - usually root
    dbpass = "root" #PUT YOUR PASSWORD HERE
    dbhost = "localhost" 
    dbport = "3306"
    dbname = "leave_management_dBase"
    #DB Server

elif PATH_MAC == "/Users/miatian": #If it is Mia's path, use Mia's database config
    #Local Config
    dbuser = "root" #PUT YOUR MySQL username here - usually root
    dbpass = "miatian1024" #PUT YOUR PASSWORD HERE
    dbhost = "localhost" 
    dbport = "3306"
    dbname = "leave_management_dBase"
    #DB Server
    #dbuser = "root"
    #dbpass = "Saoiesf3"
    #dbhost = "150.230.9.92" 
    #dbport = "3308"
    #dbname = "leave_management_dBase"
elif PATH_WIN == None: #If it is Belinda's path, use Belinda's database config
    print(PATH_WIN)
    #Local Config
    dbuser = "root" #PUT YOUR MySQL username here - usually root
    dbpass = "root" #PUT YOUR PASSWORD HERE
    dbhost = "localhost" 
    dbport = "3306"
    dbname = "leave_management_dBase"
    #DB Server
    #dbuser = "root"
    #dbpass = "Saoiesf3"
    #dbhost = "150.230.9.92" 
    #dbport = "3308"
    #dbname = "leave_management_dBase"
else:
    dbuser = "root" #PUT YOUR MySQL username here - usually root
    dbpass = "root" #PUT YOUR PASSWORD HERE
    dbhost = "localhost" 
    dbport = "3306"
    dbname = "leave_management_dBase"
    #DB Server
    #dbuser = "root"
    #dbpass = "Saoiesf3"
    #dbhost = "150.230.9.92" 
    #dbport = "3308"
    #dbname = "leave_management_dBase"
    



