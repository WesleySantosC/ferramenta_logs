function saveToken(token){

    localStorage.setItem(
        "token",
        token
    );

}


function getToken(){

    return localStorage.getItem(
        "token"
    );

}


function removeToken(){

    localStorage.removeItem(
        "token"
    );

    localStorage.removeItem(
        "user"
    );

}


function saveUser(user){

    localStorage.setItem(
        "user",
        JSON.stringify(user)
    );

}


function getUser(){

    const user =
        localStorage.getItem(
            "user"
        );


    if(!user){

        return null;

    }


    return JSON.parse(user);

}


function isAuthenticated(){

    return !!getToken();

}