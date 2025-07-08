from kubernetes import client, config

def get_pod_resource_usage(namespace="default"):
    """
    Lists the CPU and memory usage of all pods in a given namespace.
    Requires the Metrics Server to be running in the Kubernetes cluster.
    """
    try:
        # Load Kubernetes configuration
        config.load_kube_config()
        v1 = client.CoreV1Api()
        metrics_client = client.CustomObjectsApi()

        # List all pods in the specified namespace
        pods = v1.list_namespaced_pod(namespace=namespace)

        print(f"Resource Usage for Pods in Namespace: {namespace}\n")
        print(f"{'POD NAME':<40} {'CPU (cores)':<15} {'MEMORY (MiB)':<15}")
        print("-" * 70)

        for pod in pods.items:
            pod_name = pod.metadata.name
            try:
                # Get metrics for the pod
                pod_metrics = metrics_client.get_namespaced_custom_object(
                    group="metrics.k8s.io",
                    version="v1beta1",
                    namespace=namespace,
                    plural="pods",
                    name=pod_name,
                )

                if pod_metrics and pod_metrics.get('containers'):
                    cpu_usage = 0
                    memory_usage = 0
                    for container in pod_metrics['containers']:
                        cpu = container['usage'].get('cpu')
                        memory = container['usage'].get('memory')

                        if cpu and cpu.endswith('n'):
                            cpu_nanocores = int(cpu[:-1])
                            cpu_cores = cpu_nanocores / 1_000_000_000
                            cpu_usage += cpu_cores
                        elif cpu and cpu.endswith('m'):
                            cpu_millicores = int(cpu[:-1])
                            cpu_cores = cpu_millicores / 1000
                            cpu_usage += cpu_cores

                        if memory and memory.endswith('Ki'):
                            memory_kibibytes = int(memory[:-2])
                            memory_mibibytes = memory_kibibytes / 1024
                            memory_usage += memory_mibibytes
                        elif memory and memory.endswith('Mi'):
                            memory_mibibytes = int(memory[:-2])
                            memory_usage += memory_mibibytes
                        elif memory and memory.endswith('Gi'):
                            memory_gibibytes = int(memory[:-2])
                            memory_mibibytes = memory_gibibytes * 1024
                            memory_usage += memory_mibibytes

                    print(f"{pod_name:<40} {cpu_usage:<15.3f} {memory_usage:<15.1f}")
                else:
                    print(f"{pod_name:<40} Metrics not available for this pod.")

            except client.ApiException as e:
                print(f"Error getting metrics for pod {pod_name}: {e}")

    except config.ConfigException as e:
        print(f"Could not load Kubernetes configuration: {e}")
    except client.ApiException as e:
        print(f"Kubernetes API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    namespace_to_monitor = "develop-runner"  # Replace with the desired namespace
    get_pod_resource_usage(namespace=namespace_to_monitor)