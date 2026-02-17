from tensorlake.applications import application, run_local_application, Request, function
from adk_ooo.agent import AGENT_IMAGE, run_tour_guide_agent


@application()
@function(image=AGENT_IMAGE, min_containers=1)
def main(query: str) -> str:
    """Entry point that dispatches to the tour guide agent."""
    return run_tour_guide_agent(query=query)


if __name__ == '__main__':
    request: Request = run_local_application(
        main, query="What are some interesting historical sites in my location?"
    )
    print(request.output())
