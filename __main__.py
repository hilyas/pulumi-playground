import os
import pulumi
from pulumi_gcp import storage, compute, container


def get_project_id():
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    if not project_id:
        raise pulumi.RunError("GOOGLE_PROJECT_ID environment variable not set")
    return project_id


def create_bucket(name, location):
    bucket_resource = storage.Bucket(name, location=location)
    pulumi.export(f"bucket_url_{name}", bucket_resource.url)
    return bucket_resource


def create_instance(name, zone, machine_type, boot_disk_image, network):
    boot_disk = compute.InstanceBootDiskArgs(
        initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
            image=boot_disk_image
        )
    )
    network_interfaces = [compute.InstanceNetworkInterfaceArgs(network=network)]
    instance = compute.Instance(
        name,
        zone=zone,
        machine_type=machine_type,
        boot_disk=boot_disk,
        network_interfaces=network_interfaces,
    )
    pulumi.export(f"instance_name_{name}", instance.name)
    return instance


def create_cluster(name, location, remove_default_node_pool, initial_node_count):
    cluster = container.Cluster(
        name,
        location=location,
        remove_default_node_pool=remove_default_node_pool,
        initial_node_count=initial_node_count,
    )
    return cluster


def create_node_pool(cluster_name, location, cluster, node_count, node_config):
    node_pool = container.NodePool(
        cluster_name + "preemptible",
        location=location,
        cluster=cluster.name,
        node_count=node_count,
        node_config=container.NodePoolNodeConfigArgs(
            preemptible=node_config["preemptible"],
            machine_type=node_config["machine_type"],
            disk_size_gb=node_config["disk_size_gb"],
            service_account=node_config["service_account"],
            oauth_scopes=["https://www.googleapis.com/auth/cloud-platform"],
        ),
    )
    return node_pool


def main():
    # Get the configuration values
    config = pulumi.Config()
    buckets = config.require_object("buckets")
    instances = config.require_object("instances")
    clusters = config.require_object("clusters")

    # Create and export the buckets
    for bucket in buckets:
        create_bucket(bucket["name"], bucket["location"])

    # Create and export the instances
    for instance_config in instances:
        create_instance(
            instance_config["name"],
            instance_config["zone"],
            instance_config["machine_type"],
            instance_config["boot_disk"]["initialize_params"]["image"],
            instance_config["network_interfaces"][0]["network"],
        )

    # Create and export the clusters and their node pools
    for cluster_config in clusters:
        cluster = create_cluster(
            cluster_config["name"],
            cluster_config["location"],
            cluster_config["remove_default_node_pool"],
            cluster_config["initial_node_count"],
        )
        for node_pool in cluster_config["node_pools"]:
            create_node_pool(
                cluster_config["name"],
                cluster_config["location"],
                cluster,
                cluster_config["initial_node_count"],
                node_pool,
            )


if __name__ == "__main__":
    main()
