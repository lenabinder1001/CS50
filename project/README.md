# Personal Planner
#### Video Demo: https://youtu.be/wPCo5BV5nq8
#### Description:

### **Overview**
For my final project i decided to do a personal planner web application which i can also use after the course.
The main features are:
- Register users and remember them with sessions
- Todo-List (Add todos, edit todos, delete todos, give priorities and a status)
- Spendings (Add spendings, edit spendings, delete spendings and tag them with a category)
- Show spendings of current month in a pie chart (using JavaScript)
- Get current weather in my hometown (using API from openweathermap.org)

### **Database planner.db**
Before i started coding i thought about the database i want to use for my project. How many tables do i need?
How many fields do i need in these tables and what are their values? My planer.db database at this time contains
three tables: users, todos and spendings.

**users:**
Every user has an id (integer), username (text), hashed password (text) and his or her first name (text).

**todos:**
Todos have an id (integer), name (text), status (text) and a priority (text).

**spendings:**
Spendings have an id (integer), name (text), amount (text), category (text) and date (day, month and year as text).

### **app.py**
The first lines of app.py are the same as in the finance web application: import functions, import helpers (apology and login_required)
configurate application, ensure templates are auto-reloaded, configure session to use filesystem, configure CS50 Library to use SQLite database
and the function after_request.

**login function**
This function clears all sessions and returns the template login.html if the user reaches the route via GET. The login.html file contains a form with different input fields
for username and password and a submit button to post the data back to the login function. There is also a link to the register function in case
the user has not registered yet. If the user reaches the login function via POST by submitting the form, the function ensures that
a username and a password were submitted, makes a database query to ensure that the username exists and the password is correct, redirects the user to his
homepage and remembers the user data in a session.

**register function**
This function also clears all sessions and returns the template register.html if the user reaches the route via GET. The register.html file contains a form with different
input fields for first name, username, password and confirmation and a submit button to post the data back to the register function. If the user reaches the register function
via POST by submitting the form, the function ensures that name, username, password and confirmation were submitted, ensures that both passwords are equal, makes a database
query to ensure that the username does not already exists and insert a new user to the database if not. It also remembers that the user is logged in.

**todos function**
This function makes a database query to get all todos from the current logged in user and passes them to the todos.html file. The todos.html file shows all todos from
the user in a table with the priority and a tag for the current status of the task. There are buttons to edit and delete every task and a button to add a new todo.

**add_todo function**
This function returns the template add_todo.html if the user reaches the route via GET. The add_todo.html file contains a form with different
input fields for the name and the priority of the task and a submit button to post the data back to the add_todo function. If the user reaches the add_todo function
via POST by submitting the form, the function ensures that a name and a priority were submitted and inserts a new todo to the database with the matching user_id. It then redirects
to the todos function.

**edit_todo function**
This function returns the template edit_todo.html and the selected todo (id of task is tranferred, when user clicks on edit-button) if the user reaches the route via GET. The edit_todo.html
file contains a form with different input fields for the name, the status and the priority of the task and a submit button to post the data back to the edit_todo function. Its possible to only fill in one of the input fields if the user only wants to change one thing. If the user reaches the add_todo function via POST by submitting the form, the function checks which input fields were submitted and changes these fields in the database with the matching user_id. It then redirects to the todos function.

**delete_todo function**
This function deletes the todo from the database (id of task is tranferred, when user clicks on delete-button) and redirects to the todos function.

**spendings function**
This function makes a database query to get all todos from the current logged in user from the current month and passes them to the spendings.html file. The spendings.html file shows all spendings from the user in a table with the amount and a tag for the category of the spending. There are buttons to edit and delete every spending and a button to add a new spending.

**add_spending function**
This function returns the template add_spending.html if the user reaches the route via GET. The add_spending.html file contains a form with different
input fields for the name, the amount and the category of the spending and a submit button to post the data back to the edit_spending function. If the user reaches the add_spending function
via POST by submitting the form, the function ensures that a name, a amount and a category were submitted, gets the current date with day, month and year and inserts a new spending to the database with the matching user_id. It then redirects to the spendings function.

**edit_spending function**
This function returns the template edit_spending.html and the selected spending (id of task is tranferred, when user clicks on edit-button) if the user reaches the route via GET. The edit_spending.html file contains a form with different input fields for the name, the amount and the category of the task and a submit button to post the data back to the edit_spending function. Its possible to only fill in one of the input fields is the user only wants to change one thing. If the user reaches the edit_spending function via POST by submitting the form, the function checks which input fields were submitted and changes these fields in the database with the matching user_id. It then redirects to the spendings function.

**delete_spending function**
This function deletes the spending from the database (id of spending is tranferred, when user clicks on delete-button) and redirects to the spendings function.

**index function**
The first part of this function deals with the openweathermap.org API. It makes a request to get the current temperature of my hometown. Because we have celsius and not fahrenheit in Germany,
the function also conterts the temperature. The function also makes a databse query to get the name from the user which is used to greet the user at his or her homepage. After that it makes another database query to get three todos which are not done yet to also print them out on the homepage. Next it groups all spendings from the user by category, calculates the sum per category and finally calculates the total spending sum of the current month.

**index.html**
This file represents the homepage of my web application. First there is a section to greet the user by his or her name. Underneath it shows three todos that are not finished yet and a button which links to the todos page. On the left side the monthly spendings are represented in a pie chart which i did with JavaScript and Google Charts. There is also a section in which the current temperator and date are represented.

**logout function**
If the user clicks on the logout-button, this function clears all sessions and redirects to the login function.

**style.css**
The style.css file contains all styling information for the web application. I didn´t really made any concret design decisions. I just did what looks and feels good in my eyes. Most of the time i change sizes, margins, backgroundcolors and the colorsof the text. I also included a font from Google Fonts and a few icons from Bootstrap.

**layout.html**
This html file contains all the elements which show up on every other html file like the menu or the logo to avoid duplications. The content of the other html files is transferred by referencing to the layout.html file.

