var alert_volumePerc;
var alert_valuePerc;
var alert_minVolume;

function runAlert(){
    openSimulationPanel();
    insertHtmlAlert();
    setTimeout(()=>{
        updateVariablesAlert();
        updateAlert();
    },1);

}

function updateVariablesAlert(){
    alert_volumePerc = document.getElementById("alert_volumePerc");
    alert_valuePerc = document.getElementById("alert_valuePerc");
    alert_minVolume = document.getElementById("alert_minVolume");
}

function insertHtmlAlert(){
    simulationContent.innerHTML = `
    <div class="statsPageDataList" style="margin-left:20px;width:800px">
        <div class="flex">
            <div class="bd w-200">volume percentage delta</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="20" type="number" class="form-control" id="alert_volumePerc" onchange="updateAlert();">
            </div>
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">value percentage delta</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="5" type="number" class="form-control" id="alert_valuePerc" onchange="updateAlert();">
            </div>
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">minimum volume difference</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="5" type="number" class="form-control" id="alert_minVolume" onchange="updateAlert();">
            </div>
        </div>
        <table class="table table-striped mt-4" id="simulationTable">
        </table>
    </div>
    `;
}


function updateAlert(){
    eel.checkAlert(parseFloat(alert_volumePerc.value), parseFloat(alert_valuePerc.value), parseInt(alert_minVolume.value))
}

eel.expose(applyAlertTable);
function applyAlertTable(alerts){
    let table = document.getElementById("simulationTable");
    let html=`
    <tr>
        <th scope="col">Title</th>
        <th scope="col">Volume Delta</th>
        <th scope="col">Value Delta</th>         
    </tr>
    `;
    alerts.forEach(a => {
        html+=`
        <tr>
            <th scope="row">${a["symbol"]}</th>
            <td>${a["volumeDeltaPerc"]}</td>
            <td>${a["valueDeltaPerc"]}</td>
        </tr>
        `;
    });
    table.innerHTML=html;
}

