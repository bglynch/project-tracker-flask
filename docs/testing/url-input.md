# Defensive Testing using URL input

### Summary
The backend logic of this app uses data from the page urls to run.  
Therefore this code needed to be written so that only owners of a project or task were able to manipulate this data.

To test this I created a scenario with 2 users: John Doe and Jane Doe

- **John Doe** has 2 project of which one of them is completed.  
- **Jane Doe** has no projects completed.  
- To test  I logged in as **Jane Doe** and input URLs that were relating to John Doe's projects

### URLS
---
| URLS to Test | Aim |
| ------------ |-------|
| **/project / \<projectno\>**                      | access project not owned by Jane |
| **/project / \<projectno\> / edit_project**       | edit project not owned by Jane |
| **/project / \<projectno\> / delete_project**     | delete project not owned by Jane |
|<img width=400/>|<img width=400/>|
| **/project/\<projectno>/add_task**                | add a task to a project not owned by Jane|
| **/project/\<projectno>/delete_task/<task_id>**   | delete a task not owned by Jane |
| **/project/\<projectno>/edit_task/<task_id>**     | edit a task not owned by Jane |
| **/project/\<projectno>/task_complete/<task_id>** | complete a task  not owned by Jane |
| **/\<projectno>/task_not_complete/\<task_id>**    | uncomplete a task not owned by Jane |
  
  
### Method
---
- Cloned the app as per the directions in the README file
- Created users John Doe and Jane Doe
- Added projects and tasks to John Doe's profile
- Checked the database using sqlite commands

Here is a snapshot of the commands and results of checking the database
```sql

sqlite3 app.db

sqlite> .headers ON
sqlite> .mode column

sqlite> SELECT
   ...> user.username AS Username,
   ...> project.id AS ProjectID,
   ...> project.completed AS Finished,
   ...> task.id AS TaskID,
   ...> task.title AS Task,
   ...> task.completed AS Task_Completed
   ...> FROM
   ...> task
   ...> INNER JOIN project ON project.id = task.project_id
   ...> INNER JOIN user ON user.id = project.user_id
   ...> ;  
   
Username    ProjectID   Finished    TaskID      Task        Task_Completed
----------  ----------  ----------  ----------  ----------  --------------
john doe    1           1           1           Task 01     1             
john doe    1           1           2           Task 02     1             
john doe    2           0           4           Task 03     0
```
- login as Jane Doe
- input the URLS stated above using John Doe's project id's and task id's

### Results

| URL Input | Result |
| ------------ |-------|
| **/project/1**                    | Custom 403 error page |
| **/project/1/edit_project**       | Custom 403 error page |
| **/project/1/delete_project**     | Custom 403 error page |
|<img width=400/>|<img width=400/>|
| **/project/1/add_task**           | Custom 403 error page |
| **/project/1/delete_task/1**      | Custom 403 error page |
| **/project/1/edit_task/1**        | Custom 403 error page |
| **/project/1/task_complete/4**    | Custom 403 error page |
| **/1/task_not_complete/1**        | Custom 403 error page |
