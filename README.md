#TO_DO_APP

Application backend : Python/Django

<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img
      src="https://go-skill-icons.vercel.app/api/icons?i=python,django,djangorestframework"
    />
  </a>
</p>

Application Frontend: Html, Bootsrap css, Custom css, and Javascripts

<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img
      src="https://go-skill-icons.vercel.app/api/icons?i=html,bootstrap,css,javascript"
    />
  </a>
</p>

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

| Description              | URLS                                                       | METHODS                       |
| ------------------------ | ---------------------------------------------------------- | ----------------------------- |                                            
| API main summary page    | http://127.0.0.1:8000/api/                                 | OPTIONS, GET                  | 
| User Register            | http://127.0.0.1:8000/api/api-auth/register/               | POST, OPTIONS                 |           
| User Login               | http://127.0.0.1:8000/api/api-auth/login/                  | GET, POST, PUT, HEAD, OPTIONS |       
| User Update              | http://127.0.0.1:8000/api/api-auth/update-user/            | GET, PUT, HEAD, OPTIONS       | 
| Password Update          | http://127.0.0.1:8000/api/api-auth/update-password/        | PUT, OPTIONS                  |
| Task List and Create     | http://127.0.0.1:8000/api/tasks/                           | GET, POST, HEAD, OPTIONS      |
| Task Detail              | http://127.0.0.1:8000/api/task/{int:task.pk}/              | GET, HEAD, OPTIONS            |
| Task Update              | http://127.0.0.1:8000/api/task/{int:task.pk}/update/       | GET, PUT, HEAD, OPTIONS       |
| Task Delete              | http://127.0.0.1:8000/api/task/{int:task.pk}/delete/       | DELETE, OPTIONS               |
| Sub Task List and Create | http://127.0.0.1:8000/api/task/{int:task.pk}/subtasks/     | GET, POST, HEAD, OPTIONS      |
| Sub Task Detail          | http://127.0.0.1:8000/api/subtask/{int:subtask.pk}/        | GET, HEAD, OPTIONS            |
| Sub Task Update          | http://127.0.0.1:8000/api/subtask/{int:subtask.pk}/update/ | GET, PUT, HEAD, OPTIONS       |
| Sub Task Delete          | http://127.0.0.1:8000/api/subtask/{int:subtask.pk}/delete/ | DELETE, OPTIONS               |



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



sample images from tasks and subtask pages:

![tasks](https://github.com/user-attachments/assets/da8a7a5b-8362-4f3b-b359-13ecc74ce2c3)


![subtasks](https://github.com/user-attachments/assets/1f8e50c7-db86-4f8d-b91b-255c9e8d383f)











