# Work Command Center - OneNote Windows Desktop Builder
# Requires classic OneNote desktop / Microsoft 365 OneNote with COM automation.
$ErrorActionPreference = 'Stop'

try { $one = New-Object -ComObject OneNote.Application } catch {
  Write-Host 'OneNote desktop COM automation was not found. Install/open Microsoft 365 OneNote desktop and run again.' -ForegroundColor Red
  Read-Host 'Press Enter to exit'; exit 1
}

$root = Join-Path $env:USERPROFILE 'Documents\Work Command Center'
New-Item -ItemType Directory -Path $root -Force | Out-Null

# OneNote OpenHierarchy CreateFileType: 1 = section, 3 = notebook (supported by desktop object model)
$notebookId = ''
$one.OpenHierarchy($root, '', [ref]$notebookId, 3)

$sections = [ordered]@{
 '00 - Inbox' = @(
  @{Title='INBOX - Quick Capture'; Body=@('Capture first. Process later.','','☐ Task / idea / request:','☐ Who / what is involved:','☐ Due or follow-up date:','☐ Move to the correct project, meeting, person, decision, or reference page during processing.')}
 )
 '01 - Daily Notes' = @(
  @{Title='TEMPLATE - Daily Work Note'; Body=@('TOP 3','1.','2.','3.','','TODAY''S CALENDAR / PREP','• Meeting / event:','• Preparation needed:','','TASKS / PRIORITIES','☐','☐','☐','','WAITING / FOLLOW-UP','•','','NOTES / CAPTURE','•','•','','DECISIONS MADE TODAY','•','','RISKS / BLOCKERS','•','','END-OF-DAY CLOSE','☐ Notes processed','☐ Tasks updated','☐ Waiting / Follow-Up updated','☐ Commitments updated','☐ Tomorrow checked','☐ Tomorrow''s Top 3 identified','☐ Anything important still only in my head?')},
  @{Title='TEMPLATE - Weekly Review'; Body=@('INBOX / CAPTURE','☐ Process OneNote Inbox','☐ Process loose notes','☐ Capture anything still in my head','','PROJECT REVIEW','☐ Review every active project','☐ Update status and next milestone','☐ Confirm next action and owner','☐ Identify risks / blockers','','COMMITMENTS','☐ Review commitments I made','☐ Review commitments others made to me','','WAITING / FOLLOW-UP','☐ Review all waiting items','☐ Send overdue follow-ups','☐ Schedule future follow-ups','','14-DAY LOOKAHEAD','☐ Review calendar','☐ Prepare important meetings','☐ Identify deadlines / decision points','','NEXT WEEK TOP 3','1.','2.','3.')}
 )
 '02 - Meetings' = @(
  @{Title='TEMPLATE - Work Meeting Note'; Body=@('Date:','Project / Area:','Meeting / Topic:','People:','','PURPOSE','What are we discussing or trying to accomplish?','','KEY POINTS','•','•','•','','DECISIONS','• Decision:','  Why:','','ACTIONS','☐ Action:                 Owner:          Due:','☐ Action:                 Owner:          Due:','','WAITING','• Waiting for:            From:           Expected:','','FOLLOW-UP','• Follow up with:         About:          Date:','','RISKS / BLOCKERS','•','','IMPORTANT INFORMATION','•','','NEXT','Next action:','Next milestone / date:','','FILES / LINKS','•','','CLOSE-OUT','☐ Actions moved to Task list','☐ Waiting items recorded','☐ Follow-ups recorded','☐ Commitments recorded','☐ Decisions captured','☐ Important files / links saved','☐ Nothing important left buried in these notes')}
 )
 '03 - Projects' = @(
  @{Title='TEMPLATE - Project Page'; Body=@('Project:','Owner:','Status:','Last Reviewed:','','PURPOSE / OUTCOME','','CURRENT STATUS','','NEXT MILESTONE','Milestone:','Due:','','NEXT ACTIONS','☐ Action:                 Owner:          Due:','☐ Action:                 Owner:          Due:','','WAITING','• Item:                   From:           Expected:','','RISKS / BLOCKERS','•','','KEY DECISIONS','• Date:                   Decision:','','KEY PEOPLE','• Name / Role:','','IMPORTANT LINKS / FILES','•','','LATEST UPDATE','Date:','What changed:','What happens next:','','STATUS QUESTION CHECK','☐ Can I quickly answer current status, last update, next action, owner, due date, blocker, and next milestone?')}
 )
 '04 - People - 1-on-1s' = @(
  @{Title='TEMPLATE - 1-on-1 Page'; Body=@('Person:','Role:','Last 1-on-1:','Next 1-on-1:','','OPEN ITEMS','☐','☐','','THEIR PRIORITIES','•','•','','MY FOLLOW-UPS','☐','☐','','FEEDBACK / COACHING','•','','DEVELOPMENT / GROWTH','•','','DECISIONS / COMMITMENTS','•','','NEXT CONVERSATION','•')}
 )
 '05 - Decisions' = @(
  @{Title='TEMPLATE - Decision Record'; Body=@('Decision:','Date:','Owner:','Project / Area:','','CONTEXT','What prompted the decision?','','OPTIONS CONSIDERED','•','•','','DECISION','','WHY','','IMPACT / CONSEQUENCES','•','','FOLLOW-UP','☐ Action:                 Owner:          Due:')}
 )
 '06 - Reference' = @(
  @{Title='Work Command Center - How To Use'; Body=@('CAPTURE • TRACK • REVIEW • PREPARE • RETRIEVE','','Operating rule: OneNote holds information and context. Tasks, Waiting, Follow-Up, deadlines, and commitments should also be recorded in your Organizational Command System.','','DAILY','1. Open Daily Work Note.','2. Review calendar and preparation.','3. Set Top 3.','4. Capture decisions, risks, waiting items, and follow-ups as work happens.','5. Complete End-of-Day Close.','','WEEKLY','Run the Weekly Review. Review every active project, commitment, waiting item, follow-up, person, deadline, and the next 14 days.','','CORE PRINCIPLE','Capture once. Decide once. Review routinely.')},
  @{Title='TEMPLATE - Follow-Up Waiting Record'; Body=@('Item:','Project / Area:','Waiting for / Follow up with:','Expected / Follow-up date:','Status:','','CONTEXT','','NEXT ACTION IF NO RESPONSE','','NOTES','•')}
 )
 '99 - Archive' = @(
  @{Title='Archive'; Body=@('Move completed or inactive project pages, old meeting series, retired reference material, and other closed information here.')}
 )
}

function Escape-Xml([string]$s) { return [System.Security.SecurityElement]::Escape($s) }

foreach ($sectionName in $sections.Keys) {
  $sectionPath = Join-Path $root ($sectionName + '.one')
  $sectionId = ''
  $one.OpenHierarchy($sectionPath, $notebookId, [ref]$sectionId, 1)
  foreach ($page in $sections[$sectionName]) {
    $pageId = ''
    $one.CreateNewPage($sectionId, [ref]$pageId, 0)
    $ns = 'http://schemas.microsoft.com/office/onenote/2013/onenote'
    $title = Escape-Xml $page.Title
    $htmlLines = foreach ($line in $page.Body) {
      if ($line -eq '') { '<br/>' }
      elseif ($line -match '^[A-Z0-9][A-Z0-9 /&''-]+$' -and $line.Length -lt 40) { '<span style="font-weight:bold;font-size:12pt">' + (Escape-Xml $line) + '</span><br/>' }
      else { (Escape-Xml $line) + '<br/>' }
    }
    $html = ($htmlLines -join '')
    $xml = @"
<?xml version="1.0"?>
<one:Page xmlns:one="$ns" ID="$pageId">
  <one:Title><one:OE><one:T><![CDATA[$title]]></one:T></one:OE></one:Title>
  <one:Outline><one:Position x="36.0" y="90.0" z="0"/><one:OEChildren><one:OE><one:T><![CDATA[$html]]></one:T></one:OE></one:OEChildren></one:Outline>
</one:Page>
"@
    $one.UpdatePageContent($xml, [datetime]::MinValue)
  }
}

$one.NavigateTo($notebookId, '')
Write-Host ''
Write-Host 'Work Command Center created successfully in OneNote.' -ForegroundColor Green
Write-Host "Notebook location: $root"
Write-Host 'The TEMPLATE pages are ready to use. In OneNote, you can optionally save any TEMPLATE page as a Page Template from Insert > Page Templates.'
Read-Host 'Press Enter to finish'
