var indicator_macd_dataChart = "indicator_macd_dataChart";
var indicator_macd_macdChart = "indicator_macd_macdChart";
var indicator_macd_signalChart = "indicator_macd_signalChart";
var indicator_macd = new Indicator("macd", [
    new Input("period1", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "fast period"),
        new Option(HtmlInputFactory.defaultValue0Option, 12)
    ]),
    new Input("period2", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "slow period"),
        new Option(HtmlInputFactory.defaultValue0Option, 26)
    ]),
    new Input("periodSignal", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "signal period"),
        new Option(HtmlInputFactory.defaultValue0Option, 9)
    ]),
    new Input("historicalData", HtmlInputFactory.dateRangeInput, [
        new Option(HtmlInputFactory.titleOption, "historical data"),
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue),
        new Option(HtmlInputFactory.defaultValue1Option, HtmlInputFactory.inheritValue),
    ]),
    new Input("interval", HtmlInputFactory.intervalTypeInput, [   
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue),
    ]),
    new Input("type", HtmlInputFactory.dataTypeInput, [
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue),
    ]),
    new Input("chartHeight", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "chart height"),
        new Option(HtmlInputFactory.defaultValue0Option, 400),
    ]),
    new Input("load", HtmlInputFactory.buttonInput, [
        new Option(HtmlInputFactory.titleOption, "Load"),
        new Option(HtmlInputFactory.onClickOption, "indicator_macd_load();")
    ])
],
    `
    <div id="${indicator_macd_dataChart}" class="chartHeighted" style="height:400px"></div>
    <div id="${indicator_macd_macdChart}" class="chartHeighted" style="height:700px"></div>
    <div id="${indicator_macd_signalChart}" class="chartHeighted" style="height:700px"></div>
    `
);

function indicator_macd_load(){
    let h = indicator_macd.getInputValue("chartHeight");
    setChartHeight(indicator_macd_macdChart, h);
    setChartHeight(indicator_macd_signalChart, h);
    let options = getDefaultChartOptions(indicator_macd_macdChart, h);
    let optionsMacd = {
        height: h
    }
    let dtData = addChartDataTable(indicator_macd_dataChart, "line", [simulationTitles[0]], "price", null, "", "", null, null, getDefaultChartOptions(indicator_macd_macdChart));
    let dtMacd = addChartDataTable(indicator_macd_macdChart, "line", ["macd signal"], "", null, "", "", null, null, {...options, ...optionsMacd});
    let dtSignal = addChartDataTable(indicator_macd_signalChart, "line", ["macd", "signal"], "", null, "", "", null, null, {...options, ...optionsMacd});
    eel.indicator_macd_calculate(simulationTitles[0], dtMacd, dtSignal, ...indicator_macd.getInputsValues("historicalData", "interval", "type", "period1", "period2", "periodSignal"));
    let hd = indicator_macd.getInputValue("historicalData");
    eel.formatData([simulationTitles[0]], hd[0], hd[1], ...indicator_macd.getInputsValues("interval", "type"), "value", dtData)
}

