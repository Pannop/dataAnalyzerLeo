var simulationPanel = document.getElementById("simulationPanel");
var simulationContent = document.getElementById("simulationContent");
var marketListChecks = document.getElementById("marketListChecks");
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

var TAG_RATIO = "ratio";
var TAG_SUM_PREC = "sumprec";
var TAG_SCALED = "scaled";
var TAG_SAME_START = "samestart";

var baseData = null;

eel.expose(setSize);
function setSize(width, height) {

    let html = document.getElementById("html");
    //html.style.width = `${width}px`;
    //html.style.height = `${height}px`;
    window.resizeTo(width, height);
}


function setMarketList(index, marketList) {
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
    str = addMarketCheckBox(index);
    for (let i = 0; i < marketList.length; i++) {
        str += addMarketCheckBox(marketList[i]);
    }
    marketListChecks.innerHTML = str;
    document.getElementById(`marketListCheck_${index}`).checked = true;
}

function setComparisonList(index, marketList){
    addOption = (name) => {
        return `
        <option value="${name}">${name}</option>
        `
    }
    str = addOption(index);
    for (let i = 0; i < marketList.length; i++) {
        str += addOption(marketList[i]);
    }
    comparisonTitle1.innerHTML = str;
    comparisonTitle2.innerHTML = str;
}

eel.expose(setTitles);
function setTitles(data) {
    baseData = data;
    setMarketList(baseData["indexName"], baseData["marketList"]);
    setComparisonList(baseData["indexName"], baseData["marketList"]);
    updateStatistics();
}

google.charts.load('current', { packages: ['corechart', 'line'] });
//google.charts.setOnLoadCallback(drawCharts);


eel.setDefaultSize();
eel.loadTitles();


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
    return document.querySelector('input[name="marketListCheck_radioInterval"]:checked').value;
}

function getTypeValue(){
    return document.querySelector('input[name="marketListCheck_radioType"]:checked').value;
}


function updateStatistics(){
    createStatsPages();
    drawCharts();
    setStats();
}

function removeCharts(){
    document.querySelectorAll(".chart").forEach((c)=>{
        c.innerHTML="";
    })
}

function setStats(){
    eel.calculateStats([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), parseInt(marketListCheck_sections.value), "comparison"); 
    getSelectedMarkets().forEach((title)=>{
        eel.calculateStats([title], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), 30, "market"+title); 
    });
}

eel.expose(applyStats);
function applyStats(correlation, weightedCorrelation, betaDaily, betaWeekly, betaMonthly, elemsId){
    document.getElementById(elemsId+"Correlation").innerHTML = correlation;
    document.getElementById(elemsId+"WeightedCorrelation").innerHTML = weightedCorrelation;
    document.getElementById(elemsId+"BetaDaily").innerHTML = betaDaily;
    document.getElementById(elemsId+"BetaWeekly").innerHTML = betaWeekly;
    document.getElementById(elemsId+"BetaMonthly").innerHTML = betaMonthly;
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
                    <div class="statsPageDataList">
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
                            <button class="btn btn-outline-dark" onclick="marketExportExcel('${title}')">Export to Excel</button>
                        </div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runSubdivision(['${title}']);">Run Subdivision</button>
                        </div>
                        <hr>
                        <div class="flex">
                            <button class="btn btn-outline-dark" onclick="runPrevision(['${title}']);">Run Prevision</button>
                        </div>
                    </div>
                    <div id="market${title}ChartValues" class="chart"></div>
                </div>
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


var chartCodeCounter = 0;
var chartDataTables = {}
function addChartDataTable(columns, title, tags=null, yAxis="price", xAxis="time", callbackPreTag=null, callbackAfterTag=null){
    chartDataTables[chartCodeCounter.toString()] = {};
    obj = chartDataTables[chartCodeCounter.toString()]; 
    obj["table"] =  new google.visualization.DataTable();
    obj["table"].addColumn('date', 'x');
    columns.forEach(element => {
        obj["table"].addColumn('number', element);
    });
    obj["title"] = title;
    obj["tags"] = (tags==null?[]:tags);
    obj["yAxis"] = yAxis;
    obj["xAxis"] = xAxis;
    obj["callbackPreTag"] = callbackPreTag;
    obj["callbackAfterTag"] = callbackAfterTag;
    return (chartCodeCounter++).toString();
}


function drawTitleCharts(title){
    eel.formatData([title], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "value", `market${title}ChartValues`, addChartDataTable([title], "prices"));
    eel.formatData([title], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "deltaPerc", `market${title}ChartDeltaValues`, addChartDataTable([title], "delta values", [], "percentage"));
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
        

        eel.formatData(selected, marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "value", "marketChart", addChartDataTable(selected,""));
        
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "deltaPerc", "comparisonChartDelta", addChartDataTable([comparisonTitle1.value, comparisonTitle2.value], "percentage trend", [TAG_SUM_PREC], "percentage"));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "log", "comparisonChartLog", addChartDataTable([comparisonTitle1.value, comparisonTitle2.value], "log trend", [TAG_SUM_PREC], "log"));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "value", "comparisonChartScaled", addChartDataTable([comparisonTitle1.value, comparisonTitle2.value], "same start", [TAG_SAME_START]));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "deltaPerc", "comparisonChartDeltaValues", addChartDataTable([comparisonTitle1.value, comparisonTitle2.value], "delta values", [], "percentage"));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "value", "comparisonChartRatio", addChartDataTable([comparisonTitle1.value, comparisonTitle2.value], "ratio", [TAG_RATIO], "value"));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "deltaPerc", "comparisonChartDeltaRatio", addChartDataTable([comparisonTitle1.value, comparisonTitle2.value], "delta ratio", [TAG_RATIO], "value"));


        eel.sendStopDrawing()
    }
}

eel.expose(stopDrawing);
function stopDrawing(){
    drawingCharts = false;
}


eel.expose(applyChart);
function applyChart(formattedData, elemId, dataChartCode){
    setTimeout(()=>{
        if(chartDataTables[dataChartCode]==null)
            return;
        let dataTable = chartDataTables[dataChartCode]["table"];
        let chartTitle = chartDataTables[dataChartCode]["title"];
        let tags = chartDataTables[dataChartCode]["tags"];
        let yAxis = chartDataTables[dataChartCode]["yAxis"];
        let xAxis = chartDataTables[dataChartCode]["xAxis"];
        let callbackPreTag = chartDataTables[dataChartCode]["callbackPreTag"];
        let callbackAfterTag = chartDataTables[dataChartCode]["callbackAfterTag"];
        
        for(let i=0;i<formattedData.length;i++){
            formattedData[i][0] = new Date(formattedData[i][0]*1000);
        }

        if(callbackPreTag){
            formattedData = callbackPreTag(formattedData, dataChartCode);
        }
        tags.forEach((t)=>{
            if(t == TAG_RATIO){
                dataTable.removeColumns(1,2);
                dataTable.addColumn('number', "ratio");
                for(let i=0;i<formattedData.length;i++){
                    formattedData[i][1] = (formattedData[i][1]/formattedData[i][2]);
                    formattedData[i].pop(2);
        
                }
            }
            else if( t == TAG_SUM_PREC){
                for(let i=1;i<formattedData.length;i++){
                    for(let j=1;j<formattedData[0].length; j++){
                        formattedData[i][j] += formattedData[i-1][j];
                    }
                }
            }
            else if(t == TAG_SCALED){
                for(let j=2;j<formattedData[0].length; j++){
                    let factorScale = formattedData[0][1]/formattedData[0][j];
                    for(let i=0;i<formattedData.length;i++){
                        formattedData[i][j] *= factorScale;
                    }
                }
            }
            else if(t == TAG_SAME_START){
                for(let j=2;j<formattedData[0].length; j++){
                    let factorAdditional = formattedData[0][1]-formattedData[0][j];
                    for(let i=0;i<formattedData.length;i++){
                        formattedData[i][j] += factorAdditional;
                    }
                }
            }
        });
        if(callbackAfterTag){
            formattedData = callbackAfterTag(formattedData, dataChartCode);
        }

    
        dataTable.addRows(formattedData);
    
        let options = {
            hAxis: {
                title: xAxis
            },
            vAxis: {
                title: yAxis
            },
            title: chartTitle
        };
    
        let chart = new google.visualization.LineChart(document.getElementById(elemId));
        chart.draw(dataTable, options);    
    
    },1);
}


function runCorrelationTable(){
    eel.calculateCorrelationMatrix(getSelectedMarkets(), marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue());
}


var corrMatrixCache = null;
eel.expose(createCorrelationTable);
function createCorrelationTable(corrMatrix){
    if(corrMatrix){
        corrMatrixCache = corrMatrix;
        let markets = getSelectedMarkets();
        let upperThreshold = document.getElementById("correlationUpperThreshold").value;
        let  lowerThreshold = document.getElementById("correlationLowerThreshold").value;
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


function openSimulationPanel(){
    window.scrollTo(0, 0);
    simulationPanel.style.display="block";
    document.getElementById("html").style.overflowY="hidden";
    removeCharts();
}

function closeSimulationPanel(){
    simulationPanel.style.display="none";
    document.getElementById("html").style.overflowY="scroll";
    updateStatistics();
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