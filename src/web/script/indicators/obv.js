var indicator_obv_dataChart = "indicator_obv_dataChart";
var indicator_obv_obvChart = "indicator_obv_obvChart";
var indicator_obv_volumeChart = "indicator_obv_volumeChart";
var indicator_obv = new Indicator("obv", [
    new Input("historicalData", HtmlInputFactory.dateRangeInput, [
        new Option(HtmlInputFactory.titleOption, "historical data"),
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue),
        new Option(HtmlInputFactory.defaultValue1Option, HtmlInputFactory.inheritValue),
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
        new Option(HtmlInputFactory.onClickOption, "indicator_obv_load();")
    ])
],
    `
    <div id="${indicator_obv_dataChart}" class="chartHeighted" style="height:400px"></div>
    <div id="${indicator_obv_obvChart}" class="chartHeighted" style="height:700px"></div>
    <div id="${indicator_obv_volumeChart}" class="chartHeighted" style="height:700px"></div>
    `
);

function indicator_obv_load(){
    let h = indicator_obv.getInputValue("chartHeight");
    setChartHeight(indicator_obv_obvChart, h);
    let options = getDefaultChartOptions(indicator_obv_obvChart, h);
    let optionsObv = {
        height: h
    }
    let dtData = addChartDataTable(indicator_obv_dataChart, "line", [simulationTitles[0]], "price", null, "", "", null, null, getDefaultChartOptions(indicator_obv_obvChart));
    let dtObv = addChartDataTable(indicator_obv_obvChart, "line", ["obv"], "obv", null, "", "", null, null, {...options, ...optionsObv});
    let dtVolumeBar = addChartDataTable(indicator_obv_volumeChart, "bar", ["volume"], "volume", null, "", "", null, null, getDefaultChartOptions(indicator_obv_volumeChart));

    eel.indicator_obv_calculate(simulationTitles[0], dtObv, ...indicator_obv.getInputsValues("historicalData", "interval"));
    let hd = indicator_obv.getInputValue("historicalData");
    eel.formatData([simulationTitles[0]], hd[0], hd[1], indicator_obv.getInputValue("interval"), "close", "value", dtData);
    eel.formatData([simulationTitles[0]], hd[0], hd[1], indicator_obv.getInputValue("interval"), "volume", "value", dtVolumeBar);
}

