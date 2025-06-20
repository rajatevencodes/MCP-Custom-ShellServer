## Configuration

### Local Development

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

## DevOps

### Docker Deployment

Build a custom Docker image for secure containerized execution:

```bash
# Build the Docker image
docker build -t mcp-img .

# Run the container interactively
docker run -it --rm mcp-img
```

> **Note**: The `--rm` flag automatically deletes the container after exit.

### MCP Client Configuration (Claude)

For integration with Claude Desktop, refer to the [official Docker documentation](https://www.docker.com/blog/the-model-context-protocol-simplifying-building-ai-apps-with-anthropic-claude-desktop-and-docker/).

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
