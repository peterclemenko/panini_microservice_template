from panini import app as panini_app
from panini.middleware.prometheus_monitoring import PrometheusMonitoringMiddleware
from app.config_manager import get_panini_config


panini_config = get_panini_config()


app = panini_app.App(
    service_name="template_app",
    servers=panini_config.nats_servers,
    client_nats_name=panini_config.nats_client_name,
    auth=panini_config.auth,
)


log = app.logger

message = {
    "key1": "value1",
    "key2": [1, 2, 3, 4],
}


@app.task(interval=2)
async def request_periodically():
    for _ in range(10):
        response = await app.request(subject="some.request.subject", message=message)
        log.info(f"get response from periodic request {response}")


@app.listen("some.request.subject")
async def receive_messages(msg):
    log.info(f"{msg.subject}:{msg.data}")
    return {"success": True, "data": msg.data}


if __name__ == "__main__":
    if 'PROMETHEUS_PUSHGATEWAY_URL' in panini_config.infrastructure:
        app.add_middleware(
            PrometheusMonitoringMiddleware,
            pushgateway_url=panini_config.infrastructure.get(
                'PROMETHEUS_PUSHGATEWAY_URL'),
        )
    app.start()
