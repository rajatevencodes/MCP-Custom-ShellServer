```json
 "shell": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/rajatsharma/Desktop/Custom-ShellServer-MCP",
        "run",
        "src/server.py"
      ]
    }
```

DevOps

Build Custom Image and then container

```bash
docker build -t mcp-img .
docker run -it --rm mcp-img
```

--rm - automatically deletes the container after exit

on MCP-client : Claude
Following this docs : https://www.docker.com/blog/the-model-context-protocol-simplifying-building-ai-apps-with-anthropic-claude-desktop-and-docker/

```json
	 "docker-shell": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--init",
        "-e",
        "DOCKER_CONTAINER=true",
        "mcp-img"
      ]
    }
```
