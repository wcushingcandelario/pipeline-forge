---
cssclasses: [work-dashboard]
tags: [work-os, daily]
date: {{date:YYYY-MM-DD}}
---

# 🔷 Work Command Center — {{date:dddd, MMMM D, YYYY}}

> [!focus] Daily operating rhythm
> **Prepare • Prioritize • Execute • Follow Up • Close Loops**

## ☀️ Morning Startup
> [!routine]
> - [ ] Check work email and triage
> - [ ] Review today's calendar
> - [ ] Review next 48 hours
> - [ ] Review open follow-ups
> - [ ] Review active projects
> - [ ] Review risks / issues
> - [ ] Review documents requiring action
> - [ ] Review team commitments
> - [ ] Set today's Top 3
> - [ ] Prepare for first meeting

## 🎯 Today's Top 3
> [!top3]
> 1. 
> 2. 
> 3. 

## 🚦 Active Projects
```dataview
TABLE WITHOUT ID file.link AS "Project",
choice(status="on-track","🟢 On Track",choice(status="attention","🟡 Attention",choice(status="at-risk","🔴 At Risk",status))) AS "Status",
next_action AS "Next Action", target_date AS "Target"
FROM "02 - Projects"
WHERE type="work-project" AND status!="complete"
SORT target_date ASC
```

## ⏳ Follow-Ups
```dataview
TABLE WITHOUT ID file.link AS "Follow-Up", owner AS "Owner", follow_up AS "Due", status AS "Status"
FROM "04 - Follow-Ups"
WHERE type="work-follow-up" AND status!="closed"
SORT follow_up ASC
```

## ⚠️ Risks & Issues
```dataview
TABLE WITHOUT ID file.link AS "Risk / Issue", severity AS "Severity", owner AS "Owner", next_action AS "Next Action"
FROM "06 - Risks & Issues"
WHERE (type="risk" OR type="issue") AND status!="closed"
SORT severity DESC
```

## 📅 Upcoming Meetings
```dataview
TABLE WITHOUT ID file.link AS "Meeting", meeting_date AS "Date", purpose AS "Purpose"
FROM "03 - Meetings"
WHERE type="meeting" AND meeting_date >= date(today)
SORT meeting_date ASC
LIMIT 8
```

## 📄 Documents Requiring Action
```dataview
TABLE WITHOUT ID file.link AS "Document", action_needed AS "Action", due AS "Due"
FROM "07 - Documents"
WHERE type="work-document" AND action_required=true AND status!="complete"
SORT due ASC
```

## ✅ Open Work Tasks
```dataview
TASK
FROM "02 - Projects" OR "03 - Meetings" OR "04 - Follow-Ups" OR "06 - Risks & Issues" OR "07 - Documents" OR "08 - Team & People"
WHERE !completed
SORT file.name ASC
```

## 📥 Work Inbox
> [!inbox]
> - [ ] Email requiring action
> - [ ] Request requiring response
> - [ ] Document requiring review
> - [ ] New commitment
> - [ ] New follow-up

## 📝 Quick Capture
> [!capture]
> - 
> - 
> - 
> - 
> - 

## 🌙 End-of-Day Shutdown
> [!evening]
> - [ ] Process work email
> - [ ] Process Quick Capture
> - [ ] Update project notes
> - [ ] Update follow-ups
> - [ ] Record decisions
> - [ ] Update risks / issues
> - [ ] File important documents
> - [ ] Review tomorrow's calendar
> - [ ] Prepare tomorrow's first meeting
> - [ ] Set tomorrow's likely Top 3
> - [ ] Confirm nothing important exists only in memory

> [!success] Shutdown complete
> **Commitments captured. Follow-ups visible. Tomorrow prepared.**
