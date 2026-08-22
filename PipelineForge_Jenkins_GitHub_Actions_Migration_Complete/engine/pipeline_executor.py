from services.jenkins_service import discover_pipelines
from services.analysis_service import analyze_pipelines
from services.scoring_service import score_pipelines
from services.reporting_service import generate_reports


class PipelineExecutor:
    def __init__(self):
        self.name = "PipelineForge Executor"

    def execute(self):
        print("PipelineForge Executor Started")

        print("Starting Jenkins discovery...")
        pipelines = discover_pipelines()

        print("Running pipeline analysis...")
        analysis_results = analyze_pipelines(pipelines)

        print("Calculating migration scores...")
        scores = score_pipelines(analysis_results)

        print("Generating reports...")
        generate_reports(scores)

        print("PipelineForge Executor Completed")

        return scores


def execute_pipeline():
    executor = PipelineExecutor()
    return executor.execute()
