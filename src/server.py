# -----------------------------
# MCP TERMINAL SERVER (EASY IMPLEMENTATION)
# -----------------------------
# subprocess is a standard Python module that lets us start new programs and
# interact with them (send input, read output). Think of it as opening a new
# terminal tab from inside your Python code to run a command like `ls` or
# `echo hello` and capture whatever text the command prints.

from mcp.server.fastmcp import FastMCP
import subprocess
from pathlib import Path

# Create the MCP server instance. "terminal_server" is just a short name that
# will show up in client UIs.
mcp = FastMCP("terminal_server")

# Absolute path to the 'resources' directory in server
RESOURCE_DIR = Path(__file__).resolve().parent.parent / "resources"

# Gist URL to download with rajat_random_downloadcode
GIST_URL = "https://gist.githubusercontent.com/rajatevencodes/22757b5402a992b201beb3e1b8de0ab9/raw"


# The @mcp.tool() decorator tells the MCP SDK that this function should be
# exposed to clients as a callable "tool" named play_with_terminal.
@mcp.tool()
def play_with_terminal(command: str) -> str:
    """Run a shell command and return its output or error text.

    Parameters
    ----------
    command : str
        Anything you could normally type in your own terminal (e.g. "ls -la").

    Returns
    -------
    str
        The text printed by the command (stdout) or, if the command fails,
        the error text (stderr).
    """

    try:
        # subprocess.run executes the given command in a new shell process.
        completed = subprocess.run(
            command,
            shell=True,  # run inside the shell so bash-style commands work
            check=True,  # raise an error if the command exits with code ≠ 0
            capture_output=True,  # capture_output=True tells it to save whatever the command prints so we can use it later instead of letting it stream directly to our terminal.
            text=True,  # text=True makes sure we get Python strings instead of raw bytes.
        )
        # .stdout contains everything the command printed successfully
        return completed.stdout.strip()
    except subprocess.CalledProcessError as error:
        # If the command fails (non-zero exit status), we reach this block.
        # We return the error text so the user can see what went wrong.
        return str(error)


# ------------------ RESOURCE EXPOSURE ------------------
# Any MCP client can fetch a URI like:
#   resource://MCP-PlsReadMe.md
# and the contents of resources/MCP-PlsReadMe.md will be streamed back.
# `{filename}` is a URI parameter that the MCP runtime will pass into our
# function. We simply read that file from disk and return its bytes.
@mcp.resource("resource://{filename}", name="Project files")
def get_project_resource(filename: str) -> bytes:
    """Serve files from the local 'resources' directory.

    Parameters
    ----------
    filename : str
        The exact file name requested by the client. No directory traversal is
        allowed; we resolve the path relative to RESOURCE_DIR and verify that
        the final path still lives inside that directory.
    """
    # Build the absolute path safely to avoid `../../` tricks.
    requested_path = (RESOURCE_DIR / filename).resolve()

    # Security check: ensure requested_path is within RESOURCE_DIR
    if not str(requested_path).startswith(str(RESOURCE_DIR)):
        raise FileNotFoundError("Invalid resource path")

    if not requested_path.is_file():
        raise FileNotFoundError(f"Resource '{filename}' not found")

    return requested_path.read_bytes()


# ------------------ DOWNLOAD TOOL ------------------
@mcp.tool()
def rajat_random_downloadcode() -> str:
    """Download the gist content via `curl` and return it as text.

    Uses the system's `curl` command so beginners can see how a shell download
    works. We pass `-sL` to make the output quiet (`-s`) and to follow any
    redirects (`-L`).
    """
    try:
        GIST_URL = "https://gist.githubusercontent.com/rajatevencodes/22757b5402a992b201beb3e1b8de0ab9/raw"
        completed = subprocess.run(
            ["curl", "-sL", GIST_URL],
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout
    except subprocess.CalledProcessError as error:
        return f"curl failed: {error.stderr or error}"


if __name__ == "__main__":
    # When you run `python src/server.py`, this starts the MCP server so tools
    # become available to connected clients.
    mcp.run("stdio")

"""
Note : Make sure to run the server and restart the claude client to see the changes.
"""


"""
Resource : get_project_resource
* We can see the changes only via Pro Plan of Claude. :/
    Check Whether the code is working or not
    Command : python -c "from src.server import get_project_resource; print(get_project_resource('MCP-PlsReadMe.md'))"
    Output : ! content of the file !
"""

"""
Tool : play_with_terminal
    Check Whether the code is working or not
    Command : python -c "from src.server import play_with_terminal; print(play_with_terminal('echo hello'))"
    Output : hello

! Make sure to run the command in the same directory as the server.py file.
* This is a very powerful tool This might delete anything from our system. So be careful.
"""

"""
Tool: - rajat_random_downloadcode

    Command : python -c "from src.server import rajat_random_downloadcode; print(rajat_random_downloadcode())"
    Output : ! content of the file ! - 
! This could be a malicous code too. so be alert.
* MCP Servers should be handled with care.
"""
