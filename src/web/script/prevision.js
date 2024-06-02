var titlesPrevision = []
var prevision_future;
var prevision_simulations;
var prevision_chartHeight;
var prevision_hystorical_from;
var prevision_hystorical_to;
var prevision_view_from;

function runPrevision(titles){
    titlesPrevision = titles;
    openSimulationPanel();
    insertHtmlPrevision();
    setTimeout(()=>{
        updateVariablesPrevision();
        updatePrevision();
    },1);

}

function updateVariablesPrevision(){
    prevision_future = document.getElementById("prevision_future");
    prevision_simulations = document.getElementById("prevision_simulations");
    prevision_chartHeight = document.getElementById("prevision_chartHeight");
    prevision_hystorical_from = document.getElementById("prevision_hystorical_from");
    prevision_hystorical_to = document.getElementById("prevision_hystorical_to");
    prevision_view_from = document.getElementById("prevision_view_from");
    prevision_view_from.value = marketListCheck_from.value;
    prevision_hystorical_from.value = marketListCheck_from.value;
    prevision_hystorical_to.value = marketListCheck_to.value;
}

function insertHtmlPrevision(){
    simulationContent.innerHTML = `
    <div class="statsPageDataList" style="margin-left:20px;width:800px">
        <div class="flex">
            <div class="bd w-200">future data</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="100" type="number" class="form-control" id="prevision_future" onchange="updatePrevision();">
            </div>
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">simulations</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="1000" type="number" class="form-control" id="prevision_simulations" onchange="updatePrevision();">
            </div>
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">hystorical data</div>
            <div>from</div>
            <input type="date" id="prevision_hystorical_from" onchange="updatePrevision();" value="2019-01-01" min="1900-01-01"/>    
            <div class="bd w-200">to</div>
            <input type="date" id="prevision_hystorical_to" onchange="updatePrevision();" value="2019-01-01" min="1900-01-01"/>    
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">view from</div>
            <input type="date" id="prevision_view_from" onchange="updatePrevision();" value="1900-01-01" min="1900-01-01"/>    
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">charts height</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="400" type="number" class="form-control" id="prevision_chartHeight" onchange="updatePrevision();">
            </div>
        </div>
        
    </div>
    <div id="simulationChart" class="chart" style="height:700px"></div>
    `;
}


function updatePrevision(){
    document.getElementById("simulationChart").style.height = prevision_chartHeight.value +"px";

    eel.calculatePrevision(titlesPrevision[0], prevision_hystorical_from.value, prevision_hystorical_to.value, getIntervalValue(), getTypeValue(), parseInt(prevision_simulations.value), parseInt(prevision_future.value));
}

eel.expose(applyChartPrevision);
function applyChartPrevision(formattedDataOriginal, formattedDataPrevision){
    setTimeout(()=>{
        let tableOrgnl = new google.visualization.DataTable();
        tableOrgnl.addColumn('date', 'x');
        tableOrgnl.addColumn('number', "base data");
        let viewFromIndex = 0;
        let d = prevision_view_from.value.split("-");
        let viewFromTimestamp = new Date(d[0], d[1]-1, d[2]).getTime();
        for(let i=0;i<formattedDataOriginal.length;i++){
            if(formattedDataOriginal[i][0]*1000 < viewFromTimestamp)
                viewFromIndex++;
            formattedDataOriginal[i][0] = new Date(formattedDataOriginal[i][0]*1000);
        }
        formattedDataOriginal.splice(0,viewFromIndex);
        tableOrgnl.addRows(formattedDataOriginal);

        let tablePrvs = new google.visualization.DataTable();
        tablePrvs.addColumn('date', 'x');
        tablePrvs.addColumn('number', "montecarlo");
        tablePrvs.addColumn('number', "gbm");
        tablePrvs.addColumn('number', "heston");
        for(let i=0;i<formattedDataPrevision.length;i++){
            formattedDataPrevision[i][0] = new Date(formattedDataPrevision[i][0]*1000);
        }
        tablePrvs.addRows(formattedDataPrevision);

        let mergedData = google.visualization.data.join(tableOrgnl, tablePrvs, 'full', [[0, 0]], [1], [1,2,3]);

        let options = {
            hAxis: {
                title: "date"
            },
            vAxis: {
                title: "value"
            },
            title: "prevision"
        };
    
        let chart = new google.visualization.LineChart(document.getElementById("simulationChart"));
        chart.draw(mergedData, options);
    

    }, 1);
}

