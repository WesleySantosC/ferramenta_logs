async function apiRequest(
    endpoint,
    options = {}
){

    const token = getToken();


    const headers = {

        "Content-Type":
            "application/json",

        ...options.headers

    };


    if(token){

        headers.Authorization =
            `Bearer ${token}`;

    }



    const response = await fetch(

        `${API}${endpoint}`,

        {
            ...options,
            headers
        }

    );



    const data =
        await response
        .json()
        .catch(() => null);



    if(!response.ok){

        throw new Error(
            data?.detail ||
            "Erro na requisição"
        );

    }


    return data;

}





/*
    DASHBOARD
*/


async function getStats(){

    return await apiRequest(
        "/logs/stats"
    );

}





/*
    LOGS
*/


async function getLogs(
    params = ""
){

    return await apiRequest(
        `/logs${params}`
    );

}





/*
    AUTH
*/


async function login(
    email,
    password
){

    return await apiRequest(
        "/auth/login",
        {

            method:"POST",

            body:JSON.stringify({

                email,
                password

            })

        }
    );

}





async function getCurrentUser(){

    return await apiRequest(
        "/auth/me"
    );

}