#FNL_webserver

####Jump to Section

- [What IS included](https://github.com/cosanlab/FNL_webserver#what-is-included)

- [Getting Started](https://github.com/cosanlab/FNL_webserver#getting-started)

    - [Adding users](https://github.com/cosanlab/FNL_webserver#adding-users)

    - [Running the development server](https://github.com/cosanlab/FNL_webserver#running-the-development-server)

    - [Initializing/populating the databases](https://github.com/cosanlab/FNL_webserver#initializingpopulating-the-databases)

- [Working with the production server](https://github.com/cosanlab/FNL_webserver#working-with-the-production-server)

    - [Transferring files/videos to the server](https://github.com/cosanlab/FNL_webserver#transferring-filesvideos-to-the-server)

####Folders not included:

    These can be obtained from the production server.

- **CSV**: contains csv files for the databases and datasets; used when populating an initialized MySQL database
- **FNL_Videos**: static video files for streaming
- **keys**: paths, oauth tokens, and keys used by the server
    Only the keys folder is required in order for the site to function, but the video folders will be required in order to stream.

##What IS included:

####Files:
- *database_init.py*: utility used to initialize and populate databases
- *entry.py*: used by uwsgi on the server; required to serve the app
- *passenger_wsgi.py*: required to run the server on dreamhost
- *requirements.txt*: run *$ pip install -r requirements.txt* to install the required dependencies for the webserver
- *runserver.py*: starts the server for development

####Folders:
- **app**: main application; contains python, HTML, and css files used by the webserver
    - *\_\_init\_\_.py*: sets initial variables used in routing, authentication, and the api.
    - *api.py*: routing for data accessible via the api; contains a decorator that makes a routing call require authentication
    - *ffmpeg_shell.py*: used for slicing video files or capturing a single frame; not currently working
    - *login.py*: providoes routing for loging users in via google oauth
    - *models.py*: SQL database models for SQLAlchemy
    - *views.py*: routing for the UX portion of the website; currently only the main homescreen and the video player
    - **static**: contains CSS files; flask expects CSS in the static folder
    - **templates**: contains HTML files; flask expects HTML in the templates folder
- **Public**: added by dreamhost
- **tmp**: contains restart.txt; used to restart the dreamhost server
- **utilities**: contains a few scrips useful when parsing data; shell_data_pull.py allows users to call the website api with a function

##Getting Started

####Folder Layout:

|–––CSV

|–––FNL_webserver

|–––keys

|–––FNL_Videos

###Adding users:

You will be unable to access the videos until you are added as a user.

####From SQLPro (recommended)

1. Following the lab instructions on the wiki, download SQLPro (http://www.sequelpro.com/download). Alternatively, if you're using a PC, switch to a mac (or, find a MySQL application for PC).
2. Log onto SQLPro using the instructions for updating personel from the website; use *tvdb_fnl* for the database (rather than cosanlab_app_db)
3. Create a new row in the *user* database; increment ID by one, and add your gmail acount and first name to the database.

####From the terminal:

1. SSH to *username*:cosanlabtv.dartmouth.edu
2. Open database in a python shell by navigating to the folder and running

        python database_init.py

3. Run *user_add*:

        user_add(<gmail address>,<name>)

4. Check that it worked by logging into the site and verifying you can stream videos or by logging into the database using SQLPro.

    This is more useful for quickly adding a user onto a local development database, but will work if you have access to the server but are not on the approved users list, or want to add several users quickly.

###Running the development server

#####The server uses flask manager to run locally, which can be started by running 'runserver.py' with the runserver command:

        $ python runserver.py runserver

- Running the server locally requires the files from the FNL_webserver github, as well as the **keys** folder. 

- THE KEYS SHOULD NEVER BE PUT ON THE GITHUB but can be accessed and moved to your local machine via **scp** or **rsync** from the production server. Again, DO NOT PUT KEYS IN ANY OF THE *FNL_webserver* FILES; put them in the Keys() class and import them to *app/__init__.py*.

- If you want to stream video or rebuild the databases from CSV files, you'll need to copy those over from the server.

- Enabling debugging in app/__init__.py is helpful when working on the development server; be sure to disable it for the production server.

###Initializing/populating the databases

1. Disable the call importing api and views at the end of app/__init__.py:

        # import api, views

2. Create a SQLAlchemy instance for the class, with **floats** represented with **db.Float**, **integers** with **db.Integer**, and **strings** with **db.String** or **db.Text** like so:

        class ep3(db.Model):
            __tablename__ = 'ep3'
            id = db.Column(db.Integer, primary_key=True, unique=True)
            timestart = db.Column(db.String(15))
            timeend = db.Column(db.String(15))
            dialogue = db.Column(db.String(255))


3. Place the CSV file into the CSV folder, or at least somewhere you can link to in python

4. Run the add_data command like so:

        >>> add_data(database,csvfile,columns)

    Where database is the name of the database as it is named in the SQLAlchemy instance, csv file is the path to the csv file, and columns is a list or tuple of the colums in the SQLAlchemy instance **in the order they appear in the CSV file**.

**Note:** you may need to format the data or adjust the add_data function to adjust the data (as with add_annotation_data()). For instance, the query performed when accessing the API will not work unless the time data are formatted as *HH:MM:SS.MS*.

Additionally, when working with ELAN, you'll need to export the file as tab-delimited, then open it in excell, and save it as a CSV before running the database_init function on it.


##Working with the production server:

####Transferring files/videos to the server:

This took an emberrasingly long time to figure out, but this command seemed to work:

    $ rsync -avu -e 'ssh' /path/to/video/folder user@cosanlabtv.dartmouth.edu:FNL_Videos

Note: must be authorized to access the server.

- uwsgi configuration based on this blog
https://chriswarrick.com/blog/2016/02/10/deploying-python-web-apps-with-nginx-and-uwsgi-emperor/

- uwsgi.ini file located here
/etc/uwsgi-emperor/vassals/tvsite.ini

- Restart uwsgi service
systemctl restart emperor.uwsgi