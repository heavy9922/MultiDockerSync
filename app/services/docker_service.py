import docker
# import json
def connect_to_docker(endpoint):
    try:
        client = docker.DockerClient(base_url=f"tcp://{endpoint['host']}:{endpoint['port']}")
        return client
    except Exception as e:
        print(f"Error connecting to Docker on {endpoint['host']}: {e}")
        return None

def get_containers_from_endpoint(client, host):
    try:
        containers = client.containers.list(all=True)
        # for container in containers:
        #     container_data = container.attrs
        #     print(json.dumps(container_data, indent=4))
        return [
            {
                "id": container.id,
                "name": container.name,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "status": container.status,
                "host": host,
            }
            for container in containers
        ]
    except Exception as e:
        print(f"Error fetching containers from {host}: {e}")
        return []
