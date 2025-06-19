# BABBLU - Communication Web Application
**Babblu** is a Django-based web application designed to help children with autism or Down syndrome, or other individuals who face difficulties with verbal communication. It uses visual cards and text-to-speech to assist users in expressing themselves.

## Features
- Add cards with images and custom text.
- Click cards to trigger speech using Web Speech API.
- Choose between multiple themes (blue, pink, neutral).
- User authentication system (signup/login/logout).
- User profile page.
- Responsive design using Bootstrap 5 and CSS media queries.

## Technology stack
### Frontend:
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Web Speech API (for browser-based text-to-speech)

### Backend:
- Python 3.11.9
- Django 5.1.7

### Environment tools:
- Pipenv
- Git & GitHub
- SQLite (default Django database)

## Installation & Run guide (using Pipenv)
These steps will help you set up and run the app on your local machine.
### Prerequisites
Ensure you have the following installed:
- Visual Studio Code
- Python 3.10 or higher
- Git

Check versions in your terminal in VS Code:
- python --version
- git --version

## Step 1: Clone the project repository
1. Open Visual Studio Code, then the terminal.
2. Run this command to clone the repository `git clone https://github.com/dianabali/DLBCSPJWD01`. After that, you will see something like this:

![Screenshot](images/gitclone.png)

3. Navigate inside the DLBCSPJWD01 folder by running `cd your-path-to-DLBCSPJWD01` like this:

![Screenshot](images/navigate.png)

## Step 2: Set up a virtual environment
1. Inside the project repository, install Pipenv using `python -m pip install pipenv`. This will create a virtual environement and install all dependencies listed in the Pipfile.

![Screenshot](images/installpipenv.png)

2. Install Django using `python -m pip install django`.
3. Install Django widget tweaks using `python -m pip install django-widget-tweaks`.
4. Install Pillow using `python -m pip install Pillow`.

## Step 3: Enter the virtual environment
Activate the virtual environment using `python -m pipenv shell`. After that, you will see something like this:

![Screenshot](images/pipenvshell.png)

## Step 4: Apply database migrations
Run `python manage.py migrate` to run migrations. You will see something like this:

![Screenshot](images/migrate.png)

## Step 5: Run the development server
1. Run `python manage.py runserver` and you will see this:

![Screenshot](images/runserver.png)

2. Click on the link (highlighted with blue) and the application will run in your browser. This is what you will see:

![Screenshot](images/babblulogin.png)

3. Click "Register" to create a new account.

**NOTE: It is recommended to use Google Chrome or Microsoft Edge. Some browsers do not support `speechSynthesis`.**

## To access Django Admin
To access Django Administration, you need to create a superuser.
1. Create a superuser running `python manage.py createsuperuser`.
2. Follow the prompts to set a username, email, and password.
3. Run the development server again.
4. After you open the app in your browser, go to `/admin`, and login with your username and password.








