# Sales-Ops Tool Kit #

## Why this Exists

The "technical" side of a Sales Ops Specialist typically includes:
  - Copying/pasting into excel 
  - Creating and maintaining reports
  - Mass emailing customers

This part of the job takes up ~80% of the time. 
It is an "operator" position; as in the person is 
intedended to move data from one place to another. 

Most of this can be automated. This is why I created the Sales-Ops Toolkit

It’s a Python-based, class-structured, modular project designed to streamline 
and automate the data processing tasks that dominate Sales Ops workflows.

## What Is In The Toolkit

- **'Baseloader'**: Read excel files into dataframes
- '**Cleaner**': Clean and standardizes data in dataframes
- '**Exporter**': Sends or saves data to various destinations (CSV, MSSQL, etc.)

## Tech Stack

- Python
- pandas
- openpyxl / xlsxwriter
- pathlib, logging, and standard libs
