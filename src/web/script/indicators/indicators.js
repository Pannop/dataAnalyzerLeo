function hash(str) {
    let hash = 0, i, chr;
    if (str.length === 0) return hash;
    for (i = 0; i < str.length; i++) {
        chr = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + chr;
        hash |= 0;
    }
    return hash;
}
  

var simulationPanel = document.getElementById("simulationPanel");
var simulationContent = document.getElementById("simulationContent");
var simulationTitles = []



var regionsNames = ['Argentina', 'Australia', 'Austria', 'Belgium', 'Brazil', 'Canada', 'Chile', 'China', 'Czechia', 'Denmark', 'Egypt', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hong Kong SAR China', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Kuwait', 'Latvia', 'Lithuania', 'Malaysia', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Suriname', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'United Kingdom', 'United States', 'Venezuela', 'Vietnam']
var regionsNamesEurope = ['Austria', 'Belgium', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'United Kingdom'];
var regionsNamesAsia = ['China', 'Hong Kong SAR China', 'India', 'Indonesia', 'Japan', 'Kuwait', 'Malaysia', 'Philippines', 'Qatar', 'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka', 'Thailand', 'Turkey', 'Vietnam'];
var realtimeSuffixes = []


eel.expose(setRealtimeSuffixes)
function setRealtimeSuffixes(suffixes){
    realtimeSuffixes = suffixes;
}
eel.getRealtimeSuffixes()


function getSelectedCapitalisations(id){
    return [
        (document.getElementById(id+"_small").value==1?0:-1),
        (document.getElementById(id+"_mid").value==1?1:-1),
        (document.getElementById(id+"_large").value==1?2:-1),
        (document.getElementById(id+"_mega").value==1?3:-1)];
}

function getSelectedRegions(id){
    let selected = [];
    for(let r of regionsNames){
        let elem = document.getElementById(id+"_"+r);
        if(elem==null)
            break;
        if(elem.checked)
            selected.push(r);
    }
    return selected;
}

function clickRegion(regionsMenuId, region, forceCheck=false){
    if(region=="europe"){
        for(let r of regionsNamesEurope)
            clickRegion(regionsMenuId, r, true);
    }
    else if(region=="asia"){
        for(let r of regionsNamesAsia)
            clickRegion(regionsMenuId, r, true);
    }
    else if(region=="all"){
        for(let r of regionsNames)
            clickRegion(regionsMenuId, r, true);
    }
    else if(region=="none"){
        for(let r of regionsNames){
            clickRegion(regionsMenuId, r, true);
            clickRegion(regionsMenuId, r);
        }
    }
    else{
        console.log(`${regionsMenuId}_${region}`);
        let elem = document.getElementById(`${regionsMenuId}_${region}`);
        if(forceCheck)
            elem.checked = true;
        else
            elem.checked = !elem.checked;
    }
}

function createRegionsMenu(regionsMenuId){
    let regMenu = document.getElementById(regionsMenuId);
    let regMenuHtml = "";
    for(let i =0;i<regionsNames.length;i+=4){
        regMenuHtml+=`<div class="flex">`;
        for(let j=0;j<4;j++){
            regMenuHtml+=`  
            <div class="form-check regionCheckBox">
                <input id="${regionsMenuId}_${regionsNames[i+j]}" class="form-check-input" type="checkbox" value="">
                <label class="form-check-label" onclick="clickRegion('${regionsMenuId}','${regionsNames[i+j]}')">
                ${regionsNames[i+j]}
                </label>
                <div class="regionMenuStatus" id="${regionsMenuId}_${regionsNames[i+j]}_status"></div>
            </div>`;
        }
        regMenuHtml+="</div>";
    }
    regMenuHtml+=`
            <hr/>
            <div class="flex">
                <button class="btn btn-outline-dark" onclick="clickRegion('${regionsMenuId}','europe');">Europe</button>
                <button class="btn btn-outline-dark" onclick="clickRegion('${regionsMenuId}','asia');">Asia</button>
                <button class="btn btn-outline-dark" onclick="clickRegion('${regionsMenuId}','all');">All</button>
                <button class="btn btn-outline-dark" onclick="clickRegion('${regionsMenuId}','none');">None</button>

            </div>
    `;
    regMenu.innerHTML = regMenuHtml;
}

function clickRegionsMenu(regionsMenuId){
    if(document.getElementById(regionsMenuId).childElementCount==0)
        createRegionsMenu(regionsMenuId);
    setTimeout(()=>{
        let regionsMenu = document.getElementById(regionsMenuId);
        switch(regionsMenu.style.display){
            case "none":
                regionsMenu.style.display = "block";
                for(let reg in marketStatus){
                    let statusElem = document.getElementById(`${regionsMenuId}_${reg}_status`);
                    let color = "";
                    if(marketStatus[reg]["open"]){
                        if(marketStatus[reg]["realtime"])
                            color="#00edffe0";
                        else
                            color="#00ff0acf";
                    }
                    else
                        color="#ff0000cf";
                    statusElem.style.backgroundColor = color;
                }
                break;
            case "block":
                regionsMenu.style.display = "none";
                break;
        }
    }, 1);
  
}

function clickCapitalisation(capitalisationId){
    let btn = document.getElementById(capitalisationId);
    if(btn.value==0){
        btn.value=1;
        btn.classList.replace("btn-dark", "btn-primary");
    }
    else{
        btn.value=0;
        btn.classList.replace("btn-primary", "btn-dark");
    }
}


const HtmlInputFactory={
    numberInput:"Inmbr",
    floatInput:"Iflt",
    dataTypeInput:"Idtatyp",
    intervalTypeInput:"Iintrvltyp",
    formatTypeInput:"Ifrmttyp",
    regionsInput:"Irgns",
    capitalisationInput:"Icptlstn",
    dateInput:"Idte",
    dateRangeInput:"Idterng",
    selectInput:"Islct",
    checkboxInput:"Ichkbx",
    headerInput:"Ihdr",
    buttonInput:"Ibtn",
    buttonProgressBarInput:"Ibtnprgrssbr",
    
    idOption:"Oid",
    defaultValue0Option:"Odfltval0",
    defaultValue1Option:"Odfltval1",
    valueListOption:"Ovllst",
    titleOption:"Ottl",
    onClickOption:"Oonclk",
    onChangeOption:"Oonchng",
    disabledOption:"Odsbld",

    inheritValue:"Vinhrt",
    


    getHtmlInput:(input, options)=>{
        let elem = '<div class="flex">';
        let disabled = (options[HtmlInputFactory.disabledOption]!=undefined && options[HtmlInputFactory.disabledOption]) ? "disabled" : "";
        let onclick = options[HtmlInputFactory.onClickOption]!=undefined ? `onclick="${options[HtmlInputFactory.onClickOption]}"` : "";
        let onchange = options[HtmlInputFactory.onChangeOption]!=undefined ? `onclick="${options[HtmlInputFactory.onChangeOption]}"` : "";
        let getSelectedAttr = (v0, v1)=> (v0==v1 ? "selected" : "");
        let v;
        switch(input){            
            case HtmlInputFactory.floatInput:
            case HtmlInputFactory.numberInput:
                elem+=`
                    <div class="bd w-200">${options[HtmlInputFactory.titleOption]}</div>
                    <div class="input-group mb-1">
                        <input style="height: 30px;" value="${options[HtmlInputFactory.defaultValue0Option]}" type="number" class="form-control" id="${options[HtmlInputFactory.idOption]}" ${onclick} ${onchange} ${disabled}>
                    </div>
                `;
                break;
            case HtmlInputFactory.dataTypeInput:
                v = options[HtmlInputFactory.defaultValue0Option]
                if(v == HtmlInputFactory.inheritValue)
                    v = getTypeValue()
                elem+=`
                    <div class="bd w-200">data type</div>
                    <div class="input-group mb-1">
                        <select id="${options[HtmlInputFactory.idOption]}" class="form-select" style="height: 33px" ${onclick} ${onchange} ${disabled} >
                            <option value="open" ${getSelectedAttr(v, "open")}>open</option>
                            <option value="close" ${getSelectedAttr(v, "close")}>close</option>
                            <option value="adjclose" ${getSelectedAttr(v, "adjclose")}>adjclose</option>
                            <option value="volume" ${getSelectedAttr(v, "volume")}>volume</option>
                        </select>            
                    </div>                  
                `;
                break;
            case HtmlInputFactory.intervalTypeInput:
                v = options[HtmlInputFactory.defaultValue0Option]
                if(v == HtmlInputFactory.inheritValue)
                    v = getIntervalValue()
                elem+=`
                    <div class="bd w-200">interval type</div>
                    <div class="input-group mb-1">
                        <select id="${options[HtmlInputFactory.idOption]}" class="form-select" style="height: 33px" ${onclick} ${onchange} ${disabled} >
                            <option value="d" ${getSelectedAttr(v, "d")}>daily</option>
                            <option value="wk" ${getSelectedAttr(v, "wk")}>weekly</option>
                            <option value="mo" ${getSelectedAttr(v, "mo")}>monthly</option>
                        </select>            
                    </div>                 
                `;
                break;
            case HtmlInputFactory.formatTypeInput:
                let title = "format type"
                if(options[HtmlInputFactory.titleOption] !== undefined)
                    title = options[HtmlInputFactory.titleOption]
                elem+=`
                    <div class="bd w-200">${title}</div>
                    <div class="input-group mb-1">
                        <select id="${options[HtmlInputFactory.idOption]}" class="form-select" style="height: 33px" ${onclick} ${onchange} ${disabled} >
                            <option value="value">prices</option>
                            <option value="perc">percentage</option>
                            <option value="deltaPerc">delta percentage</option>
                        </select>            
                    </div>                
                `;
                break;
            case HtmlInputFactory.regionsInput:
                elem+=`
                    <div class="bd w-200">regions</div>
                    <div style="position:relative" class="dropdown show" >
                        <a class="btn btn-secondary dropdown-toggle" onclick="clickRegionsMenu('${options[HtmlInputFactory.idOption]}');" href="#" role="button"  data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Regions</a>
                        <div style="display: none" class="regionMenu" id="${options[HtmlInputFactory.idOption]}"></div>                    
                    </div>                 
                `;
                break;
            case HtmlInputFactory.capitalisationInput:
                elem+=`
                    <div class="bd w-200">capitalisation</div>
                    <div class="flex" style="justify-content:start">
                        <button id="${options[HtmlInputFactory.idOption]}_small" onclick="clickCapitalisation('${options[HtmlInputFactory.idOption]}_small')" class="btn btn-primary fl" value="1" style="border-top-right-radius:0;border-bottom-right-radius:0" >Small</button>
                        <button id="${options[HtmlInputFactory.idOption]}_mid" onclick="clickCapitalisation('${options[HtmlInputFactory.idOption]}_mid')" class="btn btn-primary fl" value="1" style="border-radius:0" >Mid</button>
                        <button id="${options[HtmlInputFactory.idOption]}_large" onclick="clickCapitalisation('${options[HtmlInputFactory.idOption]}_large')" class="btn btn-primary fl" value="1" style="border-radius:0" >Large</button>
                        <button id="${options[HtmlInputFactory.idOption]}_mega" onclick="clickCapitalisation('${options[HtmlInputFactory.idOption]}_mega')" class="btn btn-primary fl" value="1" style="border-top-left-radius:0;border-bottom-left-radius:0" >Mega</button>
                        <div class="cl"></div>
                    </div>              
                `;
                break;
            case HtmlInputFactory.dateInput:
                v = options[HtmlInputFactory.defaultValue0Option]
                if(v == HtmlInputFactory.inheritValue)
                    v = marketListCheck_to.value;
                elem+=`
                    <div class="bd w-200">${options[HtmlInputFactory.titleOption]}</div>
                    <input type="date" class="form-control" id="${options[HtmlInputFactory.idOption]}" ${onclick} ${onchange} ${disabled} value="${v}" min="1971-01-01"/>    
                `;
                break;
            case HtmlInputFactory.dateRangeInput:
                let v0 = options[HtmlInputFactory.defaultValue0Option]
                if(v0 == HtmlInputFactory.inheritValue)
                    v0 = marketListCheck_from.value;
                let v1 = options[HtmlInputFactory.defaultValue1Option]
                if(v1 == HtmlInputFactory.inheritValue)
                    v1 = marketListCheck_to.value;
                elem+=`
                    <div class="bd w-200">${options[HtmlInputFactory.titleOption]}</div>
                    <div class="bd">from</div>
                    <input type="date" class="form-control" id="${options[HtmlInputFactory.idOption]}_from" ${onclick} ${onchange} ${disabled} value="${v0}" min="1971-01-01"/>    
                    <div class="bd">to</div>
                    <input type="date" class="form-control" id="${options[HtmlInputFactory.idOption]}_to" ${onclick} ${onchange} ${disabled} value="${v1}" min="1971-01-01"/>                    
                `;
                break;
            case HtmlInputFactory.selectInput:
                let valueList = options[HtmlInputFactory.valueListOption];
                elem+=`
                    <div class="bd w-200">${options[HtmlInputFactory.titleOption]}</div>
                    <div class="input-group mb-1">
                        <select id="${options[HtmlInputFactory.idOption]}" class="form-select" style="height: 33px" ${onclick} ${onchange} ${disabled} >`;
                for(let key in valueList){
                    elem+=`<option value="${valueList[key]}">${key}</option>`;
                }
                elem+=`
                        </select>            
                    </div>                
                `;
                break;
            case HtmlInputFactory.checkboxInput:
                v = options[HtmlInputFactory.defaultValue0Option] ? "checked" : "";
                elem+=`
                    <div class="bd w-200">${options[HtmlInputFactory.titleOption]}</div>
                    <div class="form-check" style="height:15px">
                        <input ${v} class="form-check-input" style="height:15px;width:15px;" type="checkbox"  id="${options[HtmlInputFactory.idOption]}" ${onclick} ${onchange} ${disabled}  >
                    </div>
                `;
                break;
            case HtmlInputFactory.headerInput:
                elem+=`
                    <div class="bd w-200" ${onclick}>${options[HtmlInputFactory.titleOption]}</div>
                `;
                break;
            case HtmlInputFactory.buttonInput:
                elem+=`
                    <button class="btn btn-outline-dark" ${onclick} ${disabled} >${options[HtmlInputFactory.titleOption]}</button>         
                `;
                break;
            case HtmlInputFactory.buttonProgressBarInput:
                elem+=`
                    <button class="btn btn-outline-dark" ${onclick} ${disabled} >${options[HtmlInputFactory.titleOption]}</button>
                    <div class="progress" style="width:80%">
                        <div id="${options[HtmlInputFactory.idOption]}" ${disabled} class="progress-bar progress-bar-striped bg-info" role="progressbar" style="width: 0" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>                
                `;
                break;
            
            default:
                elem+=`<div>input not found, i:${input}, o:${JSON.stringify(options)}</div>`;
                break;
        }

        elem+='</div>';
        return elem;
    },

    getValueInput:(input)=>{
        let type = input.type;
        let options = input.options;
        switch(type){
            case HtmlInputFactory.capitalisationInput:
                return getSelectedCapitalisations(options[HtmlInputFactory.idOption]);
            case HtmlInputFactory.regionsInput:
                return getSelectedRegions(options[HtmlInputFactory.idOption]);
            case HtmlInputFactory.dateRangeInput:
                return [
                    document.getElementById(options[HtmlInputFactory.idOption]+"_from").value,
                    document.getElementById(options[HtmlInputFactory.idOption]+"_to").value
                ];
            case HtmlInputFactory.numberInput:
                return parseInt(document.getElementById(options[HtmlInputFactory.idOption]).value)
            case HtmlInputFactory.floatInput:
                return parseFloat(document.getElementById(options[HtmlInputFactory.idOption]).value)
            case HtmlInputFactory.checkboxInput:
                return document.getElementById(options[HtmlInputFactory.idOption]).checked;
            default:
                return document.getElementById(options[HtmlInputFactory.idOption]).value;
        }
    }
    
}

function openSimulationPanel(){
    window.scrollTo(0, 0);
    simulationPanel.style.display="block";
    document.getElementById("html").style.overflowY="hidden";
    removeCharts();
}

function closeSimulationPanel(){
    simulationPanel.style.display="none";
    document.getElementById("html").style.overflowY="scroll";
    updateStatistics();
}


function insertHtmlIndicator(indicator){
    let content = `
        <div class="statsPageDataList" style="width:auto;margin:40px 20px">
            <div style="width:700px">
    `;
    let first=true;
    for(let i of indicator.inputs){
        if(!first)
            content+="<hr/>";
        first=false
        content+=HtmlInputFactory.getHtmlInput(i.type, i.options);       
    }
    content+=`</div></div>${indicator.nextHTML}`;
    simulationContent.innerHTML=content;
}

function runIndicator(titles, indicator){
    simulationTitles = titles;
    openSimulationPanel()
    insertHtmlIndicator(indicator);
    indicator.openCallback();
}

function Option(key, value){
    this.key = key;
    this.value = value;
}

function Input(name, type, optionsList){
    this.name = name;
    this.type = type;
    this.options = {};
    for(let o of optionsList){
        this.options[o.key] = o.value;
    }
    this.getElement = ()=>{
        return document.getElementById(this.options[HtmlInputFactory.idOption]);
    }
    this.getId = ()=>{
        return this.options[HtmlInputFactory.idOption];
    }
}


function Indicator(name, inputs, nextHTML, openCallback=()=>{}){
    console.log(name);
    console.log(inputs);
    this.name = name;
    this.inputs = inputs;
    this.nextHTML = nextHTML;
    this.openCallback = openCallback
    for(let i of this.inputs){
        let h = Math.abs(hash(JSON.stringify(i)));
        let n = name.replaceAll(" ","");
        i.options[HtmlInputFactory.idOption] = `input_${n}_${h}`;
    }
    this.getInputByName = (name)=>{
        for(let i of this.inputs){
            if(i.name==name)
                return i;
        }
        return null;
    };
    this.getInputValue = (name)=>{
        let input = this.getInputByName(name);
        return HtmlInputFactory.getValueInput(input);
    };
    this.getInputsValues =(...names)=>{
        let result = [];
        for(let n of names){
            console.log(n);
            result.push(this.getInputValue(n));
        }
        return result;
    };
    this.getAllInputsValues = ()=>{
        let result = [];
        for(let i of this.inputs){
            result.push(HtmlInputFactory.getValueInput(i));
      }
        return result;
    };

}

function getDefaultChartOptions(chartId, chartHeight=null){
    let chart = document.getElementById(chartId)
    let options = {
        top:0,
        bottom:0,
        chartArea: {
            width: chart.offsetWidth*0.8
        }
    };
    if(chartHeight!=null)
        options.chartArea.height = (chartHeight-40);
    return options;
}

function setChartHeight(chartId, height){
    let chart = document.getElementById(chartId);
    chart.style.height = height+"px";
}