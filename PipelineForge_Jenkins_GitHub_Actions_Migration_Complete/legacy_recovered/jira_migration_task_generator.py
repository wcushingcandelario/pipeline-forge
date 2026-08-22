import json
from pathlib import Path
from collections import defaultdict


INPUT_FILE = Path("../module4_output/github_actions_migration_plan.json")
OUTPUT_FILE = Path("../module4_output/jira_migration_tasks.json")


def create_issue_structure(item):
    """
    Creates Jira-ready Epic/Story/Task structure
    for Jenkins to GitHub Actions migration.
    """

    job = item.get("jenkins_job", "Unknown Jenkins Job")

    epic = {
        "issue_type": "Epic",
        "summary": f"Migrate Jenkins Pipeline: {job}",
        "description": (
            f"Migration of Jenkins pipeline '{job}' "
            "to GitHub Actions."
        ),
        "priority": determine_priority(item)
    }

    stories = []

    tasks = item.get("tasks", [])

    for task in tasks:
        stories.append({
            "issue_type": "Story",
            "summary": task,
            "parent_epic": epic["summary"],
            "description": (
                f"Complete migration activity for Jenkins job '{job}'."
            )
        })

    return {
        "epic": epic,
        "stories": stories,
        "migration_metadata": {
            "jenkins_job": job,
            "classification": item.get("migration_classification"),
            "score": item.get("migration_score"),
            "strategy": item.get("strategy"),
            "risks": item.get("risks", [])
        }
    }


def determine_priority(item):

    classification = item.get("migration_classification")

    if classification == "COMPLEX":
        return "High"

    if classification == "MEDIUM":
        return "Medium"

    return "Low"


def build_jira_tasks(plans):

    results = []

    for plan in plans:
        results.append(create_issue_structure(plan))

    return results


def main():

    with open(INPUT_FILE) as f:
        plans = json.load(f)

    jira_tasks = build_jira_tasks(plans)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(jira_tasks, f, indent=2)

    print("Jira migration task generation complete")
    print(f"Jira migration packages created: {len(jira_tasks)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
