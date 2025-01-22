from fastapi import APIRouter
from app.config import docker_endpoints
from app.services.docker_service import connect_to_docker, get_containers_from_endpoint

router = APIRouter()

@router.get("/containers")
async def list_containers():
    """
    Devuelve la configuración esperada por Traefik.
    """
    services = {}
    for endpoint in docker_endpoints:
        client = connect_to_docker(endpoint)
        if client:
            containers = get_containers_from_endpoint(client, endpoint["host"])
            for container in containers:
                service_name = container["name"]
                host = container["host"]
                port = container["port"]

                # Formato que Traefik espera
                services[service_name] = {
                    "loadBalancer": {
                        "servers": [
                            {"url": f"http://{host}:{port}"}
                        ]
                    }
                }

    return {"http": {"services": services}}
