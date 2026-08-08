from engine.workspace_manager import create_workspace
from engine.engine_runner import run_engine
from engine.pipeline_executor import execute_pipeline

def run():
    print("PipelineForge Assessment Started")

    print("Creating workspace...")
    workspace = create_workspace()
    print(f"Workspace created: {workspace}")

    print("Starting engine...")
    run_engine()

    print("Executing pipeline...")
    execute_pipeline()

    print("PipelineForge Assessment Complete")


if __name__ == "__main__":
    run()
