import pandas as pd
import eel
import time
import requests
import re
from datetime import datetime
from currencyCoverter import CurrencyConverter
from threading import Thread
from threadStopper import threadStop



requestHeader = {
    "Host": "query1.finance.yahoo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",    "Upgrade-Insecure-Requests": "1",
    "Cookie": "A3=d=AQABBFqE5l8CEL7R-eecHzVTxCatVIRtRikFEgABCAGDemasZudVb2UB9qMAAAcIWoTmX4RtRik&S=AQAAAvarvbzeS7_rPOIchc_8ygw; A1=d=AQABBFqE5l8CEL7R-eecHzVTxCatVIRtRikFEgABCAGDemasZudVb2UB9qMAAAcIWoTmX4RtRik&S=AQAAAvarvbzeS7_rPOIchc_8ygw; GUC=AQABCAFmeoNmrEIhWAS0&s=AQAAAKqeFOvd&g=Znk0ww; cmp=t=1719219388&j=1&u=1---&v=31; PRF=t%3DSD%252B%255EDJI%252B%255EIXIC%252BCL%253DF; A1S=d=AQABBFqE5l8CEL7R-eecHzVTxCatVIRtRikFEgABCAGDemasZudVb2UB9qMAAAcIWoTmX4RtRik&S=AQAAAvarvbzeS7_rPOIchc_8ygw; GUCS=ASmcRCXb; EuConsent=CP9oCIAP9oCIAAOACBITA5EoAP_gAEPgACiQJhNB9G7WTXFneXp2YPskOYUX0VBJ4MAwBgCBAcABzBIUIAwGVmAzJEyIICACGAIAIGJBIABtGAhAQEAAYIAFAABIAEEAABAAIGAAACAAAABACAAAAAAAAAAQgEAXMBQgmAZEAFoIQUhAhgAgAQAAAAAEAIgBAgQAEAAAQAAICAAIACgAAgAAAAAAAAAEAFAIEQAAAAECAotkfQTBADINSogCLAkJCAQMIIEAIgoCACgQAAAAECAAAAmCAoQBgEqMBEAIAQAAAAAAAAQEACAAACABCAAIAAgQAAAAAQAAAAACAAAEAAAAAAAAAAAAAAAAAAAAAAAAAMQAhBAACAACAAgoAAAABAAAAAAAAAARAAAAAAAAAAAAAAAAARAAAAAAAAAAAAAAAAAAAQAAAAAAAABAAILAAA",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "domain-id": "it"}


requestHeader2= {
    "Accept":
"*/*",
"Accept-Encoding":
"gzip, deflate, br, zstd",
"Accept-Language":
"it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
"Content-Length":
"290",
"Content-Type":
"application/json",
"Cookie":
"A1S=d=AQABBLvoVmYCEA65o37vfAXmpU6jvBAwu-EFEgABCAEtWGZ-ZudVb2UB9qMAAAcItuhWZqwaXgw&S=AQAAAifGbSAh9BN-grERtzge-yM; A3=d=AQABBLvoVmYCEA65o37vfAXmpU6jvBAwu-EFEgABCAEtWGZ-ZudVb2UB9qMAAAcItuhWZqwaXgw&S=AQAAAifGbSAh9BN-grERtzge-yM; GUC=AQABCAFmWC1mfkIh4QTQ&s=AQAAAHRWydGh&g=ZlboxQ; EuConsent=CP_YGAAP_YGAAAOACBITA2EoAP_gAEPgACiQJhNB9G7WTXFneXp2YPskOYUX0VBJ4MAwBgCBAcABzBIUIAwGVmAzJEyIICACGAIAIGJBIABtGAhAQEAAYIAFAABIAEEAIBAAIGAAACAAAABACAAAAAAAAAAQgEAXMBQgmAZEBFoIQUhAhgAgAQAAIAAEAIgBAgQAEAAAQAAICAAIACgAAgAAAAAAAAAEAFAIEQAAAAECAotkfQTBADINSogCLAkJCAQMIIEAIgoCACgQAAAAECAAAAmCAoQBgEqMBEAIAQAAAAAAAAQEACAAACABCAAIAAgQAAAAAQAAAAQCAAAEAAAAAAAAAAAAAAAAAAAAAAAAAMQAhBAACACCAAgoAAAABAAAAAAAAAARAAAAAAAAAAAAAAAAARAAAAAAAAAAAAAAAAAAAQAAAAAAAABAAILAAA; A1=d=AQABBLvoVmYCEA65o37vfAXmpU6jvBAwu-EFEgABCAEtWGZ-ZudVb2UB9qMAAAcItuhWZqwaXgw&S=AQAAAifGbSAh9BN-grERtzge-yM; cmp=t=1716971708&j=1&u=1---&v=28; axids=gam=y-U8XSyS5E2uK6qNKZ1gov0lKqusQ_B_gp~A&dv360=eS05ckRuZFo1RTJ1SHNxWnY4RnpabHpIUm15cVQ4YS55aH5B&ydsp=y-IJzoiztE2uKx6XG4rUcCfB1TPwzDKHSb~A&tbla=y-S9VmDqlE2uIoY_OFHIq5004Tn6sJpW__~A; tbla_id=c9a9e4f8-9394-41da-b5cd-1127c36f0b8f-tuctd506e3d; PRF=t%3DPEGY",
"Origin":
"https://it.finance.yahoo.com",
"Priority":
"u=1, i",
"Referer":
"https://it.finance.yahoo.com/",
"Sec-Ch-Ua":
'"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
"Sec-Ch-Ua-Mobile":
"?0",
"Sec-Ch-Ua-Platform":
"Windows",
"Sec-Fetch-Dest":
"empty",
"Sec-Fetch-Mode":
"cors",
"Sec-Fetch-Site":
"same-site",
"User-Agent":
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}


def orderObjectListBy(list, column):
    for i in range(len(list)):
        for j in range(i+1, len(list)):
            if(list[i][column] < list[j][column]):
                tmp = list[i]
                list[i] = list[j]
                list[j] = tmp


regionsNames = {'Belgium': 'be', 'Austria': 'at', 'Argentina': 'ar', 'Australia': 'au', 'Brazil': 'br', 'Switzerland': 'ch', 'Canada': 'ca', 'Chile': 'cl', 'China': 'cn', 'Germany': 'de', 'Estonia': 'ee', 'Czechia': 'cz', 'Denmark': 'dk', 'Egypt': 'eg', 'Finland': 'fi', 'United Kingdom': 'gb', 'Indonesia': 'id', 'France': 'fr', 'Spain': 'es', 'Greece': 'gr', 'Hong Kong SAR China': 'hk', 'Israel': 'il', 'Hungary': 'hu', 'Ireland': 'ie', 'New Zealand': 'nz', 'Mexico': 'mx', 'Philippines': 'ph', 'Poland': 'pl', 'Netherlands': 'nl', 'Qatar': 'qa', 'Saudi Arabia': 'sa', 'Singapore': 'sg', 'Norway': 'no', 'Malaysia': 'my', 'Latvia': 'lv', 'Pakistan': 'pk', 'Portugal': 'pt', 'Russia': 'ru', 'Sweden': 'se', 'Peru': 'pe', 'Lithuania': 'lt', 'Italy': 'it', 'Iceland': 'is', 'Japan': 'jp', 'Kuwait': 'kw', 'South Korea': 'kr', 'India': 'in', 'Sri Lanka': 'lk', 'Thailand': 'th', 'Suriname': 'sr', 'United States': 'us', 'Taiwan': 'tw', 'Venezuela': 've', 'South Africa': 'za', 'Vietnam': 'vn', 'Turkey': 'tr'}
regionsLoaded = []



def getYaMarketData(progressBarId, regions, caps, currencyConverter: CurrencyConverter):
    CRUMB = "nQGWAqVg.Xy"
    #req = requests.get(f"https://query1.finance.yahoo.com/v1/finance/screener/instrument/equity/new?crumb={CRUMB}&lang=it-IT&region=IT&corsDomain=it.finance.yahoo.com", headers=requestHeader)
    #payload = {"requests":{"g0":{"resource":"StreamService","operation":"read","params":{"ui":{"editorial_featured_count":1,"image_quality_override":1,"link_out_allowed":1,"ntk_bypassA3c":1,"pubtime_maxage":-1,"storyline_count":2,"storyline_min":2,"thumbnail_size":100,"view":"sidekick","editorial_content_count":0,"finance_upsell_threshold":4},"category":"SIDEKICK:TOPSTORIES","forceJpg":1,"releasesParams":{"limit":20,"offset":0},"offnet":{"include_lcp":1,"use_preview":1},"useNCP":1,"ads":{"ad_polices":1,"count":25,"frequency":4,"generic_viewability":1,"partial_viewability":1,"pu":"finance.yahoo.com","se":4492794,"spaceid":1185835883,"start_index":2,"timeout":0,"type":"STRM,STRM_CONTENT","useHqImg":1,"useResizedImages":1},"batches":{"size":48,"timeout":500,"total":170},"blending_enabled":1,"enableAuthorBio":1,"max_exclude":10,"min_count":3,"service":{"specRetry":{"enabled":0}},"pageContext":{"pageType":"utility","subscribed":"0","tier":"0","enablePremium":"0","eventName":"","topicName":"","category":"","quoteType":"","calendarType":"","screenerType":"new","inTrial":"0","cryptoUser":"0","enableTrading":"0","hubName":""},"content_type":"screener","content_site":"finance","exclude_uuids":[]}}},"context":{"feature":"canvassOffnet,ccOnMute,disableCommentsMessage,debouncesearch100,deferDarla,disableMegaModalSa,ecmaModern,enable3pConsent,enableCCPAFooter,enableNewCCPAFooter,enableCMP,enableConsentData,enableEncryption,enableEVPlayer,enableFBRedirect,enableFreeFinRichSearch,enableGAMAds,enableGAMBrokerButtonEvent,enableGuceJs,enableGuceJsOverlay,enableNcpVideo,enablePortfolioBasicEolFlow,enablePrivacyUpdate,enableUpgradeLeafPage,enableVideoURL,enableYodleeErrorMsgCriOS,ncpPortfolioStream,ncpQspStream,ncpQspStreamV2,upgradeNCPQueries,ncpStream,ncpStreamIntl,ncpTopicStream,newContentAttribution,newLogo,notificationsServiceWorker,oathPlayer,relatedVideoFeatureOff,removeConversations,useNextGenHistory,videoNativePlaylist,enableComscoreUdm2,sunsetMotif2,enableUserPrefAPI,enableCustomSymbolsTotalGain,enableHeaderBidding,enablePortfolioHoldingsRedesign,enableOnlyBetaPortfoliosCreation,enablePortfolioHoldingsRedesignMweb,enableNCPChannel,enableSingleRail,enhanceAddToWL,article2_csn,enableStageAds,sponsoredAds,enableNativeBillboard,enableLiveDynamicData","bkt":"finance-IT-it-IT-def","crumb":{CRUMB},"device":"desktop","intl":"it","lang":"it-IT","partner":"none","prid":"6qqd7jhj5dvh6","region":"IT","site":"finance","tz":"Europe/Rome","ver":"0.10101010102.490","ecma":"modern"}}
    #req = requests.post(f"https://it.finance.yahoo.com/_finance_doubledown/api/resource?bkt=finance-IT-it-IT-def&crumb=nQGWAqVg.Xy&device=desktop&ecma=modern&feature=canvassOffnet%2CccOnMute%2CdisableCommentsMessage%2Cdebouncesearch100%2CdeferDarla%2CdisableMegaModalSa%2CecmaModern%2Cenable3pConsent%2CenableCCPAFooter%2CenableNewCCPAFooter%2CenableCMP%2CenableConsentData%2CenableEncryption%2CenableEVPlayer%2CenableFBRedirect%2CenableFreeFinRichSearch%2CenableGAMAds%2CenableGAMBrokerButtonEvent%2CenableGuceJs%2CenableGuceJsOverlay%2CenableNcpVideo%2CenablePortfolioBasicEolFlow%2CenablePrivacyUpdate%2CenableUpgradeLeafPage%2CenableVideoURL%2CenableYodleeErrorMsgCriOS%2CncpPortfolioStream%2CncpQspStream%2CncpQspStreamV2%2CupgradeNCPQueries%2CncpStream%2CncpStreamIntl%2CncpTopicStream%2CnewContentAttribution%2CnewLogo%2CnotificationsServiceWorker%2CoathPlayer%2CrelatedVideoFeatureOff%2CremoveConversations%2CuseNextGenHistory%2CvideoNativePlaylist%2CenableComscoreUdm2%2CsunsetMotif2%2CenableUserPrefAPI%2CenableCustomSymbolsTotalGain%2CenableHeaderBidding%2CenablePortfolioHoldingsRedesign%2CenableOnlyBetaPortfoliosCreation%2CenablePortfolioHoldingsRedesignMweb%2CenableNCPChannel%2CenableSingleRail%2CenhanceAddToWL%2Carticle2_csn%2CenableStageAds%2CsponsoredAds%2CenableNativeBillboard%2CenableLiveDynamicData&intl=it&lang=it-IT&partner=none&prid=6qqd7jhj5dvh6&region=IT&site=finance&tz=Europe%2FRome&ver=0.10101010102.490", headers=requestHeader, json=payload)
    data = []
    name=None
    rCount = 0
    if(progressBarId):
        eel.setProgress(progressBarId, 0)
    
    capsConditions = [{"operator":"LT","operands":["intradaymarketcap",2000000000]},
                      {"operator":"BTWN","operands":["intradaymarketcap",2000000000,10000000000]},
                      {"operator":"BTWN","operands":["intradaymarketcap",10000000000,100000000000]},
                      {"operator":"GT","operands":["intradaymarketcap",100000000000]}]

    filteredCapsConditions = []
    for c in caps:
        if(c!=-1):
            filteredCapsConditions.append(capsConditions[c])
    for r in regions:
        for o in range(0, 10000, 250):
            reqList=[]
            retryNum=10
            for retry in range(retryNum):
                try:
                    payload = {"size":250,"offset":o,"sortField":"dayvolume","sortType":"DESC","quoteType":"EQUITY","topOperator":"AND","query":{"operator":"AND","operands":[{"operator":"or","operands":[{"operator":"EQ","operands":["region", regionsNames[r]]}]},{"operator":"or","operands":filteredCapsConditions},{"operator":"gt","operands":["avgdailyvol3m",10]},{"operator":"gt","operands":["percentchange",0]},{"operator":"gt","operands":["dayvolume",10]}]},"userId":"","userIdType":"guid"}
                    req = requests.post(f"https://query2.finance.yahoo.com/v1/finance/screener?crumb={CRUMB}&lang=it-IT&region=IT&formatted=true&corsDomain=it.finance.yahoo.com", headers=requestHeader2, json=payload).json()
                    reqList = req["finance"]["result"][0]["quotes"]
                    break
                except:
                    if(retry==retryNum-1):
                        raise ConnectionError
                    continue
            if(len(reqList)==0):
                break
            for d in reqList:
                try:
                    if d["averageDailyVolume3Month"]["raw"] > 0:
                        try:
                            name = d["shortName"]
                        except KeyError:
                            try:
                                name = d["longName"]
                            except KeyError:
                                name = d["symbol"]

                        data.append({"symbol":d["symbol"],
                                    "name":name,
                                    "region":r,
                                    "valueDeltaPerc":round(d["regularMarketChangePercent"]["raw"], 3), 
                                    "volume":d["regularMarketVolume"]["raw"], 
                                    "volumeAvg":d["averageDailyVolume3Month"]["raw"], 
                                    "volumeDeltaPerc":round((d["regularMarketVolume"]["raw"]-d["averageDailyVolume3Month"]["raw"])*100/d["averageDailyVolume3Month"]["raw"]), 
                                    "marketState":d["marketState"], 
                                    "volumePrice":round(d["regularMarketPreviousClose"]["raw"]*d["regularMarketVolume"]["raw"]*currencyConverter.getUsdConversion(d["currency"]))} )

                except KeyError:
                    pass
            total = req["finance"]["result"][0]["total"]
            if(progressBarId):
                eel.setProgress(progressBarId, (rCount*100)/len(regions) + o*(1/len(regions)*100)/total)
        rCount+=1
    if(progressBarId):
        eel.setProgress(progressBarId, 100)
    print(len(data))
    return data


class AlertListener(Thread):
    def __init__(self,num, volumePerc, valuePerc, minVolume, minVolumePrice, regions, caps, refreshRate, currencyConverter : CurrencyConverter):
        Thread.__init__(self)
        self.stopped = False
        self.num=num
        self.volumePerc=volumePerc
        self.valuePerc=valuePerc
        self.minVolume=minVolume
        self.minVolumePrice=minVolumePrice
        self.regions=regions
        self.caps=caps
        self.refreshRate=refreshRate
        self.currencyConverter = currencyConverter
        self.oldSymbols = {}


    def run(self):
        while(not self.stopped and not threadStop.stop):
            try:
                alerts = getYaMarketData(None, self.regions, self.caps, self.currencyConverter)
                filteredAlerts = [d for d in alerts if d["volumeAvg"]>self.minVolume and 
                                            d["volumeDeltaPerc"]>=self.volumePerc and 
                                            d["valueDeltaPerc"]>=self.valuePerc and
                                            d["volumePrice"]>=self.minVolumePrice]
                
                symbolsUpdated = [a["symbol"] for a in filteredAlerts]
                notPresent = [a for a in self.oldSymbols if a not in  symbolsUpdated]
                
                for a in filteredAlerts:
                    if(a["symbol"] in self.oldSymbols):
                        a["time"] = self.oldSymbols[a["symbol"]]
                        a["new"] = 0
                    else:
                        a["time"] = datetime.now().time().replace(microsecond=0)
                        self.oldSymbols[a["symbol"]] = a["time"]
                        a["new"] = 1
                    a["deleted"] = 0

                for np in notPresent:
                    a = {"symbol":np, "time":self.oldSymbols[np], "deleted":1}
                    filteredAlerts.insert(0, a)

                orderObjectListBy(filteredAlerts, "time")

                for a in filteredAlerts:
                    a["time"] = str(a["time"])

                eel.applyAlertListenerTable(filteredAlerts, self.num)
            except ConnectionError:
                print("listener connection error")


            for t in range(self.refreshRate*60):
                time.sleep(1)
                if(threadStop.stop):
                    break
        



class AlertChecker:
    
    def __init__(self, titleList, currencyConverter : CurrencyConverter):
        self.titleList = titleList
        self.data = None
        self.alerts = []
        self.regions=[]
        self.caps=[]
        self.currencyConverter = currencyConverter
        self.alertListeners = {}

    def getData(self, progressBarId):
        try:
            self.data = getYaMarketData(progressBarId, self.regions, self.caps, self.currencyConverter)

        except ConnectionError:
            print("alert connection error")



    def check(self, volumePerc, valuePerc, minVolume, minVolumePrice, regions, caps, progressBarId, forceUpdateData = False):
        
        if(self.data==None or regions!=self.regions or caps!=self.caps  or forceUpdateData):
            self.regions = regions
            self.caps = caps
            self.getData(progressBarId)
        self.alerts = [d for d in self.data if d["volumeAvg"]>minVolume and 
                                                d["volumeDeltaPerc"]>=volumePerc and 
                                                d["valueDeltaPerc"]>=valuePerc and
                                                d["volumePrice"]>=minVolumePrice]
        orderObjectListBy(self.alerts, "volumeDeltaPerc")

    def addListener(self, num, volumePerc, valuePerc, minVolume, minVolumePrice, regions, caps, refreshRate):
        al = AlertListener(num, volumePerc, valuePerc, minVolume, minVolumePrice, regions, caps, refreshRate, self.currencyConverter)
        self.alertListeners[str(num)] = al
        al.start()

    def removeListener(self, num):
        self.alertListeners[str(num)].stopped = True
        del self.alertListeners[str(num)]

