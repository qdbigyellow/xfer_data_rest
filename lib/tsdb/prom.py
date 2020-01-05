from config import Configurations
from prometheus_client import CollectorRegistry, Gauge, pushadd_to_gateway, push_to_gateway
from typing import Optional, Any, Dict
import os

def push_data_to_gateway(job_name: str, gauge_name: str, gauge_detail: str, data: Any,
                         labels: Dict[str, str] = None, grouping_key: Dict[str, str] = None, pushadd: bool = False):
    """
    :param job_name: name of the job.
    :param gauge_name: the matric name.
    :param gauge_detail: The help text of the matric.
    :param data: data to be pushed to the gateway.
    :param labels: a dictionary of label name and value.
    :param grouping_key: a dictionary for grouping.
    :param pushadd: a flag, if True,  use pushadd mode. 
    """
    registry = CollectorRegistry()
    label_names = [k for k, v in labels.items()] if labels else ()
    g = Gauge(gauge_name, gauge_detail, label_names, registry=registry)
    if labels is not None:
        g.labels(**labels).set(data)
    else:
        g.set(data)

    ip = Configurations.DEV_DB.IP if os.getenv('DEVENV', '0') == '1' else Configurations.DB.IP
    port = Configurations.DEV_DB.PUSH_GATEWAY if os.getenv('DEVENV', '0') == '1' else Configurations.DB.PUSH_GATEWAY

    # gauge_name{job=jobname, <lable_1_key>=<label_1_value>, ..., <label_n_key>}
    # https://github.com/prometheus/client_python
    # push_to_gateway replaces metrics with the same grouping key -> meaning if the grouping key is same, even matrix name is different, the latter matrix will overwrite the former matrix
    # pushadd_to_gateway only replaces metrics with the same name and grouping key 
    if grouping_key is None or pushadd:
        pushadd_to_gateway(ip +':'+ port, job=job_name, grouping_key=grouping_key, registry=registry)
    else:
        push_to_gateway(ip +':'+ port, job=job_name, grouping_key=grouping_key, registry=registry)

    