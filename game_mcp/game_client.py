import asyncio


# Feel free to import any libraries you need - if needed change requirements.txt


class BombClient:
    def __init__(self):
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE

    async def connect_to_server(self, server_url: str):
        """Connect to an sse MCP server"""
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE

    async def process_query(self, tool_name: str, tool_args: dict[str, str]) -> str:
        """Process a query using the game_interaction tool"""
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE

    async def cleanup(self):
        """Properly clean up the session and streams"""
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE


class Defuser(BombClient):
    async def run(self, action: str) -> str:
        """Run a defuser action"""
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE


class Expert(BombClient):
    async def run(self) -> str:
        """Run an expert action"""
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE


async def main():
    """ Main function to connect to the server and run the clients """
    # YOUR CODE STARTS HERE
    pass
    # YOUR CODE ENDS HERE


async def expert_test(expert_client: Expert):
    """Test the Expert class"""
    result = await expert_client.run()

    possible_outputs = ["BOOM!", "BOMB SUCCESSFULLY DISARMED!", "Regular Wires Module", "The Button Module",
                        "Memory Module", "Simon Says Module"]

    assert any(output.find(result) != -1 for output in possible_outputs), f"Expert test failed"


async def defuser_test(defuser_client: Defuser):
    """Test the Defuser class"""
    result = await defuser_client.run("state")

    possible_outputs = ["BOMB STATE"]

    assert any(output.find(result) != -1 for output in possible_outputs), f"Defuser test failed"

if __name__ == "__main__":
    asyncio.run(main())
