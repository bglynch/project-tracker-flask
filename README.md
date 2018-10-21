# Project Tracker
## Summary
**Project Tracker** is a simple, easy to use app for keeping track of small scale projects.  
It allows the user the ability to create project tasks and give each task a genre.  
Each task can be given a time upon completion which is saved to the database and used for dashboard analysis.


## Demo
To view a demo of this project, please click **[HERE](http://bglynch-project-tracker.herokuapp.com)**.

## User Experience
**Project Tracker** was built with the following list of users and user stories in mind.  
This allowed me to focus my design and development work on priority features that would be of value to those users:

| User | Sample user story |
| ------ | ------ |
| Structural Engineer (Domestic)| I am an engineer working on domestic projects. Theses projects are small scale and have repeditive tasks. I would like to be able to create a list of tasks that I must do to complete the project. Alaso, I would like to track the time it takes to complete these tasks. |


To help me refine the design and layout of my site, I drew a mock-up of the project tracker on a whiteboard. 
I used this mock-up as a guide when coding a 'walking skeleton' of the project tracket.  
Images of the mockups are located in the docs folder [here](docs/wireframes). 

## Features
The key features I developed to fulfil the user stories I created are:
1. User can register an account and login / logout of this account
2. User can reset their password if they forget or misplace it
3. User can create a new project
4. User can associated new projects with a client
5. User can list the tasks associated with a project
6. User can create, edit and delete tasks
7. User list the due date for a project or a individual project task
8. User can toggle the status of a task
9. The status for a project is auto-updated to complete when all tasks are set to complete
10. The status for a project is changed from complete to in progress if a task in that project is changed from complete to in progress
11. User can capture the time taken to complete tasks
12. User can view a personal dashboard summarising their projects


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
User testing was completed with the help of a few friends, who acted as recruiters, hiring managers and clients viewing my portfolio. I asked the testers to first navigate around the site freely (without any instruction) and then to follow sample scenarios I had created based on my user stories. 

A sample scenario I asked friends to test was to contact me using the contact form. This was based on the following user story: 
> To do............


### Navigation
To do ................... 

### Responsiveness
I tested the responsiveness of my site by viewing the site on different devices and browsers. 
I also employed tools such as [Chrome Developer Tools](https://developers.google.com/web/tools/chrome-devtools/) and [Resizer](https://material.io/tools/resizer/#url=https%3A%2F%2Fcodeinstitute.net) to test responsive features. 

### Performance
I also employed the [Lighthouse](https://developers.google.com/web/tools/lighthouse/) which is a Chrome Dev Tool that helped me assess the performance and quality of the website.  

### Code validation
I also used the following validators to validate my code:
1. [W3C - HTML Validator](https://validator.w3.org/)  
2. [W3C - CSS Validator](http://jigsaw.w3.org/css-validator/)  

## Deployment

Heroku was used to deploy this project. I provisioned a sandbox database using heroku postgres. 

To run the code locally, please follow the instructions below:
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

## Credits
### Content
- ...

### Acknowledgements
- [SQL Designer](http://ondras.zarovi.cz/sql/demo/) - for initial database mockup
