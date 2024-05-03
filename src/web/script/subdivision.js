var titlesSubdivision = []
var subdivision_interval;
var subdivision_offset;
var subdivision_datatype;

function runSubdivision(titles){
    titlesSubdivision = titles;
    openSimulationPanel();
    insertHtmlSubdivision();
    setTimeout(()=>{
        updateVariables();
        updateSubdivision();
    },1);

}

function updateVariables(){
    subdivision_interval = document.getElementById("subdivision_interval");
    subdivision_offset = document.getElementById("subdivision_offset");
    subdivision_datatype = document.getElementById("subdivision_datatype");
    subdivision_chartHeight = document.getElementById("subdivision_chartHeight");
}

function insertHtmlSubdivision(){
    simulationContent.innerHTML = `
    <div class="statsPageDataList" style="margin-left:20px;width:800px">
        <div class="flex">
            <div class="bd w-200">interval</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="30" type="number" class="form-control" id="subdivision_interval" onchange="updateSubdivision();">
            </div>
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">charts offset</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="30" type="number" class="form-control" id="subdivision_offset" onchange="updateSubdivision();">
            </div>
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">charts height</div>
            <div class="input-group mb-1">
                <input style="height: 30px;" value="400" type="number" class="form-control" id="subdivision_chartHeight" onchange="updateSubdivision();">
            </div>
        </div>
        <hr>
        <div class="flex">
            <div class="bd w-200">data types</div>
            <div class="input-group mb-1">
                <select id="subdivision_datatype" class="form-select" style="height: 33px" onchange="updateSubdivision();" >
                    <option value="value">prices</option>
                    <option value="perc">percentage</option>
                    <option value="deltaPerc">delta percentage</option>
                </select>            
            </div>
        </div>
    </div>
    <div id="simulationChart" class="chart" style="height:700px"></div>
    `;
}

function applySubdivision(formattedData, dataChartCode){
    intervalDays = parseInt(subdivision_interval.value);
    offset = parseFloat(subdivision_offset.value);
    splits = Math.floor(formattedData.length/intervalDays);
    markets = formattedData[0].length-1;
    pointer = formattedData.length-1;
    startPoint = formattedData.length - splits*intervalDays;
    data = []
    let startValues = [0];
    for(let i=0;i<intervalDays;i++){
        newData = [i];
        for(let s=0;s<splits;s++){
            for(let m =0;m<titlesSubdivision.length;m++){
                if(i==0){
                    startValues.push(formattedData[startPoint+s*intervalDays][m+1]);
                }
                newData.push(formattedData[startPoint+i+s*intervalDays][m+1]+offset*s);
            }
        }
        for(let j=1;j<newData.length;j++){
            newData[j]-=startValues[j];
        }
        data.push(newData);
    }
    table = chartDataTables[dataChartCode]["table"];
    table.removeColumn(0);
    table.addColumn('number', "x");

    for(let s=0;s<splits;s++){
        console.log(formattedData[s*intervalDays][0]);
        console.log(formattedData[s*intervalDays][0].getDate());
        console.log(formattedData[s*intervalDays][0].getMonth());
        for(let m =0;m<titlesSubdivision.length;m++){
            table.addColumn('number', dateToString(formattedData[s*intervalDays][0])+" "+titlesSubdivision[m]);
        }
    }
    
    return data;
}

function updateSubdivision(){
    document.getElementById("simulationChart").style.height = subdivision_chartHeight.value +"px";
    let xAxis = "";
    let iv = getIntervalValue();
    if(iv=="d")
        xAxis = "days";
    if(iv=="wk")
        xAxis = "weeks";
    if(iv=="mo")
        xAxis = "months";
    eel.formatData(titlesSubdivision, marketListCheck_from.value, marketListCheck_to.value, getIntervalValue(), getTypeValue(), (subdivision_datatype.value=="perc"?"deltaPerc":subdivision_datatype.value), "simulationChart", addChartDataTable([], "subdivision", [(subdivision_datatype.value=="perc"?TAG_SUM_PREC:"")], "value", xAxis, null, applySubdivision));
}