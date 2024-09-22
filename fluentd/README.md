# Fluentd DaemonSet in Kubernetes

## Overview

Fluentd is an open-source data collector designed for processing logs and events. It's highly flexible, allowing you to collect data from multiple sources, transform it as needed, and send it to various destinations. 

In Kubernetes, Fluentd is typically run as a `DaemonSet`, ensuring that an instance of Fluentd runs on every node. This enables efficient log collection from both the nodes and the pods running on them.

## Why Fluentd on Kubernetes?

Kubernetes is a powerful container orchestration platform that automates the deployment, scaling, and management of containerized applications. By deploying Fluentd in Kubernetes, we can utilize Kubernetes' scalability and management capabilities to streamline log collection and forwarding for all nodes and containers.

## Fluentd Configuration Example

The following Fluentd configuration collects logs from Fluentd agents running on Kubernetes nodes and forwards them to Elasticsearch.

### Fluentd Configuration (`fluentd-config.conf`)

```conf
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<match **>
  @type elasticsearch
  host elasticsearch.default.svc.cluster.local
  port 9200
  logstash_format true
</match>




Next, let's create the fluentd configuration file named fluent.conf that ships logs created by the app container.

You can find these logs under the /var/log/containers/ directory.

Place this file in the following path: /root/fluentd/etc/fluent.conf

Create the required directories in the above path, if not present. This specific path will ensure that our custom configuration gets mounted to the pod.

Use the standard Fluentd source, parse, filter, and match directives to collect logs from all containers and forward them to Elasticsearch at elasticsearch.elastic-stack.svc.cluster.local on port 9200.

You can also include other file paths in this config file.



Refer to the official Fluentd documentation on how to create this file:
https://docs.fluentd.org/configuration/config-file




Finally, let's create a fluentd DaemonSet to collect and forward logs to Elasticsearch.

Create a file named fluentd.yaml in the /root/fluentd directory with the configuration for a DaemonSet named fluentd in the elastic-stack namespace.


Use ServiceAccount fluentd in the configuration.

For the fluentd container, use the following image:
fluent/fluentd-kubernetes-daemonset:v1.14.1-debian-elasticsearch7-1.0

Use appropriate environment variables for the elasticsearch address and port above.
Also, add a variable FLUENT_ELASTICSEARCH_LOGSTASH_PREFIX with the value fluentd.

Mount the /var/log and /var/lib/docker/containers directories from the host to the pods, with the /var/lib/docker/containers directory mounted as read-only.

Also, mount the config file located under the fluentd/etc folder to the pod.


----
To retrieve all logs, you can use the size parameter to increase the number of documents returned or use the scroll API for large result sets:
curl localhost:30200/_search?q=*:*&size=10000&pretty






