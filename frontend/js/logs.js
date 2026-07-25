let filtroAtual  = "";
let paginaAtual  = 1;
const limiteLogs = 15;

const paginationLogs = new Pagination({
    container:"#logsPagination",
    
    page:1,

    limit:limiteLogs,
    total:0,

    onChange:(page)=>{
        paginaAtual = page;
        carregarLogs();
    }
});

async function carregarLogs(){
    let params = filtroAtual;

    if(params){
        params += "&";
    }else{
        params = "?";
    }

    params += `page=${paginaAtual}&limit=${limiteLogs}`;

    const dados = await getLogs(params);

    preencherTabela(dados);

    paginationLogs.update(
        dados.total,
        dados.page
    );
}

async function filtrarLogs(){
    let params        = "?";
    const search      = document.getElementById("search").value;
    const level       = document.getElementById("level").value;
    const service     = document.getElementById("service").value;
    const application = document.getElementById("application").value;

    if(search)
        params += `search=${search}&`;


    if(level)
        params += `level=${level}&`;


    if(service)
        params += `service=${service}&`;


    if(application)
        params += `application=${application}&`;

    filtroAtual = params;
    paginaAtual = 1;

    carregarLogs();
}

function preencherTabela(dados){
    const tabela = document.getElementById("logsTable");

    tabela.innerHTML="";

    dados.data.forEach(log=>{
        tabela.innerHTML += `
        <tr onclick='abrirDetalhe(${JSON.stringify(log)})'>
            <td>${log.created_at}</td>
            <td>${log.application}</td>
            <td>${log.service}</td>
            <td>
                <span class="level ${log.level.toLowerCase()}">
                    ${log.level}
                </span>
            </td>
            <td>${log.message}</td>
        </tr>
        `;
    });
}

function abrirDetalhe(log){
    document.getElementById("logDetails").textContent = JSON.stringify(log,null,4);
    document.getElementById("logModal").style.display = "block";
}

function fecharModal(){
    document.getElementById("logModal").style.display="none";
}

carregarLogs();

setInterval(()=>{

    carregarLogs();

},5000);