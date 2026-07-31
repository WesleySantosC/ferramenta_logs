document.addEventListener(
    "DOMContentLoaded",

    () => {
        const path =
            window.location.pathname;

        const loginPage =
            path.includes("login.html");

        if(!isAuthenticated() && !loginPage){
            Router.login();
            return;
        }

        if(isAuthenticated() && loginPage){
            Router.dashboard();
        }
    }
);