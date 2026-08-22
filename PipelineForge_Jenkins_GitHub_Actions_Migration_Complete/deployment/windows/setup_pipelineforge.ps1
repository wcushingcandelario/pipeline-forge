Write-Host 'PipelineForge Windows Setup'
python -m venv pipelineforge-env
.\pipelineforge-env\Scripts\Activate.ps1
pip install -r requirements.txt
Write-Host 'Complete'
