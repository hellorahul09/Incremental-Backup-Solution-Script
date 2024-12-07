# Incremental Backup Solution

A script for automated incremental backups using Python and batch files. This solution maps network drives, runs a Python script to back up files incrementally, and disconnects the drives after the backup.

## Features
- **Incremental Backup**: Copies only new or modified files since the last backup.
- **Supports Network Drives**: Maps drives using batch scripts for seamless network access.
- **Logging**: Logs all backup activities for easy debugging and monitoring.

## Prerequisites
- **Python**: Ensure Python 3.x is installed. Download from [python.org](https://www.python.org/).
- **Network Access**: Ensure the source and destination folders are accessible over the network.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/incremental-backup-solution.git
