from config import Configurations
from prometheus_client import CollectorRegistry, Gauge, pushadd_to_gateway, push_to_gateway
from typing import Optional, Any, Dict

def push_data_to_gateway(job_name: str, gauge_name: str, gauge_detail: str, data: Any,
                         labels: Dict[str, str] = None, grouping_key: Dict[str, str] = None):
        """
    :param job_name: name of the job.
    :param gauge_name: the matric name.
    :param gauge_detail: The help text of the matric.
    :param data: data to be pushed to the gateway.
    :param labels: a dictionary of label name and value.
    :param grouping_key: a dictionary for grouping.
    """
    registry = CollectorRegistry()
    label_names = [k for k, v in labels.items()] if labels else ()
    g = Gauge(gauge_name, gauge_detail, label_names, registry=registry)
    if labels is not None:
        g.labels(**labels).set(data)
    else:
        g.set(data)
    push_to_gateway(Configurations.DB.IP +':'+ Configurations.DB.PUSH_GATEWAY, job=job_name, grouping_key=grouping_key, registry=registry)

