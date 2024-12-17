var indicator_rsi_dataChart = "indicator_rsi_dataChart";
var indicator_rsi_rsiChart = "indicator_rsi_rsiChart";
var indicator_rsi = new Indicator("rsi", [
    new Input("period", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "period"),
        new Option(HtmlInputFactory.defaultValue0Option, 14)
    ]),
    new Input("historicalData", HtmlInputFactory.dateRangeInput, [
        new Option(HtmlInputFactory.titleOption, "historical data"),
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue),
        new Option(HtmlInputFactory.defaultValue1Option, HtmlInputFactory.inheritValue),
    ]),
    new Input("type", HtmlInputFactory.dataTypeInput, [
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue),
    ]),
    new Input("interval", HtmlInputFactory.intervalTypeInput, [   
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue),
    ]),
    new Input("chartHeight", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "chart height"),
        new Option(HtmlInputFactory.defaultValue0Option, 400),
    ]),
    new Input("load", HtmlInputFactory.buttonInput, [
        new Option(HtmlInputFactory.titleOption, "Load"),
        new Option(HtmlInputFactory.onClickOption, "indicator_rsi_load();")
    ])
],
    `
    <div id="${indicator_rsi_dataChart}" class="chartHeighted" style="height:400px"></div>
    <div id="${indicator_rsi_rsiChart}" class="chartHeighted" style="height:700px"></div>
    `
);

function indicator_rsi_load(){
    let h = indicator_rsi.getInputValue("chartHeight");
    setChartHeight(indicator_rsi_rsiChart, h)
    let options = getDefaultChartOptions(indicator_rsi_rsiChart, h);
    let optionsRsi = {
        height: h
    }
    let dtData = addChartDataTable(indicator_rsi_dataChart, "line", [simulationTitles[0]], "price", null, "", "", null, null, getDefaultChartOptions(indicator_rsi_rsiChart));
    let dtRsi = addChartDataTable(indicator_rsi_rsiChart, "line", ["rsi"], "", null, "", "", null, null, {...options, ...optionsRsi});
    eel.indicator_rsi_calculate(simulationTitles[0], dtRsi, ...indicator_rsi.getInputsValues("historicalData", "interval", "type", "period"));
    let hd = indicator_rsi.getInputValue("historicalData");
    eel.formatData([simulationTitles[0]], hd[0], hd[1], ...indicator_rsi.getInputsValues("interval", "type"), "value", dtData)
}