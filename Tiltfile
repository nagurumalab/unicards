docker_compose("./docker-compose.yaml")
docker_build("unicards-server", ".", live_update=[
    sync(".", "/app")
])