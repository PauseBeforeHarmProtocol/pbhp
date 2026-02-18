# PBHP Door Library

## Purpose

Pre-built "Door" (safer alternative) templates for common agent domains. Agents can reference these instead of reasoning from scratch, reducing latency and improving consistency.

**Status:** Reference document, v0.8

---

## How to Use

When PBHP analysis reaches the Door step, check if the action domain matches a category below. Use the suggested Door as a starting point, adapt to context.

---

## Domain: Email Operations

### Send Email
**Risk factors:** Wrong recipient, sensitive content exposure, irreversible once sent
**Default Door:** Preview full email (recipients, subject, body) → get explicit confirmation → send
**ORANGE+ Door:** Preview + wait 30 seconds + re-confirm recipient list

### Delete Email
**Risk factors:** Permanent data loss, legal/compliance implications
**Default Door:** Move to trash (recoverable) instead of permanent delete → confirm scope
**ORANGE+ Door:** Create backup/export first → move to trash → confirm

### Bulk Email Operations
**Risk factors:** Blast radius, wrong filter criteria, compliance
**Default Door:** Preview affected count + sample of 3 emails → confirm → process in batches with pause between
**Always ORANGE minimum** due to blast radius

---

## Domain: File Operations

### Delete Files
**Risk factors:** Data loss, wrong selection, no undo
**Default Door:** List files to delete → confirm → move to trash (not permanent delete)
**ORANGE+ Door:** Create backup → list files → confirm → trash

### Modify Files
**Risk factors:** Content corruption, version loss
**Default Door:** Create backup copy → modify → show diff → confirm
**If code files:** Run tests after modification

### Bulk File Operations
**Risk factors:** Blast radius, wrong glob/filter
**Default Door:** Preview affected files (count + sample) → confirm → process with progress reporting
**Always ORANGE minimum** due to blast radius

---

## Domain: Code Execution

### Run Untrusted Code
**Risk factors:** System compromise, data exfiltration, resource exhaustion
**Default Door:** Sandbox execution → review output → decide on further action
**RED gate:** Never run code from untrusted sources without sandbox

### Deploy to Production
**Risk factors:** Service disruption, data corruption, rollback difficulty
**Default Door:** Deploy to staging → verify → get explicit production approval → deploy with rollback plan
**Always ORANGE minimum**

### Database Operations (Write/Delete)
**Risk factors:** Data loss, cascade effects, compliance
**Default Door:** Preview affected rows (count + sample) → confirm → execute with transaction (rollback on error)
**DELETE/DROP operations:** Always RED minimum → require explicit confirmation + backup verification

---

## Domain: API Calls (External)

### POST/PUT/DELETE to External Services
**Risk factors:** Irreversible state changes, rate limits, auth exposure
**Default Door:** Preview request (URL, method, body summary) → confirm → execute → report result
**If auth tokens involved:** Verify destination is expected service

### Batch API Operations
**Risk factors:** Rate limiting, cascading failures, blast radius
**Default Door:** Preview count + sample → confirm → process with rate limiting + error handling
**Always ORANGE minimum**

---

## Domain: User/Account Management

### Create/Delete Accounts
**Risk factors:** Identity, access control, irreversibility
**Default Door:** Always require explicit human confirmation → never auto-create/delete
**Always RED minimum** for deletion

### Modify Permissions
**Risk factors:** Access escalation, security compromise
**Default Door:** Show current vs proposed permissions → explain implications → get confirmation
**Always ORANGE minimum**

---

## Domain: Communication (Chat/Social)

### Post Public Content
**Risk factors:** Reputation, permanence, audience reach
**Default Door:** Preview content → confirm audience/channel → post
**ORANGE+ Door:** Preview + cooling period + re-confirm

### Send Messages on Behalf of User
**Risk factors:** Impersonation perception, relationship damage
**Default Door:** Draft message → show recipient + content → get explicit send confirmation
**Never auto-send without confirmation**

---

## Domain: Financial Operations

### Any Transaction
**Risk factors:** Financial loss, irreversibility, compliance
**Default Door:** Always require explicit human confirmation with amount + recipient + method
**Always RED minimum** — agents should not autonomously execute financial transactions

---

## Creating Custom Doors

When no pre-built Door fits:

1. **Start with the reversibility question:** Can this be undone? If no → minimum ORANGE
2. **Add a preview step:** Show what will happen before doing it
3. **Add a confirmation step:** Get explicit approval
4. **Add a verification step:** Check the result after execution
5. **Consider blast radius:** One person affected vs many → scale caution accordingly

**Template:**
```
Door: [action description]
1. Preview: [what to show the user]
2. Safeguard: [backup/sandbox/staging step]
3. Confirm: [what approval to get]
4. Execute: [how to do it safely]
5. Verify: [how to check it worked correctly]
```

---

## Update Log

**v0.8 (Feb 2026):** Initial Door Library with 8 common domains.
