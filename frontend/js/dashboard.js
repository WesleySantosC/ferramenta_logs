document.addEventListener(
    "DOMContentLoaded",
    async()=>{


        if(!isAuthenticated()){

            window.location =
                "login.html";

            return;

        }


        await loadDashboard();


    }

);




async function loadDashboard(){


    try{


        const stats =
            await getStats();



        document.getElementById(
            "totalLogs"
        ).innerText =
            stats.total;



        document.getElementById(
            "errorLogs"
        ).innerText =
            stats.levels.ERROR || 0;



        document.getElementById(
            "warningLogs"
        ).innerText =
            stats.levels.WARN || 0;



        document.getElementById(
            "applications"
        ).innerText =
            Object.keys(
                stats.applications
            ).length;




        renderTimeline(
            stats
        );



        renderLevelChart(
            stats
        );



        renderApplicationsChart(
            stats
        );



    }
    catch(error){


        console.error(
            "Erro carregando dashboard:",
            error
        );


    }


}






function renderTimeline(stats){


    const container =
        document.getElementById(
            "timeline"
        );



    container.innerHTML = "";



    Object.entries(
        stats.services
    )
    .forEach(
        ([service,total])=>{


            container.innerHTML += `

                <div class="timeline-item">


                    <strong>
                        ${service}
                    </strong>


                    <span>
                        ${total} logs
                    </span>


                </div>

            `;


        }

    );


}







function renderLevelChart(stats){


    const ctx =
        document.getElementById(
            "logsLevelChart"
        );



    new Chart(
        ctx,
        {

            type:"doughnut",


            data:{


                labels:[

                    "INFO",
                    "WARN",
                    "ERROR"

                ],


                datasets:[{

                    data:[

                        stats.levels.INFO || 0,

                        stats.levels.WARN || 0,

                        stats.levels.ERROR || 0

                    ]

                }]


            },


            options:{


                responsive:true,


                plugins:{


                    legend:{


                        position:"bottom"


                    }


                }


            }


        }

    );


}








function renderApplicationsChart(stats){


    const ctx =
        document.getElementById(
            "applicationsChart"
        );



    const applications =
        stats.applications;



    new Chart(

        ctx,

        {


            type:"bar",


            data:{


                labels:

                    Object.keys(
                        applications
                    ),



                datasets:[{


                    label:
                    "Logs",


                    data:

                        Object.values(
                            applications
                        )


                }]


            },


            options:{


                responsive:true,


                scales:{


                    y:{


                        beginAtZero:true


                    }


                }


            }


        }

    );


}