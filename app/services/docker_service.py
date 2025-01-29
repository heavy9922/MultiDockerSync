import json
import docker

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
        result = []
        for container in containers:
            # print("RAW CONTAINER DICT:", json.dumps(container.__dict__, indent=4, default=str))
            container_info = {
                "id": container.id,
                "name": container.name,
                "image": container.image.tags[0] if container.image.tags else "N/A",
                "status": container.status,
                "created": container.attrs.get("Created"),
                "labels": container.attrs.get("Config", {}).get("Labels", {}),
                "host": host
            }
            # print(json.dumps(container_info, indent=4))  

            result.append(container_info)
        return result
    except Exception as e:
        print(f"Error fetching containers from {host}: {e}")
        return []
