var alert_volumePerc;
var alert_valuePerc;
var alert_minVolume;
var alert_minVolumePrice;
var alert_regionMenu;
var alert_results;

function runAlert(){
    openSimulationPanel();
    insertHtmlAlert();
    setTimeout(()=>{
        updateVariablesAlert();
        //updateAlert();
    },1);

}

var regionsNames = ['Argentina', 'Australia', 'Austria', 'Belgium', 'Brazil', 'Canada', 'Chile', 'China', 'Czechia', 'Denmark', 'Egypt', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hong Kong SAR China', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Kuwait', 'Latvia', 'Lithuania', 'Malaysia', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Suriname', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'United Kingdom', 'United States', 'Venezuela', 'Vietnam']
var regionsNamesEurope = ['Austria', 'Belgium', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'United Kingdom'];
var regionsNamesAsia = ['China', 'Hong Kong SAR China', 'India', 'Indonesia', 'Japan', 'Kuwait', 'Malaysia', 'Philippines', 'Qatar', 'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka', 'Thailand', 'Turkey', 'Vietnam'];

function clickRegionAlert(region, forceCheck=false){
    if(region=="europe"){
        for(let r of regionsNamesEurope)
            clickRegionAlert(r, true);
    }
    else if(region=="asia"){
        for(let r of regionsNamesAsia)
            clickRegionAlert(r, true);
    }
    else if(region=="all"){
        for(let r of regionsNames)
            clickRegionAlert(r, true);
    }
    else if(region=="none"){
        for(let r of regionsNames){
            clickRegionAlert(r, true);
            clickRegionAlert(r);
        }
    }
    else{
        let elem = document.getElementById("alert_regionMenu_"+region);
        if(forceCheck)
            elem.checked = true;
        else
            elem.checked = !elem.checked;
    }

}

function getSelectedRegions(){
    let selected = [];
    for(let r of regionsNames){
        let elem = document.getElementById("alert_regionMenu_"+r);
        if(elem.checked)
            selected.push(r);
    }
    return selected;
}

function updateVariablesAlert(){
    alert_volumePerc = document.getElementById("alert_volumePerc");
    alert_valuePerc = document.getElementById("alert_valuePerc");
    alert_minVolume = document.getElementById("alert_minVolume");
    alert_minVolumePrice = document.getElementById("alert_minVolumePrice");
    alert_regionMenu = document.getElementById("alert_regionMenu");
    alert_results = document.getElementById("alert_results");
    alert_regionMenu.style.display="none";
    let regMenuHtml = "";
    for(let i =0;i<regionsNames.length;i+=4){
        regMenuHtml+=`<div class="flex">`;
        for(let j=0;j<4;j++){
            regMenuHtml+=`  
            <div class="form-check regionCheckBox">
                <input id="alert_regionMenu_${regionsNames[i+j]}" class="form-check-input" type="checkbox" value="">
                <label class="form-check-label" onclick="clickRegionAlert('${regionsNames[i+j]}')">
                ${regionsNames[i+j]}
                </label>
            </div>`;
        }

        regMenuHtml+="</div>";
        
    }
    regMenuHtml+=`
            <hr/>
            <div class="flex">
                <button class="btn btn-outline-dark" onclick="clickRegionAlert('europe');">Europe</button>
                <button class="btn btn-outline-dark" onclick="clickRegionAlert('asia');">Asia</button>
                <button class="btn btn-outline-dark" onclick="clickRegionAlert('all');">All</button>
                <button class="btn btn-outline-dark" onclick="clickRegionAlert('none');">None</button>

            </div>
    `;
    alert_regionMenu.innerHTML = regMenuHtml;
}

var titleRegionsAlertOpen=0;
function clickRegionsListAlert(){
    if(titleRegionsAlertOpen){
        alert_regionMenu.style.display = "none";
    }
    else{
        alert_regionMenu.style.display = "block";
    }
    titleRegionsAlertOpen=Math.abs(titleRegionsAlertOpen-1);
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
            <div class="bd w-200">minimum average volume</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="50" type="number" class="form-control" id="alert_minVolume" onchange="updateAlert();">
            </div>
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">minimum volume price</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="1000" type="number" class="form-control" id="alert_minVolumePrice" onchange="updateAlert();">
            </div>
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">results</div>
            <div class="input-group mb-1">
                <input disabled style="height: 30px;" value="0" type="number" class="form-control" id="alert_results">
            </div>
        </div>
        <hr>
        <div class="flex" style="justify-content:flex-start">
            <div class="dropdown show" onclick="clickRegionsListAlert();">
                <a class="btn btn-secondary dropdown-toggle" href="#" role="button"  data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Regions</a>
            </div>
            <div style="position:relative">
                <div id="alert_regionMenu"></div>
            </div>       
        </div>
        <hr>
        <div class="flex">
            <button class="btn btn-outline-dark" onclick="updateAlert();">Load Alerts</button>
            <div class="progress" style="width:80%">
                <div id="simulationProgressBar" class="progress-bar progress-bar-striped bg-info" role="progressbar" style="width: 0" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
        </div>
        <table class="table table-striped mt-4" id="simulationTable">
        </table>
    </div>
    `;
}


function updateAlert(){
    eel.checkAlert(parseFloat(alert_volumePerc.value), parseFloat(alert_valuePerc.value), parseInt(alert_minVolume.value), parseInt(alert_minVolumePrice.value), getSelectedRegions(), "simulationProgressBar");
}

eel.expose(applyAlertTable);
function applyAlertTable(alerts){
    let table = document.getElementById("simulationTable");
    
    let html=`
    <tr>
        <th scope="col">Title</th>
        <th scope="col">Symbol</th>
        <th scope="col">Volume Delta</th>
        <th scope="col">Value Delta</th>         
        <th scope="col">Volume Price</th>         
        <th scope="col">Region</th>         
        <th scope="col">Market State</th>         
    </tr>
    `;
    alerts.forEach(a => {
        html+=`
        <tr>
            <th scope="row">${a["name"]}</th>
            <td class="clickable" onclick="window.open('https://it.finance.yahoo.com/quote/${a["symbol"]}/','name')">${a["symbol"]}</td>
            <td>${a["volumeDeltaPerc"]} %</td>
            <td>${a["valueDeltaPerc"]} %</td>
            <td>${a["volumePrice"]} $</td>
            <td>${a["region"]}</td>
            <td>${a["marketState"]}</td>
        </tr>
        `;
    });
    table.innerHTML=html;
    alert_results.value = alerts.length;
}

