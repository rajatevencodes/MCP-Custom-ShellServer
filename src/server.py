# -----------------------------
# MCP TERMINAL SERVER (EASY IMPLEMENTATION)
# -----------------------------
# subprocess is a standard Python module that lets us start new programs and
# interact with them (send input, read output). Think of it as opening a new
# terminal tab from inside your Python code to run a command like `ls` or
# `echo hello` and capture whatever text the command prints.

from mcp.server.fastmcp import FastMCP
import subprocess

# Create the MCP server instance. "terminal_server" is just a short name that
# will show up in client UIs.
mcp = FastMCP("terminal_server")


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


if __name__ == "__main__":
    # When you run `python src/server.py`, this starts the MCP server so tools
    # become available to connected clients.
    mcp.run("stdio")

"""
Check Whether the code is working or not
Command : python -c "from src.server import play_with_terminal; print(play_with_terminal('echo hello'))"
Output : hello

! Make sure to run the command in the same directory as the server.py file.
"""
