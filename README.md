# CS50's Web Programming with Python and JavaScript


## Final Project


### Introduction

This was my final project for the course "CS50's Web Programming with Python and JavaScript" by HarvardX.

It's more or less a simplistic 'trading app', where the primary purpose is simply to show if you would have been better off just buying or holding your chosen asset/portfolio, instead of actively managing it (i.e. buying and selling).

Main reason I did it was because most people intend to buy low and sell high but end up buying high and selling low instead.
So I felt that was the most important thing to visualize before getting fancy by including a lot of other metrics.

In all it's simplicity, it might help to clarify if one is more suited for active or passive investing.


### App Features

In order to view the app, one must either log in to an existing account or create a new one.

Upon registration, the user is prompted to specify their 'initial stack' (I should probably have used a slightly less 'hacky' name).
The initial stack is whatever amount a user has devoted to finding out what type of investor they are.

The initial stack is stored as a database entry and used as a benchmark reference to help the user track where they currently stand compared to a passive 'buy and hold' strategy.

The application also displays average purchase price and average selling price, and includes a complete record of user transactions.

#### Market page

Displays current price of the asset and lets the user create buy or sell orders.

#### Analysis page

Calculates current value of the user's portfolio and compares it to the value of the benchmark.
The user is presented with a 'dynamic' evaluation that determines if they are currently outperforming or underperforming the market.
The page also includes calculations of 'Average Entry Price' and 'Average Sell Price' in order to provide some guidance based on the user's previous activity.

#### Transactions page

Provides a complete record of the user's order history. Implements pagination for records that exceed 10 entries.


### Distinctiveness and Complexity

While my final project may borrow working parts or features from previous projects in the course (i.e. drawing upon the course content), I believe the overarching theme and design of the app is sufficiently distinct from previous course projects.

It's a mobile-responsive app, utilizing Python, Django and Sqlite on the backend and using HTML, CSS, JavaScript, Bootstrapa and SASS to handle the front end.

### How to Install and Run the Application

Clone the project
```
   git clone https://github.com/pe-et/cs50w-final-project
```
cd into the 'btfd' directory (where manage.py is located), create and activate a virtual environment
```
   python -m venv .venv
   .venv/Scripts/Activate.ps1
```
Install dependencies
```
   pip install -r requirements.txt
```
Generate a new secret key
```
   python -c "import secrets; print(secrets.token_urlsafe())"
```
Create a .env file in the same directory as manage.py. Copy paste the secret key into it along with the following:
```
   DEBUG=True
   SECRET_KEY=<secret key goes here>
   DATABASE_URL=sqlite:///db.sqlite3
```
Make migrations
```
   python manage.py migrate
```
Run the application on a local server
```
   python manage.py runserver
```
Visit 127.0.0.1:8000 in your browser to view the application.

### Credits & Acknowledgements
Thanks to:
  * CS50 Staff for creating the course
  * openechangerates.org for the free API
