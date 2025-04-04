# Python Database Integration Project

This project connects to a CSV file, retrieves data, and inserts it into a SQL Server database. It demonstrates how to use Python to work with SQL using `pyodbc`.

## Requirements

- Python 3.x
- `pyodbc` for database connection

## Setup

1. Clone the repository:
	git clone https://github.com/shivampuniani/integration_csv_sql

2. Install the required Python dependencies:
	pip install -r requirements.txt

3. Configure the database connection:

Update the connection strings (if required in main.py) and config.ini for both SQL Server.
SQL Server connection: Update the SERVER, DATABASE, UID, and PWD placeholders in config.ini file.
comma separated file: Ensure the path to your .csv file is correct.
Run the script:

python main.py
  
CSV-SQL-Integration-project/  
│  
├── main.py               # Your main Python program  
├── requirements.txt      # Python dependencies  
├── README.md             # Project documentation  
├── config.ini            # config file to store and configure sql server and file data   
├── .gitignore            # Git ignore rules  
└── log_file.txt          # Log file (will be generated when running the program)  
