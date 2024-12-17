var indicator_subdivision_chart = "indicator_subdivision_chart";
var indicator_subdivision = new Indicator("subdivision", [
    new Input("period", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "period"),
        new Option(HtmlInputFactory.defaultValue0Option, 30)
    ]),
    new Input("chartOffset", HtmlInputFactory.floatInput, [
        new Option(HtmlInputFactory.titleOption, "chart offset"),
        new Option(HtmlInputFactory.defaultValue0Option, 30),
    ]),
    new Input("chartHeight", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "chart height"),
        new Option(HtmlInputFactory.defaultValue0Option, 400),
    ]),
    new Input("historicalData", HtmlInputFactory.dateRangeInput, [
        new Option(HtmlInputFactory.titleOption, "historical data"),
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue),
        new Option(HtmlInputFactory.defaultValue1Option, HtmlInputFactory.inheritValue)
    ]),
    new Input("type", HtmlInputFactory.dataTypeInput, [
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue)
    ]),
    new Input("interval", HtmlInputFactory.intervalTypeInput, [   
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue)
    ]),
    new Input("format", HtmlInputFactory.formatTypeInput, [   
    ]),
    new Input("load", HtmlInputFactory.buttonInput, [
        new Option(HtmlInputFactory.titleOption, "Load"),
        new Option(HtmlInputFactory.onClickOption, "indicator_subdivision_load();")
    ])
],
    `
    <div id="${indicator_subdivision_chart}" class="chartHeighted" style="height:700px"></div>
    `
);


function indicator_subdivision_applySub(formattedData, dataChartCode){
    let intervalDays = indicator_subdivision.getInputValue("period")
    let offset = indicator_subdivision.getInputValue("chartOffset");
    let splits = Math.floor(formattedData.length/intervalDays);
    let startPoint = formattedData.length - splits*intervalDays;
    let data = []
    let startValues = [0];
    for(let i=0;i<intervalDays;i++){
        newData = [i];
        for(let s=0;s<splits;s++){
            for(let m =0;m<simulationTitles.length;m++){
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
        for(let m =0;m<simulationTitles.length;m++){
            table.addColumn('number', dateToString(formattedData[s*intervalDays][0])+" "+simulationTitles[m]);
        }
    }
    
    return data;
}

function indicator_subdivision_load(){
    setChartHeight(indicator_subdivision_chart, indicator_subdivision.getInputValue("chartHeight"));
    let iv = indicator_subdivision.getInputValue("interval");
    let xAxis = "";
    if(iv=="d")
        xAxis = "days";
    if(iv=="wk")
        xAxis = "weeks";
    if(iv=="mo")
        xAxis = "months";
    let format = indicator_subdivision.getInputValue("format")
    let dt = addChartDataTable(indicator_subdivision_chart, "line", [], "subdivision", [format=="perc"?TAG_SUM_PREC:""], "value", xAxis, null, indicator_subdivision_applySub)
    let hd = indicator_subdivision.getInputValue("historicalData")
    let f = indicator_subdivision.getInputValue("format");
    eel.formatData(simulationTitles, hd[0], hd[1], ...indicator_subdivision.getInputsValues("interval", "type"), (format=="perc"?"deltaPerc":format), dt)
}