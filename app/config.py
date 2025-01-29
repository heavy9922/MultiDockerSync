import os
import json
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde .env si existe

docker_endpoints_env = os.getenv("DOCKER_ENDPOINTS")

if not docker_endpoints_env:
    raise ValueError("ERROR: La variable de entorno 'DOCKER_ENDPOINTS' no está definida.")

try:
    docker_endpoints = json.loads(docker_endpoints_env)
    if not isinstance(docker_endpoints, list) or not all(isinstance(item, dict) and "host" in item and "port" in item for item in docker_endpoints):
        raise ValueError("ERROR: 'DOCKER_ENDPOINTS' debe ser una lista de diccionarios con 'host' y 'port'.")
except json.JSONDecodeError:
    raise ValueError("ERROR: 'DOCKER_ENDPOINTS' no tiene un formato JSON válido.")