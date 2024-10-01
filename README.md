# Event Management

Welcome to my Event Management project. This project builds a system that provides microservices necessary to support event management. The system has APIs for user's logging activities and CRUDs operations to manage user's events and users' registration to an event. The system use Python Django for its backend framework, and PostgreSQL for the database

## Table of Contents
- [Setting Up The Project](#setting-up-the-project)
- [Data Model](#data-model)
- [Overview] (#overview)
- [Testing](#testing)

## Setting Up The Project

#### 1. Clone the repository:

```bash
git clone https://github.com/tarcisiusdaniel/Event-Management.git
```
After you have cloned the project, make sure that you are navigated to the project directory to proceed

#### 2. Install pip3, python3, and PostgreSQL

For this step, you need to make sure <a href = "https://www.python.org/downloads/">python3</a>, <a href = "https://www.activestate.com/resources/quick-reads/how-to-install-and-use-pip3/">pip3</a>,  and <a href = "https://www.postgresql.org/download/">PostgreSQL </a> are setup in your local machine

#### 3. Create a virtual environment (Optional)
This is in case if you want to isolate the dependencies for this project from your local machine.
</br>

```bash
python3 -m venv venv
```

After that, activate the virtual environment
<br />

MacOS
```bash
source venv/bin/activate
```
Windows
```bash
venv\Scripts\activate
```

#### 4. Install the Project Dependencies:

```bash
pip3 install -r requirements.txt
```
The ``requirements.txt`` contains all the dependencies that supports this project to work.

#### 5. Set up the Environment Variables:

For this, you will need .env file that contains the credentials that rooted the services in this project. The sample of the variables needed will be inside the ``.env.example`` file. I will give the values of variables needed for the file to you personally. 

#### 6. Create and Migrate the database:

```bash
python3 manage.py migrate
```
This will migrate all the data model and create the tables in the database

#### 7. Run the development server

```bash
python3 manage.py runserver
```
After this command, the project will run, and you will be able to test the microservices built within this project

#### 8. Setup several of the supporting softwares (Recommended)
The softwares listed are really recommended as I used these tools to help running the software and checking to see if the APIs are running correctly.
- <a href = 'https://www.pgadmin.org/download/'>pgAdmin</a>
- Postman

You can substitue pgAdmin with terminal to manage and oversee the Postgre database, and use software other than Postman to test your APIs. However, for simplicity in understanding the [Overview](#overview) section, it is better to use the two software previously mentioned

## Data Model
There are three entities in this data model:
- User
- Event
- Registration

Here is the relations between the models

<img src="./images/data_model.png" alt="Event Management Data Model" width="650" height="400">

From the picture above, the user has one to many (1->M) relationship, because a user can create and have more than one event(s). The user also has one to many (1->M) relationship, because a user can make more than one registration(s), and a registration can only point to one event. 

The registration has one to many (1->M) relationship because an event can hold more than one registration(s) from a user, and a registration can only point to one user.

## Overview

This passage will show the overview of how the system works by giving explanations and snippets of how the API endpoints work. I will also explain what the API's HTTP methods uses, the things each API needs to work, and the URL endpoints.

This application is still in development, so it will use http://localhost:8000 to run the application locally in port 8000.

### User

This is the application that handles user logging activity, annd authentication for running other APIs that maintains the main services of the event management system. There are two main URL endpoints that builds the User app operations:

- ``http://localhost:8000/user/login``, 
    - This URL is a POST method used as the end point to log the user in, and post the user in the database if the user does not exist in the database. If you call this when you are not signed in, you will be taken to a standard Django page, where you can sign in by using your Google account.

    <img src="./images/user/sign_in_landing.png" alt="Event Management Data Model" width="450" height="280">

    Afterwards, click the <b>Google</b> link, and you will be brought to the following page

    <img src="./images/user/sign_in_via_google.png" alt="Event Management Data Model" width="450" height="280">

- ``http://localhost:8000/user/logout``


### Event APIs

### Registration APIs

## Testing