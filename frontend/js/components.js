async function carregarSidebar(){
    const sidebar     = document.getElementById("sidebar");
    const response    = await fetch("../components/sidebar.html");
    sidebar.innerHTML = await response.text();
}

carregarSidebar();