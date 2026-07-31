const Router = {
    go(page){
        window.location.href = page;
    },

    login(){
        this.go("login.html");
    },

    dashboard(){
        this.go("dashboard.html");
    }
};