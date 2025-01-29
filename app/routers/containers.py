import json
from fastapi import APIRouter
from app.config import docker_endpoints
from app.services.docker_service import connect_to_docker, get_containers_from_endpoint
from app.utils.docker_client import clean_container_name

router = APIRouter()

@router.get("/containers")
async def list_containers():
    routers = {}
    services = {}
    containers = []
    
    for endpoint in docker_endpoints:
        client = connect_to_docker(endpoint)
        if client:
            containers.extend(get_containers_from_endpoint(client, endpoint["host"]))

    for container in containers:
        original_name = container["name"]
        cleaned_name = clean_container_name(original_name)

        labels = container.get("labels", {})
        traefik_labels = {key: value for key, value in labels.items() if key.startswith("traefik.")}

        # Depuración
        # print(f"DEBUG: {original_name} -> {cleaned_name}")
        # print(json.dumps(traefik_labels, indent=4))

        if traefik_labels.get("traefik.enable") == "true":
            rule = traefik_labels.get(f"traefik.http.routers.{cleaned_name}.rule")
            port = traefik_labels.get(f"traefik.http.services.{cleaned_name}.loadbalancer.server.port")
            host = container["host"]

            if rule and port:
                routers[cleaned_name] = {
                    "rule": rule,
                    "entryPoints": ["web"],
                    "service": cleaned_name
                }
                services[cleaned_name] = {
                    "loadBalancer": {
                        "servers": [
                            {"url": f"http://{host}:{port}"}
                        ]
                    }
                }

    return {"http": {"routers": routers, "services": services}}