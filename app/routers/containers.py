from fastapi import APIRouter
from app.models.container import ContainerInfo
from app.config import docker_endpoints
from app.services.docker_service import connect_to_docker, get_containers_from_endpoint

router = APIRouter()

@router.get("/containers", response_model=list[ContainerInfo])
async def list_containers():
    all_containers = []
    for endpoint in docker_endpoints:
        client = connect_to_docker(endpoint)
        if client:
            containers = get_containers_from_endpoint(client, endpoint["host"])
            all_containers.extend(containers)
    return all_containers
