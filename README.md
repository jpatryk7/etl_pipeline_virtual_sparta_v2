# ETLPipelineForSG
Data drawn from S3 bucket from Sparta's AWS is converted and intergrated into a SQL database. Program is useful for data from cloud being moved into a database for querying. The schema used is __, and database is normalised. Cleaned data is also pushed back to S3, as well as new data being uploaded into the cloud going straight into the pipeline.
Pipeline is created in python using __ (django, flask) and using __ there is also the option to view specific entries in a single custom view. 
There is also some code for analytics, as well as a visualised dashboard.

## Set up
1. Open the terminal in the directory with projects or create a new directory
2. Clone repository `$ git clone https://github.com/AChaudarySG/ETLPipelineForSG.git`
3. Cd into the project directory `$ cd ETLPipelineForSG`
4. Create a new virtual environment `$ python -m venv my_venv`
5. Configure interpreter settings to add `my_venv` to the project and restart IDE (**make sure that you have my_venv showing in your command line**)
6. Run `$ cd app`
7. Run `$ docker-compose up -d --build` to spin up the MySQL container
8. Go into the `app` directory (`$ cd app`). Run `$ python manage.py makemigrations` and `$ python manage.py migrate` to update database tables according to your models
9. Run `$ python manage.py runserver` - the app can be accessed now at `http://127.0.0.1:8000`