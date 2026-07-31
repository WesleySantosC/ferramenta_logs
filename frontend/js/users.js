document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadUsers();


        const form =
            document.getElementById(
                "userForm"
            );


        if(form){

            form.addEventListener(
                "submit",
                createUser
            );

        }

    }
);





async function loadUsers(){

    try{


        const response =
            await apiRequest(
                "/users/"
            );



        const users = response.data || response;


        renderUsers(
            users
        );


    }catch(error){


        console.error(
            "Erro carregando usuários:",
            error
        );


    }

}








function renderUsers(users){


    const table =
        document.getElementById(
            "usersTable"
        );


    if(!table){

        return;

    }



    table.innerHTML = "";




    users.forEach(user => {


        table.innerHTML += `

        <tr>


            <td>
                ${user.name}
            </td>


            <td>
                ${user.email}
            </td>


            <td>

                <span class="badge">

                    ${user.role}

                </span>

            </td>



            <td>

                ${
                    user.active

                    ?

                    `
                    <span class="status active">
                        Ativo
                    </span>
                    `

                    :

                    `
                    <span class="status inactive">
                        Inativo
                    </span>
                    `

                }

            </td>



            <td>


                <button

                    class="btn-danger"

                    onclick="deleteUser(${user.id})">


                    Excluir


                </button>


            </td>



        </tr>

        `;


    });


}








async function createUser(event){

    event.preventDefault();




    const data = {


        name:

            document
            .getElementById(
                "newUserName"
            )
            .value,



        email:

            document
            .getElementById(
                "newUserEmail"
            )
            .value,



        password:

            document
            .getElementById(
                "newUserPassword"
            )
            .value,



        role:

            document
            .getElementById(
                "newUserRole"
            )
            .value


    };

    try{


        await apiRequest(

            "/users/",

            {

                method:"POST",

                body:
                    JSON.stringify(
                        data
                    )

            }

        );




        closeUserModal();



        document
            .getElementById(
                "userForm"
            )
            .reset();




        await loadUsers();




        alert(
            "Usuário criado com sucesso!"
        );



    }
    catch(error){


        console.error(
            "Erro criando usuário:",
            error
        );


        alert(
            error.message
        );


    }


}









async function deleteUser(id){


    if(
        !confirm(
            "Deseja remover este usuário?"
        )
    ){

        return;

    }




    try{


        await apiRequest(

            `/users/${id}`,

            {

                method:"DELETE"

            }

        );



        await loadUsers();



    }catch(error){


        alert(
            error.message
        );


    }


}







function openUserModal(){


    document

        .getElementById(
            "userModal"
        )

        .classList

        .add(
            "active"
        );


}







function closeUserModal(){


    document

        .getElementById(
            "userModal"
        )

        .classList

        .remove(
            "active"
        );


}