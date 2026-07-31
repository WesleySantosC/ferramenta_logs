async function loadModal(){

    await loadComponent(
        "modal",
        "modal.html"
    );

    document
        .getElementById("modalClose")
        .addEventListener(
            "click",
            closeModal
        );

}

function openModal(
    title,
    content
){

    document
        .getElementById("modalTitle")
        .innerHTML = title;

    document
        .getElementById("modalBody")
        .innerHTML = content;

    document
        .getElementById("modalOverlay")
        .classList.add(
            "active"
        );

}

function closeModal(){

    document
        .getElementById("modalOverlay")
        .classList.remove(
            "active"
        );

}