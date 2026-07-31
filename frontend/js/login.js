document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById(
                "loginForm"
            );

        if(!form){
            return;
        }

        form.addEventListener(
            "submit",
            async(event)=>{

                event.preventDefault();

                const email =
                    document.getElementById(
                        "email"
                    ).value;

                const password =
                    document.getElementById(
                        "password"
                    ).value;

                const button =
                    document.querySelector(
                        "button[type='submit']"
                    );

                try{

                    button.disabled = true;

                    button.innerText =
                        "Entrando...";

                    const response =
                        await login(
                            email,
                            password
                        );

                    saveToken(
                        response.access_token
                    );

                    const user = await getCurrentUser();

                    saveUser(
                        user
                    );

                    window.location = "dashboard.html";

                }catch(error){

                    alert(
                        error.message
                    );

                    removeToken();

                }finally{
                    button.disabled = false;
                    button.innerText =
                        "Entrar";
                }
            }
        );
    }
);