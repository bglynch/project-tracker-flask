// Changes form type to number so user can only input numbers to the Task Time form
function formInputToNumber() {
    let tasks = document.getElementsByClassName("task-item");
    for(var i = 0; i < tasks.length; i++){
      tasks[i].type= "number";
    }
}
window.onload = formInputToNumber;


// Task time input form takes units in minutes
// Function converts minutes to hours and shows the value below the time input
let noOfForms = document.getElementsByTagName("form").length;

function minsToHours(noOfForms) {
   for(var i = 0; i <= noOfForms; i++){
      let mins = document.getElementsByClassName("task-item");
      var hours = Math.floor(mins[i].value/60);
      let minutes = mins[i].value%60;
      let durationConverted = hours+"hrs "+minutes+"mins";
      document.getElementsByClassName("min-to-hr")[i].innerHTML = durationConverted;
      console.log(hours+"hrs "+minutes+"mins");
    }
}

/*---- Add/Edit task form ----*/
// Function to add genre from genre chips when clicked
function addGenre() {
    let genre = window.event.target.innerText.split(" ")[0];
    document.getElementById('genre').value = genre;
}