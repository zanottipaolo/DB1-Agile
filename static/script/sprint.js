let users = [];

const updateSubtask = (subtask_el_id, new_status) => {
	$.ajax({
		type: "PUT",
		url: "sprint",
		data: {
			subtask_id: subtask_el_id.split("-")[1],
			status: new_status,
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
		.done((subtask) => {
			console.log("created subtask " + subtask.id);
			// Subtask item
			$("#task" + task_id + "-todo").append(`
			<div
				id="subtask-${subtask.id}"
				class="bg-base-100 rounded-box cursor-pointer w-4/5 text-center whitespace-nowrap p-3"
				style="display: grid; grid-template-columns: 1fr 3fr 1fr; align-items: center;"
				>
				<div></div>
				<span style="padding: 0px 1em 0px 1em;">${subtask.name}</span>
				<button
						onclick="openSubtaskDetailModal(${subtask.id})"
						class="p-2 bg-base-300 rounded-box"
					>
					<i class="fa-solid fa-ellipsis-vertical"></i>
				</button>
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

const openSubtaskDetailModal = (subtask_id) => {
	$.ajax({
		type: "GET",
		url: "subtask-detail",
		data: {
			id: subtask_id,
		},
	})
		.done((response) => {
			console.log(response);
			$("#subtaskDetailModals").html(`
				<div class="modal" id="subtask-detail-modal" sty>
					<div
						class="modal-box w-200 px-8"
						style="overflow: visible;"
						>
							<a href="#" class="btn btn-sm btn-circle absolute btn-error right-2 top-2"
							>✕</a
						>
						<span style="font-weight: bold; font-size: 1.5em" >${
							response.subtask.name
						}</span>
						<div style="display: flex; flex-direction: column; gap: 10px; margin-top: 1em">
							<div>
								<span style="font-weight: bold">Description</span><br>
								<span>${response.subtask.description}</span>
							</div>
							<div>
								<span style="font-weight: bold;">Assigned</span>
								<div style="display: flex; align-items: center; margin-top: .2em">
									<div
										id="subtask-detail-modal-assigned-user"
										class="badge badge-lg"
										style="font-weight: bold; height: 4em"
									>
										${
											response.subtask.assigned_to != null
												? `
												<div class="avatar" style="margin-right: 1em">
													<div class="mask mask-circle w-12 h-12">
													<img src="/static/img/users/profile${response.subtask.assigned_to}.jpg" alt="" />
													</div>
												</div>
													<span>${response.subtask.assigned_user.name} ${response.subtask.assigned_user.surname}</span>
												`
												: `<span>Not assigned</span>`
										}
									</div>
									<div class="dropdown">
										<label tabindex="0" class="btn m-1">
											<i style="margin-right:5px" class="fa-solid fa-user-check"></i>
											Change
										</label>
										<ul tabindex="0" class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
										${response.available_users
											.map(
												(available_user) => `
												<li onclick="assignSubtaskToUser(${response.subtask.id} ,${available_user.id})">
													<a>${available_user.name} ${available_user.surname}</a>
												</li>
											`
											)
											.join("")}
										</ul>
									</div>
								</div>
							</div>
						</div>
						
						<div class="mt-5 modal-action">
							<button class="btn btn-warning" onclick="deleteSubtask(${response.subtask.id})">
								<i style="margin-right:5px" class="fa-solid fa-trash-can"></i>
								Delete Subtask
							</button>
						</div>
					</div>
				</div>
			`);
			$(location).prop("href", "#subtask-detail-modal");
		})
		.fail((e) => {
			console.log(e);
			alert("error", e);
		});
};

const assignSubtaskToUser = (subtask_id, user_id) => {
	console.log(subtask_id, user_id);
	$.ajax({
		type: "PUT",
		url: "sprint",
		data: {
			subtask_id: subtask_id,
			assigned_to: user_id,
		},
	})
		.done((subtask) => {
			$("#subtask-detail-modal-assigned-user").html(`
				<div class="avatar" style="margin-right: 1em">
					<div class="mask mask-circle w-12 h-12">
					<img src="/static/img/users/profile${subtask.assigned_to}.jpg" alt="" />
					</div>
				</div>
				<span>${subtask.assigned_user.name} ${subtask.assigned_user.surname}</span>
			`);
			console.log("updated " + subtask.id + " assigned to " + user_id);
		})
		.fail((e) => {
			console.log(e);
			alert("error", e);
		});
};
