# Django Project Name
OPG Register app for practice

## Overview
Test app for testing basic django knowledge

## Installation
1. Clone the repository:
    - git clone https://github.com/maze76/OPGRegister.git
    - cd OPGRegister

2. Create a virtual environment:
    - python -m venv venv

3. Activate the virtual environment:
    - On Windows:
        venv\Scripts\activate
    - On macOS and Linux:
        source venv/bin/activate

4. Install dependencies:
    - pip install -r requirements.txt

5. Set up database:
    - setup database of your choice with your credentials
    - python manage.py migrate

6. Create a superuser for login to admin page (optional):
    - python manage.py createsuperuser


## Usage
- python manage.py runserver
