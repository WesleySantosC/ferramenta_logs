let currentPage = 1;


let filters = {

    level:"",
    application:"",
    search:""

};





document.addEventListener(
"DOMContentLoaded",
()=>{


    document
    .getElementById("filterButton")
    ?.addEventListener(
    "click",
    ()=>{


        filters.level =
        document.getElementById(
            "level"
        ).value;



        filters.application =
        document.getElementById(
            "application"
        ).value;



        filters.search =
        document.getElementById(
            "search"
        ).value;



        currentPage = 1;


        loadLogs();


    });





    document
    .getElementById("nextPage")
    ?.addEventListener(
    "click",
    ()=>{

        currentPage++;

        loadLogs();

    });





    document
    .getElementById("prevPage")
    ?.addEventListener(
    "click",
    ()=>{


        if(currentPage > 1){

            currentPage--;

            loadLogs();

        }


    });





    document
    .getElementById("closeLogModal")
    ?.addEventListener(
    "click",
    ()=>{


        document
        .getElementById("logModal")
        .classList.remove(
            "active"
        );


    });





    loadLogs();


});







async function loadLogs(){


    try{


        let params =
        new URLSearchParams();



        params.append(
            "page",
            currentPage
        );


        params.append(
            "limit",
            50
        );



        if(filters.level){

            params.append(
                "level",
                filters.level
            );

        }



        if(filters.application){

            params.append(
                "application",
                filters.application
            );

        }



        if(filters.search){

            params.append(
                "search",
                filters.search
            );

        }




        const response =
        await getLogs(
            `?${params.toString()}`
        );



        renderLogs(
            response.data
        );


        updatePagination(
            response
        );



    }catch(error){


        console.error(
            "Erro carregando logs:",
            error
        );


    }


}








function renderLogs(logs){


    const tbody =
    document.getElementById(
        "logsTable"
    );


    if(!tbody)
        return;



    tbody.innerHTML="";




    logs.forEach(
    log=>{


        tbody.innerHTML += `


        <tr
        class="log-row"
        onclick='openLogDetails(${JSON.stringify(log)})'>


            <td>

                <span class="
                level
                level-${log.level.toLowerCase()}
                ">

                ${log.level}

                </span>

            </td>



            <td>
                ${log.application}
            </td>



            <td>
                ${log.service}
            </td>



            <td>
                ${log.message}
            </td>



            <td>
                ${log.environment}
            </td>



            <td>
                ${formatDate(log.created_at)}
            </td>



        </tr>


        `;


    });


}







function openLogDetails(log){


    const modal =
    document.getElementById(
        "logModal"
    );


    const details =
    document.getElementById(
        "logDetails"
    );



    details.innerHTML = `



    <div class="log-detail-item">

        <div class="log-detail-label">
        Level
        </div>

        <div class="log-detail-value">
        ${log.level}
        </div>

    </div>





    <div class="log-detail-item">

        <div class="log-detail-label">
        Application
        </div>

        <div class="log-detail-value">
        ${log.application}
        </div>

    </div>





    <div class="log-detail-item">

        <div class="log-detail-label">
        Service
        </div>

        <div class="log-detail-value">
        ${log.service}
        </div>

    </div>





    <div class="log-detail-item">

        <div class="log-detail-label">
        Request ID
        </div>

        <div class="log-detail-value">
        ${log.request_id ?? "-"}
        </div>

    </div>





    <div class="log-detail-item">

        <div class="log-detail-label">
        Mensagem
        </div>

        <div class="log-detail-value">
        ${log.message}
        </div>

    </div>





    <div class="log-detail-item">

        <div class="log-detail-label">
        Context
        </div>


        <pre class="log-context">

${JSON.stringify(
    log.context,
    null,
    2
)}

        </pre>


    </div>



    `;



    modal.classList.add(
        "active"
    );


}








function updatePagination(data){


    document
    .getElementById("pageInfo")
    .innerText =

    `${data.page} de ${Math.ceil(data.total/data.limit)}`;


}







function formatDate(date){

    return new Date(date)
    .toLocaleString(
        "pt-BR"
    );

}