let projects = [];


document.addEventListener(
"DOMContentLoaded",
async()=>{


    if(!isAuthenticated()){

        window.location =
        "login.html";

        return;

    }


    setupEvents();

    await loadProjects();


});



async function loadProjects(){


    try{


        projects =
        await apiRequest(
            "/projects/"
        );


        renderProjects();


    }catch(error){

        console.error(
            "Erro carregando projetos:",
            error
        );

    }


}



function renderProjects(){


const tbody =
document.getElementById(
"projectsTable"
);



tbody.innerHTML="";



projects.forEach(project=>{


tbody.innerHTML += `

<tr>


<td>
${project.name}
</td>


<td>
${project.description ?? "-"}
</td>



<td>

<span class="badge ${
project.active 
? "success"
: "error"
}">

${project.active
? "Ativo"
: "Inativo"}

</span>


</td>



<td>


<button
class="btn-small"
onclick="editProject(${project.id})">

Editar

</button>


<button
class="btn-small danger"
onclick="deleteProject(${project.id})">

Excluir

</button>


</td>


</tr>


`;


});


}




function setupEvents(){


document
.getElementById(
"btnNewProject"
)
.onclick=()=>openModal();



document
.getElementById(
"closeModal"
)
.onclick=closeModal;



document
.getElementById(
"projectForm"
)
.addEventListener(
"submit",
saveProject
);


}




function openModal(project=null){


document
.getElementById(
"projectModal"
)
.classList.remove(
"hidden"
);



if(project){


document.getElementById(
"modalTitle"
)
.innerText =
"Editar Projeto";


document.getElementById(
"projectId"
)
.value =
project.id;



document.getElementById(
"projectName"
)
.value =
project.name;



document.getElementById(
"projectDescription"
)
.value =
project.description ?? "";


document.getElementById(
"projectActive"
)
.checked =
project.active;



}else{


document
.getElementById(
"projectForm"
)
.reset();


}



}




function closeModal(){


document
.getElementById(
"projectModal"
)
.classList.add(
"hidden"
);


}




async function saveProject(event){


event.preventDefault();



const id =
document.getElementById(
"projectId"
).value;



const data={


name:
document.getElementById(
"projectName"
).value,


description:
document.getElementById(
"projectDescription"
).value,


active:
document.getElementById(
"projectActive"
).checked


};



try{


if(id){


await apiRequest(
`/projects/${id}`,
{

method:"PUT",

body:
JSON.stringify(data)

}

);



}else{


await apiRequest(
"/projects/",
{

method:"POST",

body:
JSON.stringify(data)

}

);



}


closeModal();

await loadProjects();



}catch(error){


alert(
error.message
);


}



}



function editProject(id){


const project =
projects.find(
p=>p.id===id
);


openModal(project);


}




async function deleteProject(id){


if(
!confirm(
"Excluir projeto?"
)
)
return;



try{


await apiRequest(
`/projects/${id}`,
{

method:"DELETE"

}

);



await loadProjects();



}catch(error){


alert(
error.message
);


}


}