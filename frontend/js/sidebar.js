const MENU = [

    {
        title: "Dashboard",
        icon: "layout-dashboard",
        page: "dashboard.html"
    },

    {
        title: "Logs",
        icon: "file-text",
        page: "logs.html"
    },

    {
        title: "Tokens",
        icon: "key-round",
        page: "tokens.html"
    },

    {
        title: "Organizações",
        icon: "building-2",
        page: "organizations.html"
    },

    {
        title: "Projetos",
        icon: "folder-kanban",
        page: "projects.html"
    },

    {
        title: "Usuários",
        icon: "users",
        page: "users.html"
    }

];

document.addEventListener(

    "DOMContentLoaded",

    async () => {

        await loadComponent(
            "sidebar",
            "sidebar.html"
        );

        await loadComponent(
            "header",
            "header.html"
        );

        loadUserHeader();

        createSidebar();

        activateCurrentMenu();

        document

            .getElementById("logoutButton")

            .addEventListener(

                "click",

                logout

            );

    }

);

function createSidebar(){

    const nav =
        document.getElementById(
            "sidebarMenu"
        );

    MENU.forEach(item => {

        nav.innerHTML += `

            <a
                href="${item.page}"
                class="menu-item">

                <i
                    data-lucide="${item.icon}">
                </i>

                <span>

                    ${item.title}

                </span>

            </a>

        `;

    });

    lucide.createIcons();

}

function activateCurrentMenu(){

    const page =
        location.pathname
        .split("/")
        .pop();

    document

        .querySelectorAll(".menu-item")

        .forEach(item => {

            item.classList.remove("active");

            if(item.getAttribute("href") === page){

                item.classList.add("active");

            }

        });

}

function logout(){

    removeToken();

    window.location =
        "login.html";
}

function loadUserHeader(){

    const user =
        getUser();

    if(!user){
        return;
    }

    const name =
        document.getElementById(
            "userName"
        );

    const role =
        document.getElementById(
            "userRole"
        );

    const avatar =
        document.querySelector(
            ".avatar"
        );

    if(name){
        name.innerText =
            user.name;
    }

    if(role){
        role.innerText =
            user.role;
    }

    if(avatar){
        avatar.innerText =
            user.name
            .charAt(0)
            .toUpperCase();
    }
}