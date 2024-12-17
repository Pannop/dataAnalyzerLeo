var alert_iceberg_dataChart="alert_iceberg_dataChart";
var alert_iceberg_volumeChart="alert_iceberg_volumeChart";
var alert_iceberg_volumeBarChart="alert_iceberg_volumeBarChart";
var alert_iceberg = new Alert("iceberg", [
    new Input("periodTotal", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "total period"),
        new Option(HtmlInputFactory.defaultValue0Option, 30)
    ]),
    new Input("periodToCheck", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "check period"),
        new Option(HtmlInputFactory.defaultValue0Option, 5)
    ]),
    new Input("minAvgVolDeltaPerc", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "min average volume delta perc"),
        new Option(HtmlInputFactory.defaultValue0Option, 100)
    ]),
    new Input("maxAvgPriceDeltaPerc", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "max average price delta perc"),
        new Option(HtmlInputFactory.defaultValue0Option, 30)
    ]),
    new Input("interval", HtmlInputFactory.intervalTypeInput, [
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue)
    ]),
    new Input("type", HtmlInputFactory.dataTypeInput, [
        new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue)
    ])
],
    `
        <div id="${alert_iceberg_dataChart}" class="chartHeighted" style="height:400px"></div>
        <div id="${alert_iceberg_volumeChart}" class="chartHeighted" style="height:400px"></div>
        <div id="${alert_iceberg_volumeBarChart}" class="chartHeighted" style="height:400px"></div>

    `,
    "alert_iceberg_test()",
    "alert_iceberg_addListener()"
);

function alert_iceberg_test(){
    let dtData = addChartDataTable(alert_iceberg_dataChart, "line", ["not satisfied", "satisfied"], "price", null, "", "", null, null, getDefaultChartOptions(alert_iceberg_dataChart));
    let dtVolume = addChartDataTable(alert_iceberg_volumeChart, "line", ["not satisfied", "satisfied"], "volume", null, "", "", null, null, getDefaultChartOptions(alert_iceberg_volumeChart));
    let dtVolumeBar = addChartDataTable(alert_iceberg_volumeBarChart, "bar", ["not satisfied", "satisfied"], "volume", null, "", "", null, null, getDefaultChartOptions(alert_iceberg_volumeChart));
    eel.alert_iceberg_test(simulationTitles[0], dtData, dtVolume, dtVolumeBar,  ...alert_iceberg.getInputsValues("historicalData", "periodTotal", "periodToCheck", "interval", "type", "minAvgVolDeltaPerc", "maxAvgPriceDeltaPerc"))
}

eel.expose(alert_iceberg_testApplyResults);
function alert_iceberg_testApplyResults(results){
    console.log(results);
    alert_iceberg.getInputByName("results").getElement().value = results;
}

function alert_iceberg_addListener(){
    eel.alert_iceberg_addListener(simulationTitles[0], alert_iceberg.getInputValue("minutesCheckRate"), alert_iceberg.getInputsValues("periodTotal", "periodToCheck", "interval", "type", "minAvgVolDeltaPerc", "maxAvgPriceDeltaPerc"))
}


