

var chartCodeCounter = 0;
var chartCodeListSize = 100;
var chartDataTables = {}
function addChartDataTable(chartId, type, columns, title, tags=null, yAxis="price", xAxis="time", callbackPreTag=null, callbackAfterTag=null, ulteriorOptions=null){
    if(chartCodeCounter>=chartCodeListSize)
        chartCodeCounter=0;
    chartDataTables[chartCodeCounter.toString()] = {};
    obj = chartDataTables[chartCodeCounter.toString()]; 
    obj["table"] =  new google.visualization.DataTable();
    if(type=="line" || type=="bar")
        obj["table"].addColumn('date', 'x');
    else if(type=="pie")
        obj["table"].addColumn('string', 'x');
    columns.forEach(element => {
        obj["table"].addColumn('number', element);
    });
    obj["chartId"] = chartId;
    obj["type"] = type;
    obj["title"] = title;
    obj["tags"] = (tags==null?[]:tags);
    obj["yAxis"] = yAxis;
    obj["xAxis"] = xAxis;
    obj["callbackPreTag"] = callbackPreTag;
    obj["callbackAfterTag"] = callbackAfterTag;
    obj["ulteriorOptions"] = ulteriorOptions;
    return (chartCodeCounter++).toString();
}

function removeCharts(){
    document.querySelectorAll(".chart").forEach((c)=>{
        c.innerHTML="";
    })
}

eel.expose(applyChart);
function applyChart(formattedData, dataChartCode, retryingCount=0){
    console.log(formattedData);
    setTimeout(()=>{
        try{
            if(chartDataTables[dataChartCode]==null)
                return;
            let dataTable = chartDataTables[dataChartCode]["table"];
            let chartId = chartDataTables[dataChartCode]["chartId"];
            let type = chartDataTables[dataChartCode]["type"];
            let chartTitle = chartDataTables[dataChartCode]["title"];
            let tags = chartDataTables[dataChartCode]["tags"];
            let yAxis = chartDataTables[dataChartCode]["yAxis"];
            let xAxis = chartDataTables[dataChartCode]["xAxis"];
            let callbackPreTag = chartDataTables[dataChartCode]["callbackPreTag"];
            let callbackAfterTag = chartDataTables[dataChartCode]["callbackAfterTag"];
            let ulteriorOptions = chartDataTables[dataChartCode]["ulteriorOptions"];


            if(callbackPreTag){
                formattedData = callbackPreTag(formattedData, dataChartCode);
            }
            if(type=="line" || type=="bar"){
                for(let i=0;i<formattedData.length;i++){
                    formattedData[i][0] = new Date(formattedData[i][0]*1000);
                }    
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
                else if(t == TAG_AVERAGE_LINE){
                    dataTable.addColumn('number', "average")
                    let cnt=0;
                    let sum=0;
                    for(let j = 1; j < formattedData[0].length;j++){
                        for(let i=0; i < formattedData.length; i++){
                            cnt++;
                            sum+=formattedData[i][j];
                        }
                    }
                    let avg = sum/cnt;
                    for(let i=0; i < formattedData.length; i++){
                        formattedData[i].push(avg);
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
            
            options = {...options, ...ulteriorOptions}
            let chart;
            switch(type){
                case "bar":
                    chart = new google.visualization.ColumnChart(document.getElementById(chartId));
                    break;
                case "line":
                    chart = new google.visualization.LineChart(document.getElementById(chartId));
                    break;
                case "pie":
                    chart = new google.visualization.PieChart(document.getElementById(chartId));
                    break;
                default:
                    console.error("Invalid chart type");
                    console.error(dataTable);
                    break;
            }
            if(type=="bar"){
                options = google.charts.Bar.convertOptions(options)
            }
            chart.draw(dataTable, options);    
        }
        catch(e){
            if(retryingCount == 50)
                console.error(e);
            else
                applyChart(formattedData, dataChartCode, retryingCount+1);
        }
    },100);
}

function loadGoogleCharts(callback){
    google.charts.load('current', { packages: ['corechart', 'line', 'bar'] });
    google.charts.setOnLoadCallback(callback);
}

function formattedDataSplice(formattedData, viewFrom){
    let viewFromIndex = 0;
    let d = viewFrom.split("-");
    let viewFromTimestamp = new Date(d[0], d[1]-1, d[2]).getTime();
    for(let i=0;i<formattedData.length;i++){
        if(formattedData[i][0]*1000 < viewFromTimestamp)
            viewFromIndex++;
    }
    formattedData.splice(0,viewFromIndex);
    return formattedData
}