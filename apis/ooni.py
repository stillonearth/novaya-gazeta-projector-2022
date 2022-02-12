import requests

def get_asn(asn, limit, offset):
    """Данные мониторинга провайдера"""
    link = "https://api.ooni.io/api/_/website_urls?probe_cc=RU&probe_asn={}&limit={}&offset={}".format(asn, limit, offset)
    r = requests.get(link)
    return [i for i in r.json()['results']]

def list_asn():
    """Список провайдеров РФ, мониторинг которых осуществляется OONI"""
    r = requests.get('https://api.ooni.io/api/_/website_networks?probe_cc=RU')
    return [i['probe_asn'] for i in r.json()['results']]

def get_blocked_url_data(asn, domain):
    """Данные о блокировках домена"""
    all_items = []
    i = 0
    while True:
        url = "https://api.ooni.io/api/v1/measurements?limit=50&failure=false&probe_cc=RU&domain={}&probe_asn={}&test_name=web_connectivity&since=2015-01-01&until=2022-02-12&anomaly=true&offset={}".format(asn, domain, i*50)
        try:
            results = requests.get(url).json()['results']
        except:
            break

        all_items += results
        if len(results) < 50:
            break
        i += 1

    return all_items

def fetch_ooni():
    links = {}

    for asn in Bar('Countdown', check_tty=False).iter(asn_list):
        links[asn] = []
        offset = 0
        while True:
            batch = get_asn(asn, 50, offset*50)
            links[asn] += batch
            if len(batch) < 50 or offset > 10:
                break
            offset += 1
    
    links = {}
    return 