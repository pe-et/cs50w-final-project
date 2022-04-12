# CS50's Web Programming with Python and JavaScript


## Final Project


### Introduction

This is my final project for the course: 'CS50's Web Programming with Python and JavaScript' by HarvardX.

The idea sprung from a common pitfall faced by many aspiring investors:
What was initially a passive investment strategy (buy and hold), gradually evolves into a fully-fledged trading endeavor to beat the market.

A small minority will be successful in this venture. However, the vast majority would be better off leaving the investment alone.
Given the amount of noise that people experience on a day to day basis, it's easy to skip the basics in favor of shinier things.

The app's main purpose therefore, is to address one of the most fundamental decisions the novice investor faces:
Am I a passive or active investor?


### App Features

In order to view the app, one must either log in to an existing account or create a new one.

Upon registration, the user is prompted to specify their 'initial stack'.
The initial stack is whatever amount a user has devoted to finding out what type of investor they are (sometimes called a 'trading stack', it denotes whatever amount of the total investment the investor is willing to lose).

The initial stack is stored as a database entry and used as a benchmark reference to help the user track where they currently stand compared to a passive 'buy and hold' strategy.

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

### Files and Folders

* btfd - project directory
  * .env - environment variable containing django secret key and api key, included in the course submission to facilitate grading
* ticker - app directory
  * static/ticker - contains the apps JavaScript, CSS and SASS
    * market.js - JavaScript for market.html and orders.html
    * styles.css - CSS file compiled from style.scss
    * styles.css.map - CSS sourcemap allowing the browser to map CSS from SASS
    * styles.scss - SASS file
  * templates/ticker - app's template files
    * analysis.html - template for the 'analysis' page
    * averageprice.html - included in analysis.html. Displays average entry and sell prices
    * base.html - the apps base template
    * login.html - template for the login screen
    * market.html - main template for the 'market' page
    * messages.html - Handles Django messages, included in base.html
    * orders.html - order forms, included in market.html
    * pagination.html - implements pagination, included in transactions.html
    * register.html - template for register screen
    * transactions.html - template for displaying transaction history
  * admin.py - models and other code pertaining to django admin
  * apps.py - app configuration code
  * models.py - contains 3 database models used in the app
  * urls.py - url routing for the ticker application
  * views.py - backend for the app views as well as various helper functions
* requirements.txt - project dependencies
* README.md - project's readme file. You're reading it

### How to Install and Run the Application


* Setup and activate a virtual environment (optional)
* Install project dependencies:
```
pip install -r requirements.txt
```
* Run server:
```
python manage.py runserver
```
* Open a browser tab and navigate to localhost:
```
 127.0.0.1:8000
```

### Credits & Acknowledgements
Thanks to:
  * CS50 Staff for creating the course
  * openechangerates.org for the free API
