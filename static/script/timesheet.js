function openModal(id_developer, day) {
    console.log("MODAL: " + id_developer + ", " + day)

    var modal = document.getElementById('workInfo');
    document.getElementById("title_workInfo").innerHTML = "Log time: " + day;
    document.getElementById("user").value = id_developer;
    document.getElementById("date").value = day;
    modal.classList.remove("hidden");
};

function closeModal() {
    var modal = document.getElementById("workInfo");
    modal.classList.add('hidden');
}