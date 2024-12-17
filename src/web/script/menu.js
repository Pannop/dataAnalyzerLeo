
var containerWatchlists = document.getElementById("menu_containerWatchlists");
var containerPortfolios = document.getElementById("menu_containerPortfolios");



function drawMenuLineChart(data, elemId){
    let options={
        legend: {position: 'none'},
        'width':130,
        'height':120,
        'chartArea': {
            'width':130,
            'height':90,
            'backgroundColor': {
                'fill': '#FFFFFF',
                'opacity': 0
            },
        },
        'backgroundColor': {
            'fill': '#FFFFFF',
            'opacity': 0
        },
        'tooltip' : {
            trigger: 'none'
        },
        'enableInteractivity':false
    }
    let columns = []
    for(let i=1;i<data[0].length;i++)
        columns.push("")
    let dt = addChartDataTable(elemId, "line", columns, "", null, null, null, null, null, options);
    applyChart(data, dt)
}

function drawMenuPieChart(data, elemId){
    let options = {
        legend:'none',
        pieSliceText:'label'
    }
    let dt = addChartDataTable(elemId, "pie", [""], "", null, null, null, null, null, options)
    applyChart(data, dt);
}

function loadMenuData(){
    eel.loadMenuData()
}

eel.expose(applyMenuData);
function applyMenuData(data){
    try{
        containerPortfolios.innerHTML="";
        containerWatchlists.innerHTML="";
        for(let dashboard in data){
            let idChart = `menu_cardChart${dashboard.replaceAll(" ", "")}`
            let titlesNum = Object.keys(data[dashboard]["titles"]).length;
            let totPrice = 0;
            if(data[dashboard]["chart"].length>0){
                for(let i=1;i<data[dashboard]["chart"][0].length;i++){
                    totPrice+=data[dashboard]["chart"].at(-1)[i];
                }
            }
            
            totPrice=Math.round(totPrice);
            let card = `
            <div class="menu_card">
                    <p class="menu_cardTitle">${dashboard}</p>
                    <div class="menu_cardData">
                        <div class="menu_cardChart" id="${idChart}"></div>
                        <div class="menu_cardHover">
                            <div class="menu_cardHoverButtons">
                                <button class="btn btn-outline-dark"><i class="bi bi-pencil"></i></button>
                                <button class="btn btn-outline-dark"><i class="bi bi-trash"></i></button>
                            </div>
                            <p style="margin-top:15px"><b>titles</b>: ${titlesNum}</p>
                            <p><b>price</b>: ${totPrice}</p>
                        </div>
                    </div>
                    
                    <button class="btn btn-outline-dark menu_cardBottom"  onclick="loadDashboard('${dashboard}');">Open</button>
                </div>
            `;
            
            if(data[dashboard]["type"]=="portfolio"){
                containerPortfolios.innerHTML += card;
                let formattedData = []
                for(let title in data[dashboard]["titles"]){
                    let deltaPerc = data[dashboard]["titles"][title]["latestPrice"]/data[dashboard]["titles"][title]["initialPrice"] - 1
                    let lever = data[dashboard]["titles"][title]["lever"]
                    let actualCapital = data[dashboard]["titles"][title]["capital"] * (1 + deltaPerc*lever)
                    formattedData.push([title, actualCapital])
                }
                drawMenuPieChart(formattedData, idChart);
                
            }
            else if(data[dashboard]["type"]=="watchlist"){
                containerWatchlists.innerHTML += card;
                if(data[dashboard]["chart"].length>0)
                    drawMenuLineChart(data[dashboard]["chart"], idChart);    
            }
    
        }
    }
    catch(e){
        console.error(e);
    }
}


loadGoogleCharts(()=>{loadMenuData();});


function loadDashboard(dashboard){
    eel.loadDashboard(dashboard)
}

eel.expose(openDashboard);
function openDashboard(){
    location.pathname = '/start.html';
}



