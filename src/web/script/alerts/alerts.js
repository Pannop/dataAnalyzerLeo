function runAlert(titles, alert){
    runIndicator(titles, alert)
}


function Alert(name, inputs, nextHTML, testCallbackStr, addListenerCallbackStr, openCallback=()=>{}, disableHistoricalData=false){

    inputs.push(new Input("testText", HtmlInputFactory.headerInput, [
        new Option(HtmlInputFactory.titleOption, "Tests:"),
    ]));
    if(!disableHistoricalData)
        inputs.push(
            new Input("historicalData", HtmlInputFactory.dateRangeInput, [
                new Option(HtmlInputFactory.titleOption, "historical data"),
                new Option(HtmlInputFactory.defaultValue0Option, HtmlInputFactory.inheritValue),
                new Option(HtmlInputFactory.defaultValue1Option, HtmlInputFactory.inheritValue),
            ]));
    inputs.push(new Input("results", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "results"),
        new Option(HtmlInputFactory.defaultValue0Option, 0),
        new Option(HtmlInputFactory.disabledOption, true)
    ]));
    inputs.push(new Input("test", HtmlInputFactory.buttonProgressBarInput, [
        new Option(HtmlInputFactory.titleOption, "Test"),
        new Option(HtmlInputFactory.onClickOption, testCallbackStr)
    ]));
    inputs.push(new Input("listenerText", HtmlInputFactory.headerInput, [
        new Option(HtmlInputFactory.titleOption, "Listeners:"),
    ]));
    inputs.push(new Input("minutesCheckRate", HtmlInputFactory.numberInput, [
        new Option(HtmlInputFactory.titleOption, "minutes check rate"),
        new Option(HtmlInputFactory.defaultValue0Option, 60*24)
    ]));
    inputs.push(new Input("addListener", HtmlInputFactory.buttonInput, [
        new Option(HtmlInputFactory.titleOption, "Add Listener"),
        new Option(HtmlInputFactory.onClickOption, addListenerCallbackStr)
    ]));
    Indicator.call(this, name, inputs, nextHTML, openCallback);

}

