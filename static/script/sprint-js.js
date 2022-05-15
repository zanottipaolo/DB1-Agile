// DRAG && DROP

function onDragStart(event) {
    event.dataTransfer.setData('text/plain', event.target.id);
}

function onDragOver(event) {
    event.preventDefault();
}

function onDrop(event, element) {
    event.preventDefault();

    const id = event.dataTransfer.getData('text');
    const draggableElement = document.getElementById(id);

    element.appendChild(draggableElement);

    event.dataTransfer.clearData();
}