let levelChart;
let serviceChart;

async function carregarDashboard(){
    const stats = await getStats();

    document.getElementById("totalLogs").innerText   = stats.total;
    document.getElementById("infoLogs").innerText    = stats.levels.INFO || 0;
    document.getElementById("warningLogs").innerText = stats.levels.WARN || 0;
    document.getElementById("errorLogs").innerText   = stats.levels.ERROR || 0;

    renderCharts(stats);
    carregarUltimosLogs();
}

async function carregarUltimosLogs(){
    const dados  = await getLogs("?limit=8");
    const tabela = document.getElementById("logsTable");

    tabela.innerHTML = "";

    dados.data.forEach(log => {
        tabela.innerHTML += `
        <tr>
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

function renderCharts(stats){
    const levelCtx =
        document.getElementById("levelChart");

    if(levelChart)
        levelChart.destroy();

    levelChart = new Chart(levelCtx, {
        type:"doughnut",

        data:{
            labels:Object.keys(stats.levels),

            datasets:[{
                data:Object.values(stats.levels)
            }]
        }
    });

    const serviceCtx = document.getElementById("serviceChart");

    if(serviceChart)
        serviceChart.destroy();

    serviceChart = new Chart(serviceCtx,{
        type:"bar",
        data:{
            labels:Object.keys(stats.services),
            datasets:[{
                label:"Quantidade",
                data:Object.values(stats.services)
            }]
        }
    });
}

carregarDashboard();

setInterval(()=>{
    carregarDashboard();
},5000);