# My Receipts

My receips is a App with basic Auth and basic CRUD functionalities, where users can login register, logout, and view, create, update and delete receipts

## Installation

1- Clone this project.

```bash
git clone https://github.com/khelalfa-rabeh96/my_receipts
```

2- Create and activate virtual envirement.

```bash
python3 -m venv env
source env/bin/activate
```

3- Install dependencies into the virtual environment using pip

```bash
cd my_receipts/
python3 -m pip install -r requirements.txt
```

4- Download geckodriver and set the PATH to it in .env.dev file with env vars
 
```bash
DEBUG=1
SECRET_KEY='a_django_secret_key'
SQL_ENGINE=django.db.backends.sqlite3
DB_NAME=db_path
GECKODRIVER_PATH=YOUR_PATH_TO_GECKODRIVER_YOU_DOWNLOADED
STAGING_SERVER=THIS_IS_OPTIONAL_TO_RUn_FUNCTIONL_TEST_FOR_THIS_ADDRESS
```

## Usage

1- Try a demo

Go to [my_receipts](http://rabah96.pythonanywhere.com/)

2- Running the app on local

```bash
python manage.py runserver
```

3- Running unit tests

```bash
python manage.py test receipts/
```

4- Running functional tests tests

```bash
python manage.py test functional_tests/
```

## License

[MIT](https://choosealicense.com/licenses/mit/)