from services.jenkins_service import discover_pipelines
from services.analysis_service import analyze_pipelines
from services.scoring_service import score_pipelines
from services.reporting_service import generate_reports


def execute_pipeline():
    print("Starting Jenkins discovery...")
    pipelines = discover_pipelines()

    print("Running pipeline analysis...")
    analysis_results = analyze_pipelines(pipelines)

    print("Calculating migration scores...")
    scores = score_pipelines(analysis_results)

    print("Generating reports...")
    generate_reports(scores)

    print("PipelineForge workflow execution complete")

    return scores
