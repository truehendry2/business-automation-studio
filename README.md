# Business Automation Studio

Business Automation Studio is a Python-based automation platform for small business workflows. It combines a clean Streamlit interface with reusable automation modules, SQLite logging, and tools for Excel automation, reporting, email workflows, browser automation, and AI-powered assistance.

The goal is to provide one professional dashboard where business users can run automations, track results, review activity, and manage future workflow tools from a single place.

## Current Status

Version: 1.1

Currently included:

- Streamlit dashboard
- Excel automation toolkit
- SQLite database logging
- Persistent automation history
- Recent activity tracking
- Dashboard metrics from real usage data
- Modular structure for future automation tools

## Features

### Dashboard

- Total automation tasks
- Completed tasks
- Failed tasks
- Success rate
- Recent activity
- Automation usage chart
- Recently processed files

### Excel Automation Toolkit

- Upload CSV or Excel files
- Run spreadsheet automations
- Remove duplicate rows
- Process business data
- Download cleaned results
- Save automation history

### SQLite Logging System

Each automation run is saved with:

- Timestamp
- File name
- Automation tool
- Original row count
- New row count
- Status
- Result message

## Screenshots

Add screenshots inside the `screenshots` folder.

Recommended files:

```text
screenshots/dashboard.png
screenshots/excel-toolkit.png
screenshots/recent-activity.png