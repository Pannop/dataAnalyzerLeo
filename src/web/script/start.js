var marketListChecks = document.getElementById("marketListChecks");
var marketListCheck_interval = document.getElementById("marketListCheck_interval");
var marketListCheck_type = document.getElementById("marketListCheck_type");
var marketListCheck_from = document.getElementById("marketListCheck_from");
var marketListCheck_to = document.getElementById("marketListCheck_to");
var marketListCheck_sections = document.getElementById("marketListCheck_sections");
var statsPageContainer = document.getElementById("statsPageContainer");
var comparisonTitle1 = document.getElementById("comparisonTitle1");
var comparisonTitle2 = document.getElementById("comparisonTitle2");
var comparisonRatio = document.getElementById("comparisonRatio");
var correlationTable = document.getElementById("correlationTable");
var correlationValidTitles = document.getElementById("correlationValidTitles");
var correlationTriangular = document.getElementById("correlationTriangular");
var correlationExport = document.getElementById("correlationExport");


var marketStatus;

var REALTIME_UPDATE_MILLIS = 5*60*1000

var TAG_RATIO = "ratio";
var TAG_SUM_PREC = "sumprec";
var TAG_SCALED = "scaled";
var TAG_SAME_START = "samestart";
var TAG_AVERAGE_LINE = "averageline";

var baseData = null;

eel.expose(setSize);
function setSize(width, height) {

    let html = document.getElementById("html");
    //html.style.width = `${width}px`;
    //html.style.height = `${height}px`;
    window.resizeTo(width, height);
}


function setMarketList(marketList) {
    addMarketCheckBox = (name) => {
        return `
        <div class="form-check">
            <input class="form-check-input" type="checkbox" id="marketListCheck_${name}" value="${name}" onchange="updateStatistics();">
            <label class="form-check-label">
                ${name}
            </label>
        </div>
        `
    }
    str = "";
    for (let i = 0; i < marketList.length; i++) {
        str += addMarketCheckBox(marketList[i]);
    }
    marketListChecks.innerHTML = str;
    document.getElementById(`marketListCheck_${marketList[0]}`).checked = true;
}

function setComparisonList(marketList){
    addOption = (name) => {
        return `
        <option value="${name}">${name}</option>
        `
    }
    str = "";
    for (let i = 0; i < marketList.length; i++) {
        str += addOption(marketList[i]);
    }
    comparisonTitle1.innerHTML = str;
    comparisonTitle2.innerHTML = str;
}

eel.expose(setTitles);
function setTitles(data) {
    try{
        baseData = data;
        setMarketList(baseData["marketList"]);
        setComparisonList(baseData["marketList"]);
        updateStatistics();
    }
    catch(e){
        console.error(e);
    }
}



function startApp(){
    eel.setDefaultSize();
    eel.loadTitles();
}


loadGoogleCharts(()=>{startApp();});




function getSelectedMarkets() {
    selected = [];
    checks = marketListChecks.children;
    for (let i = 0; i < checks.length; i++) {
        if (checks[i].children[0].checked)
            selected.push(checks[i].children[0].value);
    }
    return selected;
}

function marketListSetAll(checked) {
    checks = marketListChecks.children;
    for (let i = 0; i < checks.length; i++) {
        checks[i].children[0].checked = checked;
    }
    updateStatistics();
}


function getIntervalValue(){
    return marketListCheck_interval.value;
}

function getTypeValue(){
    return marketListCheck_type.value;
}


function updateStatistics(){
    createStatsPages();
    drawCharts();
    setStats();
}


function setStats(){
    eel.calculateStats([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), parseInt(marketListCheck_sections.value), "comparison"); 
    getSelectedMarkets().forEach((title)=>{
        eel.calculateStats([title], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), 30, "market"+title); 
    });
}

eel.expose(applyStats);
function applyStats(correlation, weightedCorrelation, betaDaily, betaWeekly, betaMonthly, elemsId){
    try{
        document.getElementById(elemsId+"Correlation").innerHTML = correlation;
        document.getElementById(elemsId+"WeightedCorrelation").innerHTML = weightedCorrelation;
        document.getElementById(elemsId+"BetaDaily").innerHTML = betaDaily;
        document.getElementById(elemsId+"BetaWeekly").innerHTML = betaWeekly;
        document.getElementById(elemsId+"BetaMonthly").innerHTML = betaMonthly;    
    }
    catch(e){
        console.error(e);
    }
}


function invertStatsPages(markets, manageCharts=true){
    markets.forEach((m)=>{
        let elem = document.getElementById("statsPageContent"+m);
        if(elem.style.display=="none")
            openStatsPages([m], manageCharts);
        else
            closeStatsPages([m], manageCharts);
    });
}

function openStatsPages(markets, drawCharts=true){
    markets.forEach((m)=>{
        let elem = document.getElementById("statsPageContent"+m);
        elem.style.display="block";
        if(drawCharts)
            drawTitleCharts(m);
    });
}

function closeStatsPages(markets, ereaseCharts=true){
    markets.forEach((m)=>{
        let elem = document.getElementById("statsPageContent"+m);
        elem.style.display="none";
        if(ereaseCharts)
            ereaseTitleCharts(m);
    });
}

function createStatsPages(){
    innerHtml = "";
    getSelectedMarkets().forEach((title)=>{
        innerHtml+=`
        <div class="statsPage">
            <button class="btn btn-info dropdown-toggle" style="font-size: 1.20rem;font-weight: 500;" type="button" onclick="invertStatsPages(['${title}'])" id="dropdownMenuButton" aria-haspopup="true" aria-expanded="false">${title}</button>
            
            <div class="statsPageContent" id="statsPageContent${title}" style="display:none">
                <div class="flex "> 
                    <div class="statsPageDataListScrollable">
                        <div class="flex">
                            <div class="bd">Correlation</div>
                            <div style="color: rgb(49, 49, 49);" id="market${title}Correlation">1.3</div>
                        </div>
                        <hr>
                        <div class="flex">
                            <div class="bd">Weighted Correlation</div>
                            <div style="color: rgb(49, 49, 49);" id="market${title}WeightedCorrelation">1.3</div>
                        </div>
                        <hr>
                        <div class="flex">
                            <div class="bd">Beta Daily</div>
                            <div style="color: rgb(49, 49, 49);" id="market${title}BetaDaily">1.3</div>
                        </div>
                        <hr>
                        <div class="flex">
                            <div class="bd">Beta Weekly</div>
                            <div style="color: rgb(49, 49, 49);" id="market${title}BetaWeekly">1.3</div>
                        </div>
                        <hr>
                        <div class="flex">
                            <div class="bd">Beta Monthly</div>
                            <div style="color: rgb(49, 49, 49);" id="market${title}BetaMonthly">1.3</div>
                        </div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runBackTesting('${title}');">Run Back Testing</button>
                        </div>
                        <hr>
                            <div class="bd">Indicators</div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="marketExportExcel('${title}')">Export to Excel</button>
                        </div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runIndicator(['${title}'], indicator_subdivision);">Run Subdivision</button>
                        </div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runIndicator(['${title}'], indicator_prevision);">Run Prevision</button>
                        </div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runIndicator(['${title}'], indicator_rsi);">Run RSI</button>
                        </div>
                        <hr>                        
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runIndicator(['${title}'], indicator_obv);">Run OBV</button>
                        </div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runIndicator(['${title}'], indicator_macd);">Run MACD</button>
                        </div>
                        <hr>
                            <div class="bd">Alerts</div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runAlert(['${title}'], alert_iceberg);">Run Iceberg</button>
                        </div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runAlert(['${title}'], alert_bubble);">Run Bubble</button>
                        </div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runAlert(['${title}'], alert_macdObv);">Run MACD-OBV</button>
                        </div>
                    </div>
                    <div id="market${title}ChartValues" class="chart"></div>
                </div>
                <div id="market${title}ChartDelta" class="chart"></div>
                <div id="market${title}ChartDeltaValues" class="chart"></div>
            </div>
        </div>
        `
    });
    statsPageContainer.innerHTML = innerHtml;
}

function marketExportExcel(titles){
    eel.exportExcel(titles, marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue());
}





function drawTitleCharts(title){
    eel.formatData([title], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "value", addChartDataTable(`market${title}ChartValues`, "line",  [title], "prices", [TAG_AVERAGE_LINE]));
    eel.formatData([title], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "deltaPerc", addChartDataTable(`market${title}ChartDelta`, "line", [title], "percentage trend", [TAG_SUM_PREC], "percentage"));
    eel.formatData([title], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "deltaPerc", addChartDataTable(`market${title}ChartDeltaValues`, "line", [title], "delta values", [], "percentage"));
}

function ereaseTitleCharts(title){
    document.getElementById(`market${title}ChartValues`).innerHTML="";
    document.getElementById(`market${title}ChartDeltaValues`).innerHTML="";
}

var drawingCharts = false;
function drawCharts(){
    selected = getSelectedMarkets();
    if(!drawingCharts && selected.length>0){
        chartDataTables = {};
        drawingCharts = true;
        

        eel.formatData(selected, marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "value", addChartDataTable("marketChart", "line", selected,""));
        
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "deltaPerc", addChartDataTable("comparisonChartDelta", "line", [comparisonTitle1.value, comparisonTitle2.value], "percentage trend", [TAG_SUM_PREC], "percentage"));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "log", addChartDataTable("comparisonChartLog", "line", [comparisonTitle1.value, comparisonTitle2.value], "log trend", [TAG_SUM_PREC], "log"));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "value", addChartDataTable("comparisonChartScaled", "line", [comparisonTitle1.value, comparisonTitle2.value], "same start", [TAG_SAME_START]));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "deltaPerc", addChartDataTable("comparisonChartDeltaValues", "line", [comparisonTitle1.value, comparisonTitle2.value], "delta values", [], "percentage"));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "value", addChartDataTable("comparisonChartAverageLine", "line", [comparisonTitle1.value, comparisonTitle2.value], "average line", [TAG_AVERAGE_LINE], "value"));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "value", addChartDataTable("comparisonChartRatio", "line", [comparisonTitle1.value, comparisonTitle2.value], "ratio", [TAG_RATIO], "value"));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "deltaPerc", addChartDataTable("comparisonChartDeltaRatio", "line", [comparisonTitle1.value, comparisonTitle2.value], "delta ratio", [TAG_RATIO], "value"));


        eel.sendStopDrawing()
    }
}

eel.expose(stopDrawing);
function stopDrawing(){
    drawingCharts = false;
}

function runCorrelationTable(){
    eel.calculateCorrelationMatrix(getSelectedMarkets(), marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), correlationExport.checked);
}




var corrMatrixCache = null;
eel.expose(createCorrelationTable);
function createCorrelationTable(corrMatrix){
    if(corrMatrix){
        corrMatrixCache = corrMatrix;
        let markets = getSelectedMarkets();
        let upperThreshold = document.getElementById("correlationUpperThreshold").value;
        let lowerThreshold = document.getElementById("correlationLowerThreshold").value;
        tableHtml = `<thead><tr style="position:sticky; top:0; background-color:white"><th scope="col"></th>`;
        markets.forEach((m)=>{
            tableHtml+=`<th scope="col">${m}</th>`
        });
        tableHtml+=`<th scope="col"></th></tr></thead><tbody>`;
        for(let i=0;i<markets.length;i++){
            tableHtml+=`<tr><th scope="row" style="position:sticky;left:0;background-color:white">${markets[i]}</th>`;
            for(let j=0;j<markets.length;j++){
                let value = corrMatrix[i][j];
                if((correlationTriangular.checked && j<i) || (correlationValidTitles.checked && value < upperThreshold && value > lowerThreshold)){
                    tableHtml+="<td></td>";
                }
                else{
                    let bkg = "";
                    let alphaStart = 0.3;
                    if(j!=i){
                        if(value>=upperThreshold){   
                            let prop = (value-upperThreshold) * (1-alphaStart) / (1-upperThreshold);
                            bkg=`background-color: rgb(0,255,0,${alphaStart+prop})`;
                        }
                        if(value<=lowerThreshold){
                            let prop = (value-lowerThreshold) * (1-alphaStart) / (-1-lowerThreshold);
                            bkg=`background-color: rgb(255,0,0,${alphaStart+prop})`;
                        }
                    }
                    tableHtml+=`<td title="${markets[i]} - ${markets[j]}" style="${bkg}" onclick="setComparison('${markets[i]}', '${markets[j]}');comparisonTitle1.scrollIntoView();">${value}</td>`;    
                }
            }
    
            tableHtml+=`<th scope="row">${markets[i]}</th></tr>`
        }
        tableHtml+="</tbody>";
        correlationTable.innerHTML = tableHtml;
    
    }
}



function dateToString(date){
    return date.getDate()+"/"+(date.getMonth()+1)+"/"+(date.getYear()+1900);
}


function switchComparison(){
    let tmp = comparisonTitle1.value;
    comparisonTitle1.value = comparisonTitle2.value;
    comparisonTitle2.value = tmp;
    updateStatistics();
}

function setComparison(title1, title2){
    comparisonTitle1.value = title1;
    comparisonTitle2.value = title2;
    updateStatistics();
}


eel.expose(setProgress);
function setProgress(progressBarId, value){
    document.getElementById(progressBarId).style.width = `${value}%`;
}

eel.expose(setMarketStatus)
function setMarketStatus(ms){
    if(ms==null){
        setTimeout(()=>{
            eel.getMarketStatus();
        }, 100)
    }
    else
        marketStatus = ms;
}

function openMenu(){
    location.pathname = '/menu.html';
}


eel.getMarketStatus();
setInterval(()=>{
    eel.getMarketStatus();
}, REALTIME_UPDATE_MILLIS);