# cs408-mini-lab

## Project Description: Canvas Assignment Tracker
This project is meant to pull assigments from all your courses on Canvas 
and consolidate them into one place in an easy to read table, which includes
columns for courses, assignment names, due dates, and whether or not it's been
submitted. From this table, you can filter by course. 

## Setup Instructions

### 1. Install a bunch of stuff
To run this code, you'll need to install the Django. If you don't have python
installed on your computer, you'll need download it from https://www.python.org/downloads/.

python -m pip install Django

If this doesn't work for you, try python3 -m pip install Django. Version
6 or above works best with this code. 


### 2. Clone the Repository

git clone https://github.com/<your-username>/cs408-mini-lab.git

cd cs408-mini-lab
cd minilab

### 3. Install the Dependencies
All the dependencies you need should be listed in INSTALLED_APPS under settings.py. They're included here below for your convenience. 

#### Install django_tables2
```
python -m pip install django_tables2
```
#### Install django_filters

```
python -m pip install django_filters
```

#### Install Bootstrap3

You're not going to believe this, but the command for installing bootstrap3 is:

```
python -m pip install django-bootstrap3
```

### 4. Create Your .env File
Copy the template and open it in your editor:

```
cp .env.example .env
```

Then paste in the token you generated in Canvas (Account → Settings → Approved Integrations → + New Access Token):

CANVAS_API_TOKEN=13~yourReallyLongTokenGoesHere
CANVAS_BASE_URL=https://boisestatecanvas.instructure.com
PORT=3000

MAKE SURE .env IS LISTED IN YOUR .gitignore! 

### 5. Run It

Here is where things can get a little wonky. The command to run it is:

```
python3 manage.py runserver
```

And then you can open up http://127.0.0.1:8000/fullstack/ and you'll be at the home page.

However, running the server that way occasionally don't work, and no assignments get rended. For consistent results, run the program through 
your IDE's debugger. 



## Usage

Okay. The port will take you to the landing page. To get the the assignment tracker, click the first link, which will take you to a table with all of your assignments, sorted by course name. The first time the page loads, it reaches out to Canvas, collects all courses and assigments for the semester, stores them in a database, and formats them into a table. Any time the page loads after that, it will check for new assignments to add to the table. There's also a drop down that lets you filter your assignments by course. 

If you want to clear the database for any reason, do
```
python manage.py shell
```
To open the interactive interpreter. From there, you can do
```
Course.objects.all().delete()
```
And that will clear the whole database
## API Endpoints Used
| Method  | Endpoint | What we use it for|
| ------------- | ------------- | ------------- |
| GET | /api/v1/courses  | To fill the dropdown, get the course names for the table, and as an easy way to remove both courses and assigments from the database|
| GET  | /api/v1/courses/:id/assignments  | To fill out the table|

## Pagination
Both endpoints are paginated by Canvas. To handle pagination, the method
fetch_all_assigments sets up a while loop to find the next page's url in links in the current header, and if there isn't one, it will stop.

## Project Structure
```
.
├── .vscode                Debugger launch file
├── minilab
│   ├── fullstack           
        ├── pycache         
        ├──migrations           Builds the databases for models.py
        ├──static           
        │   ├──style.css        handles the css for assignments.html
        ├── templates           Html templates: assignments.html, index.html
        ├──init.py
        ├──admin.py
        ├──apps.py
        ├──filters.py           The filter module that creates the dropdown 
        ├──models.py            Holds the models for Assignment and Course
        ├──services.py          Interacts with Canvas - handles pagination
        ├──tables.py            Creates table for assignment.html
        ├──tests.py
        ├──urls.py              
        └──views.py             Connects templates to functions
    ├── mysite             
         ├── env.examples       Template
         ├── settings.py    
         └──  urls.py
     └──  manage.py                 
```


## Reflection

Going into this project, I chose to work with Django to challenge myself by getting more experience with Python. That was a mistake. A lot of the errors I had going into this were difficult to parse, because I didn't know if I was making a language mistake or a fullstack development mistake. In the future, I'm going to stick to only doing one hard thing at a time. 

One thing I did like about Django was the was the database was integrated. It made it really easy to add to create tables and update/add/remove items, which allowed me avoid going over json files that were previously accessed. This worked as a sort of bandaid to the loading time problem I was having. 

One thing I learned, or was reminded of, is that AI sucks. At the beginning of this project, I had no idea where to start, so I decided to go with the recommendation of using AI to generate some boilerplate code for the REST API. It didn't work (some methods were connected to objects that they very much did not go with), and it took a lot of googling to get to anyting remotely usable. It definitely gave me a starting point, though, so it wasn't all bad. I do wonder if I should have gone straight to StackedOverflow though, it may have been quicker. 

I still don't know a good way to parse through a large amount of data without the server loading forever, and async and await are still mystifying to me (not for lack of trying). I also geniunely don't know why my code only worked in the debugger. 



