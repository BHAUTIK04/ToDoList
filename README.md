# ToDoList
App for todos.

# Technologies Used
```
* Python 3
* Django=1.11
* Bootstrap-4
* HTML
* CSS
* JQuery
```

## Getting Started
To deploy this project:-

### Using virtualenv
```
* Create virtualenv with some name for python3 Eg:- virtualenv name --python=python3
* Activate created virtualenv Eg:- source name/bin/activate
* Go to project folder Here todo/
* Install all required packages using 'pip install -r requirements.txt'
* To start project:- Run python manage.py runserver
* By default project will start on localhost:8000 or 127.0.0.1:8000
* For running on particular port and IP:- python manage.py runserver IP:PORT 
* To run test cases:- python manage.py test -v=2
```

### Without virtualenv
```
* Make sure your environment supports Python3
* Go to project folder Here todo/
* Install all required ppackages using 'sudo pip install -r requirements.txt'
* To start project:- Run python manage.py runserver
* By default project will start on localhost:8000 or 127.0.0.1:8000
* For running on particular port and IP:- python manage.py runserver IP:PORT
* To run test cases:- python manage.py test -v=2
```

## Available Functionalities

* Register New user
* User Login 
* Create New todo
* View All todos (Created by other user and your)
* Status change for any Todo undone -> done, done -> undone
* Edit your Todo
* Delete your Todo
* User Logout
