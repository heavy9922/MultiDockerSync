from fastapi import APIRouter
from app.config import docker_endpoints
from app.services.docker_service import connect_to_docker, get_containers_from_endpoint

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
    
    # print(f"DEBUG: Contenedores obtenidos: {containers}")

    for container in containers:
        labels = container.get("labels", {})
        if labels.get("traefik.enable") == "true":
            rule = labels.get(f"traefik.http.routers.{container['name']}.rule")
            port = labels.get(f"traefik.http.services.{container['name']}.loadbalancer.server.port")
            host = container["host"]

            # print(f"DEBUG: Procesando contenedor {container['name']} con etiquetas: {labels}")

            if rule and port:
                routers[container["name"]] = {
                    "rule": rule,
                    "entryPoints": ["web"],
                    "service": container["name"]
                }
                services[container["name"]] = {
                    "loadBalancer": {
                        "servers": [
                            {"url": f"http://{host}:{port}"}
                        ]
                    }
                }

    # print(f"DEBUG: Routers generados: {routers}")
    # print(f"DEBUG: Services generados: {services}")

    return {"http": {"routers": routers, "services": services}}