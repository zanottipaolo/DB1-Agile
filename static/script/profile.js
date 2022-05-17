function enableUpdate(){
    document.getElementById('current_name').disabled = false;
    document.getElementById('current_surname').disabled = false;
    document.getElementById('current_email').disabled = false;
    document.getElementById('current_password').disabled = false;
    document.getElementById('current_manager').disabled = false;
}

function disableUpdate(){
    document.getElementById('current_name').disabled = true;
    document.getElementById('current_surname').disabled = true;
    document.getElementById('current_email').disabled = true;
    document.getElementById('current_password').disabled = true;
    document.getElementById('current_manager').disabled = true;
}