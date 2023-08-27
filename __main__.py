import os
import pulumi
from pulumi_gcp import storage, compute, container


def get_project_id():
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    if not project_id:
        raise pulumi.RunError("GOOGLE_PROJECT_ID environment variable not set")
    return project_id


def create_buckets(buckets):
    for i, bucket in enumerate(buckets):
        bucket_resource = storage.Bucket(bucket["name"], location=bucket["location"])
        pulumi.export(f"bucket_name_{i}", bucket_resource.url)


def create_instances(instances):
    for i, instance_config in enumerate(instances):
        boot_disk = compute.InstanceBootDiskArgs(
            initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
                image=instance_config["boot_disk"]["initialize_params"]["image"]
            )
        )
        network_interfaces = [
            compute.InstanceNetworkInterfaceArgs(network=nic["network"])
            for nic in instance_config["network_interfaces"]
        ]
        instance = compute.Instance(
            instance_config["name"],
            zone=instance_config["zone"],
            machine_type=instance_config["machine_type"],
            boot_disk=boot_disk,
            network_interfaces=network_interfaces,
        )
        pulumi.export(f"instance_name_{i}", instance.name)


def create_clusters(clusters):
    for cluster_config in clusters:
        primary = container.Cluster(
            cluster_config["name"],
            location=cluster_config["location"],
            remove_default_node_pool=cluster_config["remove_default_node_pool"],
            initial_node_count=cluster_config["initial_node_count"],
        )

        primary_preemptible_nodes = [
            container.NodePool(
                cluster_config["name"] + "preemptible",
                location=cluster_config["location"],
                cluster=primary.name,
                node_count=cluster_config["initial_node_count"],
                node_config=container.NodePoolNodeConfigArgs(
                    preemptible=node_pool["preemptible"],
                    machine_type=node_pool["machine_type"],
                    disk_size_gb=node_pool["disk_size_gb"],
                    service_account=node_pool["service_account"],
                    oauth_scopes=["https://www.googleapis.com/auth/cloud-platform"],
                ),
            )
            for node_pool in cluster_config["node_pools"]
        ]


project_id = get_project_id()


def main():
    # Get the configuration values
    config = pulumi.Config()
    buckets = config.require_object("buckets")
    instances = config.require_object("instances")
    clusters = config.require_object("clusters")

    # Create and export the buckets
    create_buckets(buckets)

    # Create and export the instances
    create_instances(instances)

    # Create and export the cluster
    create_clusters(clusters)


if __name__ == "__main__":
    main()
