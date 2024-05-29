import pandas as pd
import eel
import time
import requests


requestHeader = {
    "Host": "query1.finance.yahoo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",    "Upgrade-Insecure-Requests": "1",
    "Cookie": "A3=d=AQABBGsrHGUCEJLfk6jwialcr4U1OUFzQUYFEgAACAHt8WUiZudVb2UB9qMAAAcIayscZUFzQUYID5vc8d2S8mYEiBe6cprBswkBBwoB3Q&S=AQAAAs5BXlimiiyRnEt7kF0KkjY; A1=d=AQABBGsrHGUCEJLfk6jwialcr4U1OUFzQUYFEgAACAHt8WUiZudVb2UB9qMAAAcIayscZUFzQUYID5vc8d2S8mYEiBe6cprBswkBBwoB3Q&S=AQAAAs5BXlimiiyRnEt7kF0KkjY; GUC=AQAACAFl8e1mIkIfJgSt&s=AQAAAFcXkJ1O&g=ZfCm1w; OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiUFNESzVNTjRYN0xWRjVVMzJTR1AzNTVDV1kiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiIxZXBNbkMyMWhmbjkifX0.uVZ1PMsWmbl8EBrsCYaDa1xpFQdlInXecdyUqAPaQNSxro9447GvRX97Yonc7Dk2usPwT8ygXpQuQhDiYl8Tj0Fu5OCNuo_JoVEoyfV7GrlYm3-yM2oxWjicO53qWfPHeE050D2H4AfFw_lASAagpoHuN2eTlEj7SG14EL2mMpU; T=af=JnRzPTE3MTAyNzAxNDMmcHM9MzZyNnBoSmhoXzUwRFN0aWdJQlVtUS0t&d=bnMBeWFob28BZwFQU0RLNU1ONFg3TFZGNVUzMlNHUDM1NUNXWQFhYwFBTVlSdDZGcgFhbAFhbmRlcmxpbmlsZW9uYXJkbzIwMjBAZ21haWwuY29tAXNjAW1icl9sb2dpbgFmcwFIZzZyanJCbDhLYW8BenoBL2FLOGxCQTdFAWEBUUFFAWxhdAEvYUs4bEIBbnUBMA--&kt=EAAsGitdcakPGbY7irhMab_UQ--~I&ku=FAAorceeKNG.dFwPvHECfavzXuPQWkdaBpQrGQlQKgb8SimM0JGDaieeHi_4t1nV.fzzq4dXhPHXjZ9b6mlU7ApxAA.EAq.SjisF.ObYlJilkAQ24C9eFlOj8CRU2q8ldx_LzyVSK26Rvg8VTg1GC7oynUiGXYYlAbBZO5rxS_xYyE-~E; F=d=GzmZX_s9vJVWdy9AtP9WyR.sUT1t94C_KyfMZQucvctigjhhRz0cVK51Ud2PxXG1vMy7; PH=l=it-IT; Y=v=1&n=5sggjh94ph61e&l=ix0gc8w961a6944l5hmwm6n5uhk3m0bke9pgsmhn/o&p=n38vvit00000000&r=1d5&intl=it; cmp=t=1711488666&j=1&u=1---&v=19; PRF=t%3DFTSEMIB.MI%252BAAPL%26newChartbetateaser%3D0%252C1711488327445; A1S=d=AQABBGsrHGUCEJLfk6jwialcr4U1OUFzQUYFEgAACAHt8WUiZudVb2UB9qMAAAcIayscZUFzQUYID5vc8d2S8mYEiBe6cprBswkBBwoB3Q&S=AQAAAs5BXlimiiyRnEt7kF0KkjY",
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


def getYaMarketData( retryCount = 0):
    CRUMB = "nQGWAqVg.Xy"
    #req = requests.get(f"https://query1.finance.yahoo.com/v1/finance/screener/instrument/equity/new?crumb={CRUMB}&lang=it-IT&region=IT&corsDomain=it.finance.yahoo.com", headers=requestHeader)
    #payload = {"requests":{"g0":{"resource":"StreamService","operation":"read","params":{"ui":{"editorial_featured_count":1,"image_quality_override":1,"link_out_allowed":1,"ntk_bypassA3c":1,"pubtime_maxage":-1,"storyline_count":2,"storyline_min":2,"thumbnail_size":100,"view":"sidekick","editorial_content_count":0,"finance_upsell_threshold":4},"category":"SIDEKICK:TOPSTORIES","forceJpg":1,"releasesParams":{"limit":20,"offset":0},"offnet":{"include_lcp":1,"use_preview":1},"useNCP":1,"ads":{"ad_polices":1,"count":25,"frequency":4,"generic_viewability":1,"partial_viewability":1,"pu":"finance.yahoo.com","se":4492794,"spaceid":1185835883,"start_index":2,"timeout":0,"type":"STRM,STRM_CONTENT","useHqImg":1,"useResizedImages":1},"batches":{"size":48,"timeout":500,"total":170},"blending_enabled":1,"enableAuthorBio":1,"max_exclude":10,"min_count":3,"service":{"specRetry":{"enabled":0}},"pageContext":{"pageType":"utility","subscribed":"0","tier":"0","enablePremium":"0","eventName":"","topicName":"","category":"","quoteType":"","calendarType":"","screenerType":"new","inTrial":"0","cryptoUser":"0","enableTrading":"0","hubName":""},"content_type":"screener","content_site":"finance","exclude_uuids":[]}}},"context":{"feature":"canvassOffnet,ccOnMute,disableCommentsMessage,debouncesearch100,deferDarla,disableMegaModalSa,ecmaModern,enable3pConsent,enableCCPAFooter,enableNewCCPAFooter,enableCMP,enableConsentData,enableEncryption,enableEVPlayer,enableFBRedirect,enableFreeFinRichSearch,enableGAMAds,enableGAMBrokerButtonEvent,enableGuceJs,enableGuceJsOverlay,enableNcpVideo,enablePortfolioBasicEolFlow,enablePrivacyUpdate,enableUpgradeLeafPage,enableVideoURL,enableYodleeErrorMsgCriOS,ncpPortfolioStream,ncpQspStream,ncpQspStreamV2,upgradeNCPQueries,ncpStream,ncpStreamIntl,ncpTopicStream,newContentAttribution,newLogo,notificationsServiceWorker,oathPlayer,relatedVideoFeatureOff,removeConversations,useNextGenHistory,videoNativePlaylist,enableComscoreUdm2,sunsetMotif2,enableUserPrefAPI,enableCustomSymbolsTotalGain,enableHeaderBidding,enablePortfolioHoldingsRedesign,enableOnlyBetaPortfoliosCreation,enablePortfolioHoldingsRedesignMweb,enableNCPChannel,enableSingleRail,enhanceAddToWL,article2_csn,enableStageAds,sponsoredAds,enableNativeBillboard,enableLiveDynamicData","bkt":"finance-IT-it-IT-def","crumb":{CRUMB},"device":"desktop","intl":"it","lang":"it-IT","partner":"none","prid":"6qqd7jhj5dvh6","region":"IT","site":"finance","tz":"Europe/Rome","ver":"0.10101010102.490","ecma":"modern"}}
    #req = requests.post(f"https://it.finance.yahoo.com/_finance_doubledown/api/resource?bkt=finance-IT-it-IT-def&crumb=nQGWAqVg.Xy&device=desktop&ecma=modern&feature=canvassOffnet%2CccOnMute%2CdisableCommentsMessage%2Cdebouncesearch100%2CdeferDarla%2CdisableMegaModalSa%2CecmaModern%2Cenable3pConsent%2CenableCCPAFooter%2CenableNewCCPAFooter%2CenableCMP%2CenableConsentData%2CenableEncryption%2CenableEVPlayer%2CenableFBRedirect%2CenableFreeFinRichSearch%2CenableGAMAds%2CenableGAMBrokerButtonEvent%2CenableGuceJs%2CenableGuceJsOverlay%2CenableNcpVideo%2CenablePortfolioBasicEolFlow%2CenablePrivacyUpdate%2CenableUpgradeLeafPage%2CenableVideoURL%2CenableYodleeErrorMsgCriOS%2CncpPortfolioStream%2CncpQspStream%2CncpQspStreamV2%2CupgradeNCPQueries%2CncpStream%2CncpStreamIntl%2CncpTopicStream%2CnewContentAttribution%2CnewLogo%2CnotificationsServiceWorker%2CoathPlayer%2CrelatedVideoFeatureOff%2CremoveConversations%2CuseNextGenHistory%2CvideoNativePlaylist%2CenableComscoreUdm2%2CsunsetMotif2%2CenableUserPrefAPI%2CenableCustomSymbolsTotalGain%2CenableHeaderBidding%2CenablePortfolioHoldingsRedesign%2CenableOnlyBetaPortfoliosCreation%2CenablePortfolioHoldingsRedesignMweb%2CenableNCPChannel%2CenableSingleRail%2CenhanceAddToWL%2Carticle2_csn%2CenableStageAds%2CsponsoredAds%2CenableNativeBillboard%2CenableLiveDynamicData&intl=it&lang=it-IT&partner=none&prid=6qqd7jhj5dvh6&region=IT&site=finance&tz=Europe%2FRome&ver=0.10101010102.490", headers=requestHeader, json=payload)
    data = []
    for o in range(0, 3000, 100):
        payload = {"size":100,"offset":o,"sortField":"intradaymarketcap","sortType":"DESC","quoteType":"EQUITY","topOperator":"AND","query":{"operator":"AND","operands":[{"operator":"gt","operands":["avgdailyvol3m",0]},{"operator":"gt","operands":["intradaypricechange",0]}]},"userId":"","userIdType":"guid"}
        req = requests.post(f"https://query2.finance.yahoo.com/v1/finance/screener?crumb={CRUMB}&lang=it-IT&region=IT&formatted=true&corsDomain=it.finance.yahoo.com", headers=requestHeader2, json=payload).json()
        reqList = req["finance"]["result"][0]["quotes"]
        for d in reqList:
            if d["averageDailyVolume3Month"]["raw"] > 0:
                data.append({"symbol":d["symbol"], "valueDeltaPerc":d["regularMarketChangePercent"]["raw"], "volume":d["regularMarketVolume"]["raw"], "volumeAvg":d["averageDailyVolume3Month"]["raw"], "volumeDeltaPerc":(d["regularMarketVolume"]["raw"]-d["averageDailyVolume3Month"]["raw"])*100/d["averageDailyVolume3Month"]["raw"]} )
    print(len(data))
    return data

class AlertChecker:
    
    def __init__(self, titleList):
        self.titleList = titleList
        self.data = None
        self.alerts = []

    def getData(self):
        try:
            self.data = getYaMarketData()
        except ConnectionError:
            print("alert connection error")



    def fastCheck(self, volumePerc, valuePerc, minVolume):
        if(self.data==None):
            self.getData()
        self.alerts = [d for d in self.data if d["volumeAvg"]>minVolume and d["volumeDeltaPerc"]>=volumePerc and d["valueDeltaPerc"]>=valuePerc]
        orderObjectListBy(self.alerts, "volumeDeltaPerc")
            
            
