# Project Tracker
## Summary
**Project Tracker** is a simple, easy to use app for keeping track of small scale projects.  
It allows the user the ability to create project tasks and give each task a genre.  
Each task can be given a time upon completion which is saved to the database and used for dashboard analysis.


## Demo
To view a demo of this project, please click **[HERE](http://bglynch-project-tracker.herokuapp.com)**.

A user is required to have an account to access all features of the site.
For the purposes of viewing/testing the site I have created the following dummy account, which make use of the site's features.  

| Email | Password |
| ------ | ------ |
| johndoe@example.com  | H3llowor!d |

## User Experience
**Project Tracker** was built with the following list of users and user stories in mind.  
This allowed me to focus my design and development work on priority features that would be of value to those users:

| User | Sample user story |
| ------ | ------ |
| Structural Engineer (Domestic)| I am an engineer working on domestic projects. These projects are small scale and have repetitive tasks. I would like to be able to create a list of tasks that I must do to complete the project. Also, I would like to track the time it takes to complete these tasks. |


To help me refine the design and layout of my site, I drew a mock-up of the project tracker on a whiteboard. 
I used this mock-up as a guide when coding a 'walking skeleton' of the project tracker.  
Images of the mockups are located in the docs folder [here](docs/wireframes). 

## Features
The key features I developed to fulfil the user stories I created are:
1. User can register an account and login / logout of this account
2. User can reset their password if they forget or misplace it
3. User can create a new project
4. User can associate new projects with a client
5. User can list the tasks associated with a project
6. User can create, edit and delete tasks
8. User can toggle the status of a task
9. The status for a project is auto-updated to complete when all tasks are set to complete
10. The status for a project is changed from complete to in progress if a task in that project is changed from complete to in progress
11. User can capture the time taken to complete tasks
12. User can view a personal dashboard summarising their projects

## Features for Future Development
1. Add additional chart to dashboard (e.g Project Profitability)
2. Ability to assign multiple users to a project
3. Further improve performance by taking remaining steps recommended by Lighthouse

## Technologies Used
The languages, frameworks, libraries and tools that I used to create this portfolio site are:
- [HTML5](https://www.w3.org/html/) is used to apply a structure to the website.
- [CSS3](https://www.w3.org/Style/CSS/) is used to style the website. 
- [Materialize](https://materializecss.com/) is a front-end framework which I used to improve the responsiveness of the website. Materialize also provides functionality to validate the form entries. 
- [JavaScript](https://developer.mozilla.org/bm/docs/Web/JavaScript) is used to apply logic and interactivity to the website.
- The project uses [JQuery](https://jquery.com) to simplify DOM manipulation.
- [Python 3.4](https://www.python.org/doc/) - backend language used to process the data for the project tracker. 
- [Flask](https://developer.mozilla.org/bm/docs/Web/JavaScript) is a microframework I used to serve the project tracker. I also made use of this framework for routing, requests, redirects, rendering templates and static files. 
- [Jinja2](http://jinja.pocoo.org/docs/2.10/) was used for templating. 


## Testing
I have detailed below the different approaches and techniques I used to test the functionality of my website's features and to validate the source code for this project. 

### User scenarios

User testing was completed with the help of a few friends, who acted as testers. I asked the testers to first register and login to the app and then navigate around the site freely (without any instruction) and then to follow sample scenarios I had created based on my user stories.

A sample scenario I asked friends to test was to contact me using the contact form. This was based on the following user story: 
> 1. Log out of the app  
Upon trying to log back in, pretend you forget your password and try to reset it.

> 2. Create a project and task with incorrect details.  
Now try and edit those details to fill in the correct ones

> 3. Create several projects and use the dashboard to find out which client is your most important.


### Navigation
Acting as a user, I tested the navigation of the site by using the navigation links in the navbar. I also tested all routes shown on the user flow diagram to make sure that navigation was intuitive so the user would not have to use the back button on their browser.

### Code Formatting
I used [pycodestyle](http://pycodestyle.pycqa.org/en/latest/) to test and improve the formatting of my code in line with PEP8.

### Defensive Design
Defensive design was tested manually using URL inputs. A method of how this was done can be found [HERE](docs/testing/url-input.md)

### Responsiveness
I tested the responsiveness of my site by viewing the site on different devices and browsers. 
I also employed tools such as [Chrome Developer Tools](https://developers.google.com/web/tools/chrome-devtools/) and [Resizer](https://material.io/tools/resizer/#url=https%3A%2F%2Fcodeinstitute.net) to test responsive features. 

### Performance
I used [Lighthouse](https://developers.google.com/web/tools/lighthouse/) which is a Chrome Dev Tool that helped me assess the performance and quality of the website.  
Results for this testing can be found [HERE](docs/testing/lighthouse-reports) 

### Code validation
I  used the following validators to validate my code:
1. [W3C - HTML Validator](https://validator.w3.org/)  
2. [W3C - CSS Validator](http://jigsaw.w3.org/css-validator/)  

I resolved any HTML validation issues were I felt it made sense to resolve them.  
There are some validation errors/warnings that are unresolved on the project page
1. duplicate ids: this was due to an autogenerated csrf input tag
2. article lacks header: I did not add a heading tag as it impacted on my UX design


## Deployment

I used [Heroku](https://www.heroku.com/) to deploy this project. Here is a list of steps I followed to deploy a production version of my app  
1. Created a Procfile, installed psycopg2-binary and updated my requirements.txt
2. I created a new Heroku app in the Europe Region.  
3. I provisioned a database by going to the Resources tab and selecting the Heroku Postgres add-on
4. I connected to the database locally using the DATABASE_URI and migrated my models to the database
5. I was using a .bashrc file to store my local environment variables. For deployment, I added these environment variables to Heroku settings Config vars.  
6. I connected this app to my project-tracker Github repository.  
7. I triggered a manual build for the initial deployment of my Heroku app and tested this newly deployed version
8. Finally, I enabled automatic deploys so that a new build would occur when a new change was pushed to Github

 ---
 
To run the code locally, please follow the instructions below. If you do not have python 3 installed,  please install it:
1.  Git clone this repository to a local directory:
```sh
git clone https://github.com/bglynch/project-tracker-flask.git
```
2.  Navigate into the project-tracker-flask directory:
```sh
cd project-tracker-flask
```
3.  Create a virtual environment:    
```sh
sudo pip install virtualenv
```
4.  Ensure that your virtual environment runs Python 3.4:
```sh
virtualenv -p /usr/bin/python3.4 venv
```
5.  Activate your virtual environment
```sh
source venv/bin/activate
```
6.  Install the packages required to run this project
```sh
pip install -r requirements.txt
```
7.  Create the migrations repository
```sh
flask db init
```
8.  Create the migration script
```sh
flask db migrate
```
9.  Run the migration script to apply changes to the database
```sh
flask db upgrade
```
10.  Run the project
```sh
python run_app.py
```
11.  Enjoy!

Please note that email reset will not run locally unless you provide your own Gmail setting in the **config.py** file.
To do this export the following to your environment variables:  
``` bash
(venv) $ export MAIL_SERVER=smtp.googlemail.com
(venv) $ export MAIL_PORT=587
(venv) $ export MAIL_USE_TLS=1
(venv) $ export MAIL_USERNAME=<your-gmail-username>
(venv) $ export MAIL_PASSWORD=<your-gmail-password>
```
You may also have to update your Google account setting to allow 3rd party apps to use the mail service

## Credits
### Content
- [stackover page](https://stackoverflow.com/questions/14428564/flask-wtf-uses-input-submit-instead-of-button-type-submit) - InlineButtonWidget in app/forms.py
- [iHateTomatoes Tutorial](https://ihatetomatoes.net/create-custom-preloading-screen/) - Custom preloading screen
- [HTTP Cats](https://http.cat/) - image for the custom error message


### Acknowledgements
- [SQL Designer](http://ondras.zarovi.cz/sql/demo/) - for initial database mockup
- [Miguel Grinberg Flask Mega- Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) - I followed this tutorial to help my understanding of flask before embarking on the project