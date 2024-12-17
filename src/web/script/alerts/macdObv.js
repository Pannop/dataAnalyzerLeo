var alert_macdObv_dataChart="alert_macdObv_dataChart";
var alert_macdObv_macdChart="alert_macdObv_macdChart";
var alert_macdObv_obvChart="alert_macdObv_obvChart";

var alert_macdObv = new Alert("macdObv", [
    new Input("periodTotal", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "total period"),
        new Option(HtmlInputFactory.defaultValue0Option, 300)
    ]),
    new Input("macdPeriodFast", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "macd fast period"),
        new Option(HtmlInputFactory.defaultValue0Option, 12)
    ]),
    new Input("macdPeriodSlow", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "macd slow period"),
        new Option(HtmlInputFactory.defaultValue0Option, 24)
    ]),
    new Input("macdPeriodSignal", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "macd signal period"),
        new Option(HtmlInputFactory.defaultValue0Option, 9)
    ]),
    new Input("macdThresholdIntersectedRatio", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "macd threshold intersected ratio"),
        new Option(HtmlInputFactory.defaultValue0Option, 5)
    ]),
    new Input("obvCurvePointsThresholdDeltaPerc", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "obv curve points threshold delta"),
        new Option(HtmlInputFactory.defaultValue0Option, 50)
    ]),
    new Input("macdType", HtmlInputFactory.dataTypeInput, [
        new Option(HtmlInputFactory.titleOption, "macd type"),
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue)
    ]),
    new Input("interval", HtmlInputFactory.intervalTypeInput, [
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue)
    ])
],
    `
        <div id="${alert_macdObv_dataChart}" class="chartHeighted" style="height:400px"></div>
        <div id="${alert_macdObv_macdChart}" class="chartHeighted" style="height:400px"></div>
        <div id="${alert_macdObv_obvChart}" class="chartHeighted" style="height:400px"></div>

    `,
    "alert_macdObv_test()",
    "alert_macdObv_addListener()"
);

function alert_macdObv_test(){
    let dtData = addChartDataTable(alert_macdObv_dataChart, "line", ["not satisfied", "satisfied gain", "satisfied loss"], "price", null, "", "", null, null, getDefaultChartOptions(alert_macdObv_dataChart));
    let dtMacd = addChartDataTable(alert_macdObv_macdChart, "line", ["not satisfied", "satisfied gain", "satisfied loss"], "macd", null, "", "", null, null, getDefaultChartOptions(alert_macdObv_macdChart));
    let dtObv = addChartDataTable(alert_macdObv_obvChart, "line", ["not satisfied", "satisfied gain", "satisfied loss"], "obv", null, "", "", null, null, getDefaultChartOptions(alert_macdObv_obvChart));
    eel.alert_macdObv_test(simulationTitles[0], dtData, dtMacd, dtObv,  ...alert_macdObv.getInputsValues("historicalData", "periodTotal", "interval", "macdType", "macdPeriodFast", "macdPeriodSlow", "macdPeriodSignal", "macdThresholdIntersectedRatio", "obvCurvePointsThresholdDeltaPerc"))
}

eel.expose(alert_macdObv_testApplyResults);
function alert_macdObv_testApplyResults(results){
    alert_macdObv.getInputByName("results").getElement().value = results;
}


