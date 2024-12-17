

var indicator_prevision_chart = "indicator_prevision_chart";
var indicator_prevision = new Indicator("prevision", [
    new Input("futureData", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "future data"),
        new Option(HtmlInputFactory.defaultValue0Option, 100)
    ]),
    new Input("simulations", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "simulations"),
        new Option(HtmlInputFactory.defaultValue0Option, 1000)
    ]),
    new Input("historicalData", HtmlInputFactory.dateRangeInput, [
        new Option(HtmlInputFactory.titleOption, "historical data"),
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue),
        new Option(HtmlInputFactory.defaultValue1Option, HtmlInputFactory.inheritValue),
    ]),
    new Input("viewFrom", HtmlInputFactory.dateInput, [
        new Option(HtmlInputFactory.titleOption, "view from"),
        new Option(HtmlInputFactory.defaultValue0Option, "1971-01-01"),
    ]),
    new Input("chartHeight", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "chart height"),
        new Option(HtmlInputFactory.defaultValue0Option, 400),
    ]),
    new Input("type", HtmlInputFactory.dataTypeInput, [
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue)
    ]),
    new Input("interval", HtmlInputFactory.intervalTypeInput, [  
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue) 
    ]),
    new Input("load", HtmlInputFactory.buttonInput, [
        new Option(HtmlInputFactory.titleOption, "Load"),
        new Option(HtmlInputFactory.onClickOption, "indicator_prevision_load();")
    ])
],
    `
    <div id="${indicator_prevision_chart}" class="chartHeighted" style="height:700px"></div>
    `
);

function indicator_prevision_load(){
    document.getElementById(indicator_prevision_chart).style.height =  indicator_prevision.getInputValue("chartHeight")+"px";
    let dt = addChartDataTable(indicator_prevision_chart, "line", ["base data", "montecarlo", "gbm", "heston"], "prevision", null, "value", "date", 
        (formattedData, dt)=>{
            return formattedDataSplice(formattedData, indicator_prevision.getInputValue("viewFrom"));
        }
    )
    eel.indicator_prevision_calculate(simulationTitles[0], dt, ...indicator_prevision.getInputsValues("futureData", "simulations", "historicalData", "interval", "type"));

}
