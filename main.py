import asyncio
from dotenv import load_dotenv
from agent.graph import create_web_agent_graph

load_dotenv()

async def main():
    graph = create_web_agent_graph()
    
    # Example goal - change this to whatever you want
    user_goal = "Go to https://github.com and tell me the top 3 trending repositories right now."
    
    result = await graph.ainvoke({
        "messages": [("user", user_goal)],
        "url": None
    })
    
    print("\n=== Final Result ===")
    print(result.get("messages", [])[-1])

if __name__ == "__main__":
    asyncio.run(main())