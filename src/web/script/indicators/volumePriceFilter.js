var indicator_volumePriceFilter_prevData = null
var indicator_volumePriceFilter_prevRegions = null
var indicator_volumePriceFilter_prevCaps = null
var indicator_volumePriceFilter_table = "indicator_volumePriceFilter_chart";
var indicator_volumePriceFilter = new Indicator("volumePriceFilter", [
    new Input("minVolPercDelta", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "min volume percentage delta"),
        new Option(HtmlInputFactory.defaultValue0Option, 100)
    ]),
    new Input("minPricePercDelta", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "min price percentage delta"),
        new Option(HtmlInputFactory.defaultValue0Option, 3)
    ]),
    new Input("minAvgVol", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "min average volume"),
        new Option(HtmlInputFactory.defaultValue0Option, 10000)
    ]),
    new Input("minVolPrice", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "min volume price"),
        new Option(HtmlInputFactory.defaultValue0Option, 1000)
    ]),
    new Input("regions", HtmlInputFactory.regionsInput, [
    ]),
    new Input("capitalisation", HtmlInputFactory.capitalisationInput, [
    ]),
    new Input("sort", HtmlInputFactory.selectInput, [
        new Option(HtmlInputFactory.titleOption, "sort by"),
        new Option(HtmlInputFactory.valueListOption, {"volume percentual delta":"volumeDeltaPerc", "volume value delta":"volumePrice", "price delta":"valueDeltaPerc"})
    ]),
    new Input("forceDataUpdate", HtmlInputFactory.checkboxInput, [
        new Option(HtmlInputFactory.titleOption, "force data update")
    ]),
    new Input("results", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "results"),
        new Option(HtmlInputFactory.defaultValue0Option, 0),
        new Option(HtmlInputFactory.disabledOption, true)
    ]),
    new Input("load", HtmlInputFactory.buttonProgressBarInput, [
        new Option(HtmlInputFactory.titleOption, "Load"),
        new Option(HtmlInputFactory.onClickOption, "indicator_volumePriceFilter_load();")
    ])
],
    `
    <table class="table table-striped mt-4" id="${indicator_volumePriceFilter_table}"></table>
    `
);


function indicator_volumePriceFilter_load(){
    eel.indicator_volumePriceFilter_calculate(...indicator_volumePriceFilter.getInputsValues("minVolPercDelta", "minPricePercDelta", "minAvgVol", "minVolPrice", "regions", "capitalisation", "forceDataUpdate", "sort"), indicator_volumePriceFilter.getInputByName("load").options[HtmlInputFactory.idOption], indicator_volumePriceFilter_prevData, indicator_volumePriceFilter_prevRegions, indicator_volumePriceFilter_prevCaps)
}


eel.expose(indicator_volumePriceFilter_applyTable);
function indicator_volumePriceFilter_applyTable(volumePriceFilters, data, regions, caps){
    indicator_volumePriceFilter_prevData = data;
    indicator_volumePriceFilter_prevRegions = regions;
    indicator_volumePriceFilter_prevCaps = caps;

    let table = document.getElementById(indicator_volumePriceFilter_table);
    
    let html=`
    <tr>
        <th scope="col">Title</th>
        <th scope="col">Symbol</th>
        <th scope="col">Volume Delta</th>
        <th scope="col">Price Delta</th>         
        <th scope="col">Volume Price</th>         
        <th scope="col">Region</th>         
        <th scope="col">Market State</th>         
    </tr>
    `;
    volumePriceFilters.forEach(a => {
        html+=`
        <tr>
            <th scope="row">${a["name"]}</th>
            <td class="clickable" onclick="window.open('https://it.finance.yahoo.com/quote/${a["symbol"]}/','name')">${a["symbol"]}</td>
            <td>${a["volumeDeltaPerc"]} %</td>
            <td>${a["valueDeltaPerc"]} %</td>
            <td>${a["volumePrice"]} $</td>
            <td>${a["region"]}</td>
            <td>${a["marketState"]}</td>
        </tr>
        `;
    });
    table.innerHTML=html;
    let resElem = document.getElementById(indicator_volumePriceFilter.getInputByName("results").options[HtmlInputFactory.idOption]);
    resElem.value = volumePriceFilters.length;
}
