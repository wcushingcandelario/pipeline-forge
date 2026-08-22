$ErrorActionPreference='Stop'
py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\pip.exe install -r requirements.txt
Write-Host 'PipelineForge setup complete. Run: .\.venv\Scripts\python.exe pipelineforge.py demo' -ForegroundColor Green
