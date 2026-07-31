document.addEventListener(
    "DOMContentLoaded",
    async()=>{


        if(!isAuthenticated()){

            window.location =
            "login.html";

            return;

        }


        await loadTokens();


    }
);



async function loadTokens(){


    try{


        const response =
        await apiRequest(
            "/tokens"
        );


        renderTokens(
            response.data
        );


    }
    catch(error){

        console.error(
            "Erro carregando tokens:",
            error
        );

    }

}





function renderTokens(tokens){


const table =
document.getElementById(
"tokensTable"
);



table.innerHTML="";



if(tokens.length === 0){


table.innerHTML = `

<tr>

<td colspan="6">

Nenhum token encontrado

</td>

</tr>

`;

return;


}



tokens.forEach(token=>{


table.innerHTML += `


<tr>


<td>
${token.name}
</td>


<td>
${token.application}
</td>


<td>
${token.project_id}
</td>



<td>

<span class="status ${token.active ? "active":"inactive"}">

${token.active ? "Ativo":"Inativo"}

</span>


</td>



<td>

${formatDate(token.created_at)}

</td>



<td>


<button

class="action-btn delete-btn"

onclick="deleteToken(${token.id})">

Excluir

</button>


</td>



</tr>


`;


});


}






async function createToken(){


const name =
document
.getElementById(
"tokenName"
)
.value.trim();



const project_id =
Number(
document
.getElementById(
"projectId"
)
.value
);



if(!name || !project_id){

alert(
"Informe nome e projeto"
);

return;

}




try{


const response =
await apiRequest(
"/tokens",
{

method:"POST",

body:JSON.stringify({

name,
project_id

})

}

);



document
.getElementById(
"tokenValue"
)
.innerText =
response.token;



document
.getElementById(
"generatedToken"
)
.classList
.remove("hidden");



document
.getElementById(
"createTokenButton"
)
.classList
.add("hidden");



await loadTokens();



}


catch(error){

alert(
error.message
);

}


}







async function deleteToken(id){


if(!confirm(
"Deseja remover este token?"
))
return;



try{


await apiRequest(

`/tokens/${id}`,

{

method:"DELETE"

}

);



await loadTokens();


}


catch(error){

alert(
error.message
);

}


}







function openTokenModal(){


document
.getElementById(
"tokenName"
)
.value="";



document
.getElementById(
"projectId"
)
.value="";



document
.getElementById(
"generatedToken"
)
.classList
.add("hidden");



document
.getElementById(
"createTokenButton"
)
.classList
.remove("hidden");



document
.getElementById(
"tokenModal"
)
.classList
.remove("hidden");


}





function closeTokenModal(){


document
.getElementById(
"tokenModal"
)
.classList
.add("hidden");


}





function copyToken(){


const token =
document
.getElementById(
"tokenValue"
)
.innerText;



navigator
.clipboard
.writeText(token);



alert(
"Token copiado"
);


}






function formatDate(date){


return new Date(date)
.toLocaleString(
"pt-BR"
);


}