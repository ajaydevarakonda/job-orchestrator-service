# Job Execution System
## 🧠 What This Application Does
This system is a **lightweight job runner** designed to execute long-running tasks (hours to days) reliably.

It:
* Fetches jobs from a queue (Redis / DB)
* Executes them as OS processes
* Tracks their state
* Collects results and logs
* Updates final status

---

# ⚡ Key Design Points
## 1. File-Based Communication Instead of IPC
Child processes write results to files instead of sending large data via stdout.
**Why:** avoids buffer limits, corruption, and broken pipes.

---

## 2. Atomic File Writes
Results are written using:
```text
temp file → fsync → rename
```
**Why:** ensures files are never partially written or corrupted.

---

## 3. Single Writer to State Store
Only the parent process updates Redis/DB.
**Why:** avoids race conditions and inconsistent state.

---

## 4. PID + Metadata Tracking
Processes are tracked using PID along with start time.
**Why:** prevents issues due to PID reuse.

---

## 5. Poll-Based Monitoring
A simple loop checks job status periodically.
**Why:** reliable and easy to reason about.

---

## 6. Structured Job Directories
Each job writes to its own directory:

```text
/jobs/<job_id>/
  result.json
  stdout.log
  stderr.log
```

**Why:** improves debugging and isolation.

### Key points:
* Prevents IPC-related failures between parent and child for long related tasks
    * Prevented partial / corrupt data reads
* detached processes + file-based results + centralized state updates
    * Improved reliability for long-running jobs
* Removed tight coupling between processes

---

# 🧠 Clean Code Approach (Practical)
* Clear separation of responsibilities
* Minimal abstractions (no over-engineering)
* Explicit lifecycle methods (start, complete, fail)
* Centralized handling of complex logic (files, process execution)

---

# 🧠 One-line takeaway
> A simple, durable system that favors reliability over cleverness for long-running jobs.
