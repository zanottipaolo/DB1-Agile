let users = [];

const updateSubtask = (subtask_el_id, new_status) => {
	$.ajax({
		type: "PUT",
		url: "sprint",
		data: {
			subtask_id: subtask_el_id.split("-")[1],
			new_status: new_status,
		},
	})
		.done((subtask_id) => {
			console.log("updated " + subtask_el_id + " to " + new_status);
		})
		.fail((e) => {
			console.log(e);
			alert("error", e);
		});
};

const createSubtask = (task_id) => {
	event.preventDefault();
	const data = $("#create-new-subtask-form-" + task_id)
		.serializeArray()
		.reduce((obj, item) => {
			obj[item.name] = item.value;
			return obj;
		}, {});
	$.ajax({
		type: "POST",
		url: "sprint",
		data: data,
	})
		.done((subtask_id) => {
			console.log("created subtask " + subtask_id);
			// Subtask item
			$("#task" + task_id + "-todo").append(`
			<div
				id="subtask-${subtask_id}"
				class="bg-base-100 rounded-box cursor-pointer w-4/5 text-center whitespace-nowrap"
			>
				<a href="#subtaskDetailModal-${subtask_id}" style="display:block; padding: 20px">
					<span>${data.name}</span>
				</a>
			</div>
			`);
			// Subtask detail
			$("#task" + task_id + "-todo").append(`
				<div class="modal" id="subtaskDetailModal-${subtask_id}">
					<div
						class="modal-box w-100 px-8"
						style="overflow: visible;"
						>
							<a href="#" class="btn btn-sm btn-circle absolute btn-error right-2 top-2"
							>✕</a
						>
						<h3 class="mb-2 font-bold text-lg">${data.name}</h3>
						<div style="display: flex; flex-direction: column; gap: 10px; height: 7em">
							<span>${data.description}</span>
							<div>
								<span class="badge badge-lg" style="font-weight: bold; padding: 5px;" >
										Not assigned
								</span>
							</div>
						</div>
						
						<div class="mt-0 modal-action">
							<button class="btn btn-warning" onclick="deleteSubtask({{ subtask.id }})">
								Delete Subtask
							</button>
						</div>
					</div>
				</div>
			`);
			$(location).prop("href", "#");
		})
		.fail((e) => {
			console.log(e);
			alert("error", e);
		});
};

const deleteSubtask = (subtask_id) => {
	event.preventDefault();
	const htmlComponent = $("#subtask-" + subtask_id);
	$.ajax({
		type: "DELETE",
		url: "sprint",
		data: {
			subtask_id: subtask_id,
		},
	})
		.done((subtask_id) => {
			console.log("delete subtask " + subtask_id);
			htmlComponent.remove();
			$(location).prop("href", "#");
		})
		.fail((e) => {
			console.log(e);
			alert("error", e);
		});
};

// Save users list
$(document).ready(function () {
	$.ajax({
		type: "GET",
		url: "users",
	})
		.done((response) => {
			users = JSON.parse(response);
		})
		.fail((e) => {
			console.log(e);
			alert("error", e);
		});
});
