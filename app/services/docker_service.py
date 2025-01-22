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
            labels = container.attrs.get("Config", {}).get("Labels", {})
            # print(f"DEBUG: Contenedor {container.name} etiquetas: {labels}")  # Depuración
            result.append({
                "id": container.id,
                "name": container.name,
                "labels": labels,
                "host": host,
            })
        return result
    except Exception as e:
        print(f"Error fetching containers from {host}: {e}")
        return []

