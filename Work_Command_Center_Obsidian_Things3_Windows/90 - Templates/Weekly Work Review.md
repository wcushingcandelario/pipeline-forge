---
cssclasses: [work-dashboard]
tags: [work-os, weekly-review]
type: weekly-review
date: {{date:YYYY-MM-DD}}
---
# 🗓 Weekly Work Review — {{date:MMMM D, YYYY}}

## Close the Week
> [!review]
> - [ ] Process inbox
> - [ ] Review all active projects
> - [ ] Review commitments and follow-ups
> - [ ] Review risks / issues
> - [ ] Review decisions
> - [ ] Review next two weeks of calendar
> - [ ] Prepare important meetings
> - [ ] Review team commitments

## Active Projects
```dataview
TABLE WITHOUT ID file.link AS "Project", status AS "Status", next_action AS "Next Action", target_date AS "Target"
FROM "02 - Projects"
WHERE type="work-project" AND status!="complete"
SORT target_date ASC
```

## Open Follow-Ups
```dataview
TABLE WITHOUT ID file.link AS "Follow-Up", owner AS "Owner", follow_up AS "Due"
FROM "04 - Follow-Ups"
WHERE type="work-follow-up" AND status!="closed"
SORT follow_up ASC
```

## Risks & Issues
```dataview
TABLE WITHOUT ID file.link AS "Item", severity AS "Severity", owner AS "Owner", next_action AS "Next Action"
FROM "06 - Risks & Issues"
WHERE (type="risk" OR type="issue") AND status!="closed"
```

## Next Week Top 3
> [!top3]
> 1. 
> 2. 
> 3. 
