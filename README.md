#TO_DO_APP

simple to do application with basic rest api, backend developed by python and django framework, frontend made with html, free bootstrap templates and custom css.
Application only for educational purposes.

Application functions:
Application views created with mostly customized class based views. 

- Registration(with email confirmation)
- Login (both username, and email address)
- Password reset (with email confirmation)
- Update user account
- Create, modify, delete, and set success tasks
- Create, modify, delete, and set success subtasks
- Calendar to view tasks
- Search function for tasks with selection

API functions:
API views created with customized GenericAPIViews

- Register user
- Update user
- Login 
- Logout
- Update password
- Create and list tasks
- Task detail
- Update tasks
- Delete task
- Create and list subtasks
- Subtask detail
- Update subtasks
- Delete subtask

API works with Session and as well token authentication.

BROWSABLE API (can used with any browser):

- API main summary page : http://127.0.0.1:8000/api/,  Methods: OPTIONS, GET
- User Register: http://127.0.0.1:8000/api/api/api-auth/register/, Methods: POST, OPTIONS
- User Login: http://127.0.0.1:8000/api/api/api-auth/login/,   Methods: GET, POST, PUT, HEAD, OPTIONS
- User Update: http://127.0.0.1:8000/api/api/api-auth/update-user/,    Methods: GET, PUT, HEAD, OPTIONS
- Password Update: http://127.0.0.1:8000/api/api/api-auth/update-password/, Methods:  PUT, OPTIONS
- Task List and Create: http://127.0.0.1:8000/api/api/tasks/,  Methods: GET, POST, HEAD, OPTIONS
- Task Detail: http://127.0.0.1:8000/api/api/task/<task-id>/, Methods: GET, HEAD, OPTIONS
- Task Update: http://127.0.0.1:8000/api/api/task/<task-id>/update/, Methods: GET, PUT, HEAD, OPTIONS
- Task Delete: http://127.0.0.1:8000/api/api/task/<task-id>/delete/, Methods: DELETE, OPTIONS
- Sub Task List and Create: http://127.0.0.1:8000/api/api/task/<task-id>/subtasks/, Methods: GET, POST, HEAD, OPTIONS
- Sub Task Detail: http://127.0.0.1:8000/api/api/subtask/<subtask-id>/, Methods: GET, HEAD, OPTIONS
- Sub Task Update: http://127.0.0.1:8000/api/api/subtask/<subtask-id>/update/, Methods:  GET, PUT, HEAD, OPTIONS
- Sub Task Delete: http://127.0.0.1:8000/api/api/subtask/<subtask-id>/delete/, Methods: DELETE, OPTIONS


Several important navigation links included to tasks and subtask API for better navigation in browsable api.


Extra functions:

- google reCAPTCHA integration
- Django bootsrap datepicker plus
- drf-redesign
- aiosmtpd


INSTALL:
- clone the repository ( git clone https://github.com/immonhotep/to_do_app.git )
- Create python virtual environment and activate it ( depends on op system, example on linux: virtualenv venv  and source venv/bin/activate )
- Install the necessary packages and django  ( pip3 install -r requirements.txt )
- Create the database:( python3 manage.py makemigrations and then python3 manage.py migrate )
- Create a superuser ( python3 manage.py createsuperuser )
- Run the application ( python3 manage.py runserver )


NOTES:

SENDING MAILS:

This site use email validated registration, password change.
so for the usage need some kind of mail server at least for the testing, or need modify the settings.py to real email providers port, and credentials

very simple pre-installed method for tesing with fake mail server on localhost port 1025:

aiosmtpd version 1.4.6 installed within the virtual environment with the requirements.txt, so just run in a different terminal (in the same virtual environment) the following command to run fake mailserver:

python -m aiosmtpd -n -l localhost:1025

emails will appear in the terminal


TESTING API with CLIENT SIDE REQUEST: 

For client side requests need postman or any other api client tool. 


Simple methods with curl to send request to api (several examples):

Get API authentication token with user login credentials (POST request):

curl -H "Content-Type: application/json" --request POST --data '{"username":"<username>","password":"<password>"}' http://127.0.0.1:8000/api/api-auth/api-token-auth/


User registration (POST request):

curl -H "Content-Type: application/json" -X POST --data '{"username":"<username>","password":"<password1>","password2":"<password2>" "email":"<email>"}' http://127.0.0.1:8000/api/api-auth/register/


User update (PUT request, required token authentication):

curl  -H 'Authorization: Token <token>' -H "Content-Type: application/json"  -X "PUT" --data '{"username":"<username>","first_name":"<first name>","last_name":"<last name>","email":"<email>"}' http://127.0.0.1:8000/api/api-auth/update-user/

Get information about the allowed request methods (OPTIONS request):

curl   -H "Content-Type: application/json"  -X "OPTIONS" http://127.0.0.1:8000/api/tasks/ -i

Get the current user all tasks (GET request,required token authentication):

curl  -H 'Authorization: Token <token>' -H "Content-Type: application/json"  -X "GET" http://127.0.0.1:8000/api/tasks/

Get a  task subtasks (GET request, required token authentication):

curl  -H 'Authorization: Token <token>' -H "Content-Type: application/json"  -X "GET" http://127.0.0.1:8000/api/task/<task-id>/subtasks/

Create task (POST request,required token authentication):

curl  -H 'Authorization: Token <token>' -H "Content-Type: application/json" http://127.0.0.1:8000/api/tasks/ -X "POST" --data '{"title":"test","start_date":"2025-05-04","start_time":"08:00:00","due_date":"2025-06-03","due_time":"08:00:00","status":"F"}'

Update task (PUT request,required token authentication):

curl  -H 'Authorization: Token <token>' -H "Content-Type: application/json"  -X "PUT" --data '{"title":"test","note":"test","start_date":"2025-04-05","due_date":"2025-04-05","start_time":"08:00:00","due_time":"09:00:00","status":"S"}' http://127.0.0.1:8000/api/task/<task-id>/update/

Delete task (DELETE request,required token authentication):
curl  -H 'Authorization: Token <token>' http://127.0.0.1:8000/api/task/<task-id>/delete/  -X "DELETE"



and for subtasks working the similar way ....



API security:

settings.py contain throttling settings to prevent DOS and brute force attacks against API

currently with test settings:
Anonymous user request limited to 3/hour
Logged in user request limited 20/hour

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/hour',
        'user': '20/hour'
    },


