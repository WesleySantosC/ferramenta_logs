document.addEventListener(
    "DOMContentLoaded",
    async()=>{


        if(!isAuthenticated()){

            window.location =
            "login.html";

            return;

        }


        await loadOrganizations();


    }
);





async function loadOrganizations(){


try{


const organizations =
await apiRequest(
    "/organizations"
);



renderOrganizations(
    organizations
);



}
catch(error){

console.error(
    "Erro carregando organizações:",
    error
);


}

}





function renderOrganizations(data){


const table =
document.getElementById(
    "organizationsTable"
);



table.innerHTML="";



data.forEach(org=>{


table.innerHTML += `


<tr>


<td>

${org.name}

</td>



<td>

${org.slug}

</td>



<td>

${formatDate(org.created_at)}

</td>



<td>


<button

class="action-btn delete-btn"

onclick="deleteOrganization(${org.id})">

Excluir

</button>


</td>



</tr>


`;


});


}





async function createOrganization(){


const name =
document
.getElementById(
"organizationName"
)
.value.trim();



const slug =
document
.getElementById(
"organizationSlug"
)
.value.trim();



if(!name || !slug){

alert(
"Preencha todos os campos"
);

return;

}



try{


await apiRequest(

"/organizations",

{

method:"POST",

body:JSON.stringify({

name,
slug

})

}

);



closeOrganizationModal();


await loadOrganizations();



}


catch(error){

alert(
error.message
);

}


}






async function deleteOrganization(id){


if(!confirm(
"Deseja remover esta organização?"
))
return;



try{


await apiRequest(

`/organizations/${id}`,

{

method:"DELETE"

}

);



await loadOrganizations();



}
catch(error){

alert(
error.message
);

}


}






function openOrganizationModal(){


document
.getElementById(
"organizationName"
)
.value="";



document
.getElementById(
"organizationSlug"
)
.value="";



document
.getElementById(
"organizationModal"
)
.classList
.remove("hidden");


}






function closeOrganizationModal(){


document
.getElementById(
"organizationModal"
)
.classList
.add("hidden");


}





function formatDate(date){


return new Date(date)
.toLocaleString(
"pt-BR"
);


}