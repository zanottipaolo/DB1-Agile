$("modalMoveTask").hide();

function allowDrop(ev) {
    ev.preventDefault();
}
  
function drag(ev, idTask, is_in_sprint) {
    ev.dataTransfer.setData('Text/html', ev.target.id);
}
  
function drop_on_backlog(ev) {
    ev.preventDefault();
    var id_task_to_move = ev.dataTransfer.getData("text/html");//retrieves dropped images data.
    currentPosition = document.getElementById(id_task_to_move).parentNode.id; // Current sprint or backlog

    if (currentPosition == "backlog") {
        // è già presente in backlog
        console.log('Task già presente in sprint');
        return;
    }
    else {
        console.log('Da spostare');
        updateTask(id_task_to_move, -1);
    }
}

function drop_on_sprint(ev) {
    ev.preventDefault();
    var id_task_to_move = ev.dataTransfer.getData("text/html");//retrieves dropped images data.
    var currentPosition = document.getElementById(id_task_to_move).parentNode.parentNode.id; // Current sprint or backlog
    var currentSprint = document.getElementById('idCurrentSprint').textContent;
    if (currentPosition == "currentSprint") {
        // è già presente in sprint
        console.log('Task già presente in sprint');
        return;
    }
    else {
        console.log('Da spostare');
        if (currentSprint != "") {
            updateTask(id_task_to_move, currentSprint);
        }
        else {
            document.getElementById('error_nosprint').classList.remove('hidden');
        }
    }
} 

function open_new_subtask(father_task) {
    console.log(father_task);
    document.getElementById("title_modal_subtask").innerHTML = "New subtask related to Task with id: " + father_task + "";
    var modal = document.getElementById("modalNewSubTask");
    document.getElementById("father_task").value = father_task;
    location.href="#";
    modal.classList.remove('hidden');
}

function closeModal_subtask() {
    var modal = document.getElementById("modalNewSubTask");
    modal.classList.add('hidden');
}

const updateTask = (task_id, new_status) => {
	$.ajax({
		type: "POST",
		url: "backlog",
		data: {
            move_task: true,
			task_id: task_id,
			new_status: new_status,
		},
	})
		.done(function () {
            $("#currentSprint").load(" #currentSprint");
            $("#backlog").load(" #backlog");
        })
		.fail(function (e) {
			console.log(e);
			alert("error", e);
		});
	console.log(task_id, new_status);
};