# Task 3: Git Branching Strategy Implementation

## Task Description
This repository demonstrates the implementation of Task 3 from the selection process at TakeMyTickets company: "Implement Git branching strategy (e.g., Gitflow) for version control."

## Branch Structure and Implementation

Our Git history shows the following structure:
```
*   c85e22d (HEAD -> develop) Merge branch 'hotfix/auth-bug' into develop
|\  
| | * | a97b8a4 (hotfix/auth-bug) fixed the bug
| | |/  
| | *   0176753 (tag: v1.0.0) Merging branch 'release/1.0' to main for production
| | |\  
| | |/  
| |/|   
| * | bc1c3b3 (release/1.0) Bump version to 1.0.0
|/ /  
* |   1e06141 Merging branch 'feature/payment' into develop
|\ \  
| * | 2759672 (feature/payment) Add payment processing
|/ /  
* |   248f246 Merging branch 'feature/login' into develop
|\ \  
| * | 28a6595 (feature/login) Add JWT authentication
|/ /  
* / 59baa90 Develop branch created
|/  
* 94fa72c Initial commit: Project setup
```

### Main Branches

1. **Main Branch**
   - Purpose: Contains production-ready code
   - History: Receives merged code from releases and hotfixes
   - Current state: Stable production version

2. **Develop Branch**
   - Purpose: Integration branch for all development work
   - History: Created from initial commit (59baa90)
   - Current state: Contains all completed features and fixes

### Feature Branches

1. **feature/login (28a6595)**
   - Purpose: Implement authentication functionality
   - Added: JWT authentication system
   - Merged: Into develop via commit 248f246

2. **feature/payment (2759672)**
   - Purpose: Implement payment system
   - Added: Payment processing functionality
   - Merged: Into develop via commit 1e06141

### Release Branch

**release/1.0 (bc1c3b3)**
- Purpose: Prepare first production release
- Actions: 
  - Version bump to 1.0.0
  - Merged into main (0176753)
  - Tagged as v1.0.0

### Hotfix Branch

**hotfix/auth-bug (a97b8a4)**
- Purpose: Fix critical authentication issue
- Actions:
  - Fixed authentication bug
  - Merged into both main and develop (c85e22d)

## Implementation Timeline

1. Initial Setup
   - Created repository with initial commit (94fa72c)
   - Established develop branch (59baa90)

2. Feature Development
   - Implemented login feature (28a6595)
   - Implemented payment processing (2759672)

3. Release Process
   - Created release/1.0 branch (bc1c3b3)
   - Tagged first release as v1.0.0 (0176753)

4. Bug Fix
   - Implemented hotfix for auth bug (a97b8a4)
   - Merged fixes to maintain codebase integrity

## Task Completion Checklist

✅ Implemented complete Gitflow structure  
✅ Created and managed feature branches  
✅ Handled release process  
✅ Demonstrated hotfix implementation  
✅ Maintained clean merge history  
✅ Proper version tagging  

## Additional Information

This implementation demonstrates understanding of:
- Branch management
- Version control best practices
- Code integration workflows
- Release management
- Emergency fix procedures

---
Completed by: Rathinadevan EM  
Selection Task #3 for TakeMyTickets


# Task 4: Automate Backup/Restore for PostgreSQL Databases

## Task Description
This repository demonstrates the implementation of **Task 4** from the selection process at **TakeMyTickets** company: "Automate backup/restore for MongoDB/PostgreSQL using a script."

The task involves creating scripts that automate backup and restore operations for PostgreSQL databases, ensuring secure credential management, robust error handling, and proper logging.

---

## Implementation Details

### Python Scripts Overview

1. **`backup_script.py`**
   - Automates the process of taking a backup of a PostgreSQL database.
   - Key Features:
     - Reads database credentials and configuration from a `.env` file.
     - Saves backup files with a timestamped filename.
     - Compresses backup files using `gzip` for space efficiency.
     - Logs all operations to a log file.

2. **`restore_script.py`**
   - Automates the restoration of a PostgreSQL database from a backup file.
   - Key Features:
     - Supports both compressed (`.gz`) and uncompressed (`.sql`) backup files.
     - Checks if the specified database exists; creates it if necessary.
     - Logs all operations to a log file.

---

## How to Run the Scripts

### Prerequisites
- Install Python 3.x.
- Install PostgreSQL.
- Install the required Python libraries:
  ```bash
  pip install python-dotenv
  ```
- Create a `.env` file in the repository root with the following variables:

```plaintext
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DATABASE=your_database
BACKUP_PATH=/path/to/backup/directory
```

### Backup Script

To run the backup script:
```bash
python3 backup_script.py
```

- **Expected Output:**
  - A `.sql.gz` backup file is created in the directory specified by `BACKUP_PATH`.
  - A log file `logs/backup.log` will record all actions.

### Restore Script

To run the restore script:
```bash
python3 restore_script.py <path_to_backup_file>
```

- **Arguments:**
  - `<path_to_backup_file>`: Full path to the backup file to restore. This can be either a `.sql` or `.gz` file.

- **Expected Output:**
  - Restores the database from the specified backup file.
  - Logs details in `logs/restore.log`.

---

## Logging

- **Log Files:**
  - `logs/backup.log`: Records details of the backup process.
  - `logs/restore.log`: Records details of the restore process.

Logs include:
- Timestamps for each operation.
- Descriptions of actions performed.
- Error details (if any).

---

## Implementation Features and Highlights

- **Security:**
  - Credentials are stored in a `.env` file, ensuring sensitive information is not hardcoded.
  - `.env` and logs are excluded from version control via `.gitignore`.

- **Automation:**
  - Eliminates manual database management tasks.
  - Reduces the risk of human errors during backup and restore.

- **Error Handling:**
  - Comprehensive exception handling ensures the scripts exit gracefully in case of issues.

- **Efficiency:**
  - Backups are compressed to save storage space.

---

## Task Completion Checklist

✅ Backup script implemented and tested  
✅ Restore script implemented and tested  
✅ Credential management using `.env`  
✅ Log files generated for auditing  
✅ Compression of backup files  
✅ Proper error handling implemented  

---

## Additional Notes

These scripts were created as part of the **TakeMyTickets** intern selection process. They demonstrate proficiency in automating database management tasks and secure handling of sensitive operations.

---

**Completed by:** Rathinadevan E M  
**Task:** #4 from TakeMyTickets Selection Process
