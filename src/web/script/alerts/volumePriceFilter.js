var alert_volumePriceFilter_oldSymbols = null;
var alert_volumePriceFilter_table = "alert_volumePriceFilter_chart";
var alert_volumePriceFilter = new Alert("volumePriceFilter", [
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
    ])
],
    `
    <table class="table table-striped mt-4" id="${alert_volumePriceFilter_table}"></table>
    `,
    "alert_volumePriceFilter_test()",
    "alert_volumePriceFilter_addListener()",
    ()=>{alert_volumePriceFilter_oldSymbols=null;},
    true
);

function alert_volumePriceFilter_test(){
    eel.alert_volumePriceFilter_test(...alert_volumePriceFilter.getInputsValues("minVolPercDelta", "minPricePercDelta", "minAvgVol", "minVolPrice", "regions", "capitalisation"), alert_volumePriceFilter.getInputByName("test").getId(), alert_volumePriceFilter_oldSymbols)
}


eel.expose(alert_volumePriceFilter_testApplyTable);
function alert_volumePriceFilter_testApplyTable(data, oldSymbols){
    alert_volumePriceFilter_oldSymbols = oldSymbols;
    let newAlerts = 0;
    let html=`
    <tr>
        <th scope="col">Time</th>
        <th scope="col">Title</th>
        <th scope="col">Symbol</th>
        <th scope="col">Volume Delta</th>
        <th scope="col">Value Delta</th>         
        <th scope="col">Volume Price</th>         
        <th scope="col">Region</th>         
        <th scope="col">Market State</th>         
    </tr>
    `;
    data.forEach(a => {
        if(a["deleted"]){
            html+=`
            <tr style="background-color:red">
                <td>${a["time"]}</td>
                <td>-</td>
                <td class="clickable" onclick="window.open('https://it.finance.yahoo.com/quote/${a["symbol"]}/','name')">${a["symbol"]}</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
            </tr>
            `;
        }
        else{
            if(a["new"])
                newAlerts++;
            let newTag = (a["new"]?"th":"td");
            html+=`
            <tr>
                <${newTag}>${a["time"]}</${newTag}>
                <td>${a["name"]}</td>
                <td class="clickable" onclick="window.open('https://it.finance.yahoo.com/quote/${a["symbol"]}/','name')">${a["symbol"]}</td>
                <td>${a["volumeDeltaPerc"]} %</td>
                <td>${a["valueDeltaPerc"]} %</td>
                <td>${a["volumePrice"]} $</td>
                <td>${a["region"]}</td>
                <td>${a["marketState"]}</td>
            </tr>
            `;
        }
    });
    document.getElementById(alert_volumePriceFilter_table).innerHTML = html;
    alert_volumePriceFilter.getInputByName("results").getElement().value = newAlerts;
}


function alert_volumePriceFilter_addListener(){

}