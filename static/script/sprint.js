const updateSubtask = (subtask_id, new_status) => {
	$.ajax({
		type: "POST",
		url: "sprint",
		data: {
			subtask_id: subtask_id,
			new_status: new_status,
		},
	})
		.done(function () {})
		.fail(function (e) {
			console.log(e);
			alert("error", e);
		});
	console.log(subtask_id, new_status);
};
