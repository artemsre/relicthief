from prometheus_client import start_http_server, Summary, Counter, Gauge
import random
import time
import os
import sys
import requests
import logging

metrics = ['apdex_score','response_time','throughput','error_rate']
slametrics = ['latency_ms','sla_apdex','success_rate']
gauge_metrics=dict()
for m in metrics:
    gauge_metrics[m] = Gauge(f'newrelic:{m}',m, ['app'])
for m in slametrics:
    gauge_metrics[m] = Gauge(f'newrelic:synthetic:sla:{m}',m, ['app','periodays'])

def getSyntheticMonitoringlist():
    url="https://synthetics.newrelic.com/synthetics/api/v3/monitors"
    monitors={}
    headers = {'Api-Key': NRKEY}
    try:
        r = requests.get(url, timeout=5, headers=headers)
        if r.status_code > 299:
            logging.warning(f'Responce status Error {r.status_code} {r.text}') 
        responce=r.json()['monitors']
        for r in responce:
            if "status" in r and "name" in r and "slaThreshold" in r:
                if r["status"] == "ENABLED":
                    monitors[r["name"]] = r["slaThreshold"]
    except Exception as err:
        logging.warning('getSyntheticMonitoringlist Connection Error'+str(err)) 
        return []
    return monitors

def getSLAmetric(monitor_name, apdex_ms, period_days):
    url=f"https://insights-api.newrelic.com/v1/accounts/{ACCOUNT_ID}/query?"
    payload = {'nrql': f"SELECT average(duration), apdex(duration, {apdex_ms}) as apdex, percentage(count(*), WHERE result='SUCCESS') FROM SyntheticCheck SINCE {period_days} day ago WHERE monitorName = '{monitor_name}'"}
    headers = {'Accept': 'application/json', 'X-Query-Key': QUERY_KEY}
    data={}
    try:
        r = requests.get(url, timeout=5, headers=headers,params=payload)
        if r.status_code > 299:
            logging.warning(f'getSLAmetric Responce status Error {r.status_code} {r.text}') 
        responce=r.json()['results']
        for obj in responce:
            if 'average' in obj:
                data["latency_ms"]=round(obj['average'],2)
            if 'score' in obj:
                data["sla_apdex"]=round(obj['score'],2)
            if 'result' in obj:
                data["success_rate"]=round(obj['result'],2)
    except Exception as err:
        logging.warning('getSLAmetric Connection Error'+str(err)) 
        return {}
    return data


if __name__ == '__main__':
    last_sla_scrape=time.time()-4000
    NRKEY=os.getenv('NEWRELIC_APIKEY')
    if not NRKEY or len(NRKEY) < 3:
        print("ERROR: NEWRELIC_APIKEY env variable is not defined. Exit")
        sys.exit()
    QUERY_KEY=os.getenv('NEWRELIC_QUERY_API')
    if not QUERY_KEY or len(QUERY_KEY) < 3:
        print("ERROR: NEWRELIC_QUERY_API env variable is not defined. Exit")
        sys.exit()
    ACCOUNT_ID=os.getenv('NEWRELIC_ACCOUNT_ID')
    if not ACCOUNT_ID or len(ACCOUNT_ID) < 3:
        print("ERROR: NEWRELIC_ACCOUNT_ID env variable is not defined. Exit")
        sys.exit()
    start_http_server(8000)
    while True:
        url = 'https://api.newrelic.com/v2/applications.json'
        headers = {'Api-Key': NRKEY}
        apps=[]
        try:
            r = requests.get(url, timeout=5, headers=headers)
            if r.status_code > 299:
                logging.warning(f'Responce status Error {r.status_code} {r.text}') 
            apps=r.json()['applications']
        except Exception as err:
            logging.warning('Connection Error'+str(err)) 
        for app in apps:
            if 'name' in app:
                if 'application_summary' not in app:
                    logging.warning(f'There are no "application_summary" object in {app["name"]} structure')
                    continue
                try:
                    for m in metrics:
                        if m in app['application_summary']:
                            gauge_metrics[m].labels(app['name']).set(app['application_summary'][m])
                        else:
                            logging.warning(f'There is not metric "{m}" in {app["name"]} application_summary output {app["application_summary"]}')
                except Exception as e:
                    logging.warning(f'Error parse json output: {e}')
        monitors = getSyntheticMonitoringlist()
        # sla scrape only once per hour
        if time.time() > (last_sla_scrape + 60*60):
            for m in monitors:
                for d in [1,7,30]:
                    slas = getSLAmetric(m,monitors[m]*1000,d)
                    for sla in slas:
                        gauge_metrics[sla].labels(m,d).set(slas[sla])
            last_sla_scrape=time.time()
        time.sleep(300)
