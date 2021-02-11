# relicthief
NewRelic to prometehus exporter. 

We use NewRelic APM feature and Synthetic SLA test. 

There are needs to have one place for all dashboards. We use Grafana. 

The relicthief make REST API requests to NewRelic and provide numbers with prometheus /metric endpoints. 

There are two API KEYS (I do not know why it works in this way). 

```
# HELP newrelic:apdex_score apdex_score
# TYPE newrelic:apdex_score gauge
newrelic:apdex_score{app="sso-service"} 1.0
newrelic:apdex_score{app="file_uploader_service"} 1.0
newrelic:apdex_score{app="risk-value-be-prod"} 1.0
# HELP newrelic:response_time response_time
# TYPE newrelic:response_time gauge
newrelic:response_time{app="sso-service"} 4.4
newrelic:response_time{app="file_uploader_service"} 8.26
newrelic:response_time{app="risk-value-be-prod"} 9.13
# HELP newrelic:throughput throughput
# TYPE newrelic:throughput gauge
newrelic:throughput{app="sso-service"} 12.7
newrelic:throughput{app="file_uploader_service"} 20.7
newrelic:throughput{app="risk-value-be-prod"} 13.7
# HELP newrelic:error_rate error_rate
# TYPE newrelic:error_rate gauge
newrelic:error_rate{app="sso-service"} 0.0
newrelic:error_rate{app="file_uploader_service"} 0.0
newrelic:error_rate{app="risk-value-be-prod"} 0.0
# HELP newrelic:synthetic:sla:latency_ms latency_ms
# TYPE newrelic:synthetic:sla:latency_ms gauge
newrelic:synthetic:sla:latency_ms{app="login_form",periodays="1"} 2903.76
newrelic:synthetic:sla:latency_ms{app="login_form",periodays="7"} 2883.28
newrelic:synthetic:sla:latency_ms{app="login_form",periodays="30"} 2886.77
newrelic:synthetic:sla:latency_ms{app="report_page",periodays="1"} 769.2
newrelic:synthetic:sla:latency_ms{app="report_page",periodays="7"} 766.04
newrelic:synthetic:sla:latency_ms{app="report_page",periodays="30"} 796.14
# HELP newrelic:synthetic:sla:sla_apdex sla_apdex
# TYPE newrelic:synthetic:sla:sla_apdex gauge
newrelic:synthetic:sla:sla_apdex{app="login_form",periodays="1"} 1.0
newrelic:synthetic:sla:sla_apdex{app="login_form",periodays="7"} 1.0
newrelic:synthetic:sla:sla_apdex{app="login_form",periodays="30"} 1.0
newrelic:synthetic:sla:sla_apdex{app="report_page",periodays="1"} 1.0
newrelic:synthetic:sla:sla_apdex{app="report_page",periodays="7"} 1.0
newrelic:synthetic:sla:sla_apdex{app="report_page",periodays="30"} 1.0
# HELP newrelic:synthetic:sla:success_rate success_rate
# TYPE newrelic:synthetic:sla:success_rate gauge
newrelic:synthetic:sla:success_rate{app="login_form",periodays="1"} 100.0
newrelic:synthetic:sla:success_rate{app="login_form",periodays="7"} 100.0
newrelic:synthetic:sla:success_rate{app="login_form",periodays="30"} 99.97
newrelic:synthetic:sla:success_rate{app="report_page",periodays="1"} 100.0
newrelic:synthetic:sla:success_rate{app="report_page",periodays="7"} 99.99
newrelic:synthetic:sla:success_rate{app="report_page",periodays="30"} 100.0
```
