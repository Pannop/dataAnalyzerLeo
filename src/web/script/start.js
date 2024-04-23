var marketListChecks = document.getElementById("marketListChecks");
var marketListCheck_from = document.getElementById("marketListCheck_from");
var marketListCheck_to = document.getElementById("marketListCheck_to");
var marketListCheck_sections = document.getElementById("marketListCheck_sections");
var statsPageContainer = document.getElementById("statsPageContainer");
var comparisonTitle1 = document.getElementById("comparisonTitle1");
var comparisonTitle2 = document.getElementById("comparisonTitle2");
var comparisonRatio = document.getElementById("comparisonRatio");

var TAG_RATIO = "ratio";

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


function createStatsPages(){
    innerHtml = "";
    getSelectedMarkets().forEach((title)=>{
        innerHtml+=`
        <div class="statsPage">
            <h3>${title}</h3>
            <div class="statsPageContent">
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
                            <button class="btn btn-outline-dark">Run Montecarlo</button>
                        </div>
                    </div>
                    <div id="market${title}Chart" class="chart"></div>
                </div>
            </div>
        </div>
        `
    });
    statsPageContainer.innerHTML = innerHtml;
}

function marketExportExcel(titles){
    eel.exportExcet(titles, marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue());
}


var chartCodeCounter = 0;
var chartDataTables = {}
function addChartDataTable(columns, tags=null){
    chartDataTables[chartCodeCounter.toString()] = {};
    obj = chartDataTables[chartCodeCounter.toString()]; 
    obj["table"] =  new google.visualization.DataTable();
    obj["table"].addColumn('number', 'x');
    columns.forEach(element => {
        obj["table"].addColumn('number', element);
    });
    obj["tags"] = (tags==null?[]:tags);
    console.log(chartDataTables);
    return (chartCodeCounter++).toString();
}



var drawingCharts = false;
function drawCharts(){
    selected = getSelectedMarkets();
    if(!drawingCharts && selected.length>0){
        chartDataTables = {};
        drawingCharts = true;
        

        eel.formatData(selected, marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "marketChart", addChartDataTable(selected));
        eel.formatData([comparisonTitle1.value, comparisonTitle2.value], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), "comparisonChart", addChartDataTable([comparisonTitle1.value, comparisonTitle2.value], (comparisonRatio.checked?[TAG_RATIO]:null)));
        
        selected.forEach(title => {
            eel.formatData([title], marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), `market${title}Chart`, addChartDataTable([title]));
        });

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
        dataTable = chartDataTables[dataChartCode]["table"];
        tags = chartDataTables[dataChartCode]["tags"];
        
        if(tags.includes(TAG_RATIO)){
            dataTable.removeColumns(1,2);
            dataTable.addColumn('number', "ratio");
            for(let i=0;i<formattedData.length;i++){
                formattedData[i][1] = (formattedData[i][1]/formattedData[i][2]);
                formattedData[i].pop(2);
    
            }
        }
    
        dataTable.addRows(formattedData);
    
        let options = {
            hAxis: {
                title: 'Time'
            },
            vAxis: {
                title: 'Value'
            }
        };
    
        let chart = new google.visualization.LineChart(document.getElementById(elemId));
        chart.draw(dataTable, options);    
    
    },1);
}

function loadStats(){
    str = `
        <div class="statsPage">
            <h3>Stats</h3>
            <div class="statsPageContent">
                ollare ollare
            </div>
        </div>
    `
}




