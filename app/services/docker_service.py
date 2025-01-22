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
            ports = container.attrs.get("NetworkSettings", {}).get("Ports", {})
            exposed_port = "80"
            if ports:
                for port_bindings in ports.values():
                    if port_bindings:
                        exposed_port = port_bindings[0]["HostPort"]
                        break

            result.append({
                "id": container.id,
                "name": container.name,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "status": container.status,
                "host": host,
                "port": exposed_port,
            })
        return result
    except Exception as e:
        print(f"Error fetching containers from {host}: {e}")
        return []
