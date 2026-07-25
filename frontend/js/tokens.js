let tokenAtual     ="";
let paginaTokens   = 1;
const limiteTokens = 19;

const paginationTokens = new Pagination({
    container:"#tokensPagination",

    page:1,

    limit:limiteTokens,

    total:0,

    onChange:(page)=>{
        paginaTokens = page;
        carregarTokens();
    }
});

async function criarToken(){

    const name        = document.getElementById("tokenName").value.trim();
    const application = document.getElementById("application").value.trim();

    if(!name || !application){
        alert("Preencha nome e aplicação.");
        return;
    }

    const response = await fetch(
        API + `/tokens?name=${encodeURIComponent(name)}&application=${encodeURIComponent(application)}`,
        {
            method:"POST"
        }
    );

    const data = await response.json();
    tokenAtual = data.token;

    document.getElementById("tokenValue").textContent   = data.token;
    document.getElementById("tokenModal").classList.add("open");
    
    carregarTokens();
}

async function carregarTokens(){
    const response = await fetch(
        API + `/tokens?page=${paginaTokens}&limit=${limiteTokens}`
    );

    const dados  = await response.json();
    const tabela = document.getElementById("tokensTable");

    tabela.innerHTML="";

    dados.data.forEach(token=>{
        tabela.innerHTML += `
        <tr>
            <td>${token.id}</td>
            <td>${token.name}</td>
            <td>${token.application}</td>
            <td>${token.created_at}</td>
            <td>
                <button onclick="deletarToken(${token.id})">Excluir</button>
            </td>
        </tr>
        `;
    });

    paginationTokens.update(
        dados.total,
        dados.page
    );

}

async function deletarToken(id){

    if(!confirm("Deseja remover este token?"))
        return;

    const response =
        await fetch(
            API + `/tokens/${id}`,
            {
                method:"DELETE"
            }
        );

    if(response.ok){
        carregarTokens();
    }
}

async function copiarNovoToken() {
    if (!navigator.clipboard) {
        alert("Seu navegador não suporta a API de área de transferência nesta página.");
        return;
    }

    await navigator.clipboard.writeText(tokenAtual);
    alert("Token copiado!");
}

function fecharModalToken() {
    document.getElementById("tokenModal").classList.remove("open");
}

carregarTokens();