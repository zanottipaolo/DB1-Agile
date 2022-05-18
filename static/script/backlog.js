function get_sprint_task() {
    return JSON.parse('{{ sprint_task|tojson }}');
}

function allowDrop(ev) {
    ev.preventDefault();
}
  
function drag(ev, idTask, is_in_sprint) {
    ev.dataTransfer.setData('Text/html', ev.target.id);
}
  
function drop_on_backlog(ev) {
    console.log("DROPPED ON BACKLOG");
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text/html");//retrieves dropped images data.
    console.log("ID task moved: " + data);

    alert("Move in backlog?")
}

function drop_on_sprint(ev) {
    console.log("DROPPED ON SPRINT ");
    ev.preventDefault();
    var id_task_to_move = ev.dataTransfer.getData("text/html");//retrieves dropped images data.
    console.log("ID task moved: " + get_sprint_task());

    if (get_sprint_task().includes(id_task_to_move)) {
        // è già presente in sprint
        return;
    }
} 