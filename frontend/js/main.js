const button = document.getElementById("connect");

button.addEventListener("click", async () => {
    const token = document.getElementById("token").value;
    
    saveToken(token);

    window.location = "pages/dashboard.html";

});