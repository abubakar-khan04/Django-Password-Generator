Django Password Generator
=========================

A simple Django web application that generates random passwords.

Features
--------
- Password length selection
- Lowercase letters option
- Uppercase letters option
- Numbers option
- Special characters option
- Password strength display
- Copy password button
- Responsive design using pure HTML, CSS, and JavaScript

Technologies Used
-----------------
- Python
- Django
- HTML
- CSS
- JavaScript

Project Structure
-----------------
django_password_generator/
    manage.py
    requirements.txt
    .gitignore
    .env.example
    README.txt
    core/
        settings.py
        urls.py
        wsgi.py
        asgi.py
    generator/
        views.py
        templates/
            base.html
            home.html
            generated_password.html
        static/
            generator/
                css/
                    styles.css
                js/
                    main.js

Setup Instructions
------------------
1. Clone the repository:

   git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git

2. Go inside the project folder:

   cd django_password_generator

3. Create a virtual environment (recommended name: .venv):

   python -m venv .venv

4. Activate the virtual environment:

   Windows:
   .venv\Scripts\Activate.ps1

   macOS/Linux:
   source .venv/bin/activate

5. Install dependencies:

   python -m pip install -r requirements.txt

6. Create a .env file from .env.example:

   Windows:
   copy .env.example .env

   macOS/Linux:
   cp .env.example .env

7. Add your real Django secret key in the .env file:

   DJANGO_SECRET_KEY=your-real-secret-key-here

8. Run the development server:

   python manage.py runserver

9. Open the app in your browser:

   http://127.0.0.1:8000/

Generate a New SECRET_KEY
-------------------------
Run this command:

python manage.py shell

Then run:

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

Copy the generated key into your .env file.

Files to Upload to GitHub
-------------------------
Upload these files and folders:
- manage.py
- requirements.txt
- .gitignore
- .env.example
- README.txt
- core/
- generator/

Do Not Upload
-------------
These files should stay private or local:
- .env
- db.sqlite3
- .venv/
- __pycache__/
- *.pyc

Git Commands
------------
Run these commands inside the django_password_generator folder:

git init
git add .
git commit -m "Initial Django password generator project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
git push -u origin main

Notes
-----
- This project is for learning and local development.
- Keep DEBUG=True only for development.
- Keep your real SECRET_KEY private.
- Do not upload the .env file to GitHub.
