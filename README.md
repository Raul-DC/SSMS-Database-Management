# SSMS-Database-Management

 This project is designed to automate the process of integrating weekly CSV data into an SQL Server database, ensuring that no duplicate records are stored and that logs of every execution are maintained.

 For it we will use SSMS (SQL Server Management Studio 19).

![image](https://github.com/user-attachments/assets/bba72dcc-8114-4e99-ac64-7b66ac74ca9c)


## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Process Overview](#process-overview)
4. [Scripts Automation](#scripts-automation)
5. [Logging and Scheduling](#logging-and-scheduling)
6. [Troubleshooting](#troubleshooting)
7. [End](#end)

---

## Installation

### Step 1: Restore the Database Backup

 You can restore the database using either `.bak` or `.bacpac` files.

- **For .bak file:**
    - Use SQL Server Management Studio (SSMS) to restore the database.
    ![image](https://github.com/user-attachments/assets/53925e66-416b-447b-b897-4b2eeb0d95e0)



- **For .bacpac file:**
    - Use SSMS to import the `.bacpac` file.
    ![image](https://github.com/user-attachments/assets/a3e40dc3-8e13-4022-8e61-d89d365482ad)

### Step 2: Set Up the Environment

 Make sure you set up the `.env` file with the correct variables:

```env
CSV_URL=https://example.com/data.csv
SAVE_DIRECTORY=./data/CSV_Files
DB_SERVER=localhost
DB_DATABASE=Testing_ETL
DB_USERNAME=sa
DB_PASSWORD=your_password
```

---

## Usage

### Step 1: Download Weekly CSV File

 Run the `weekly_extract.py` script to download the weekly CSV file.

![image](https://github.com/user-attachments/assets/694906a5-6ebd-41fe-ad56-f46f216a5993)


### Step 2: Insert Data into the "Unificado" Table

 Run the `insert_to_table.py` script to insert the downloaded CSV data into the database.

![image](https://github.com/user-attachments/assets/6a3df976-e3c7-4fad-9945-2774c2b4b1f7)

---

## Process Overview

1. **Download CSV file**: The script `weekly_extract.py` downloads the CSV file.
2. **Insert data into table**: The script `insert_to_table.py` inserts the CSV rows into the "Unificado" table and adds a timestamp for each row in the `FECHA_COPIA` field.
3. **Remove duplicates**: A query ensures that no duplicate records remain in the database.

```markdown
+--------------+
| IDE | Script | (weekly_extract.py)
+--------------+
|
v
+-------------------+       +----------------+
|  URL GET request  | ----> | Get a CSV File |
+-------------------+       +----------------+
|
v
+--------------+
| IDE | Script | (insert_to_table.py)
+--------------+
|
v
+-----------------------------------------------------------+
| Extract CSV File's Data, Transform it and Load it on SSMS |
+-----------------------------------------------------------+
|
v
+------------------+
| SSMS | SQL Query | ----> (Remove duplicates and store execution logs)
+------------------+

```

---

## Scripts Automation

I use Windows 10 Home so I will show it using this OS.

To ensure the scripts run without manual intervention, the execution of both weekly_extract.py and insert_to_table.py is automated using the Windows Task Scheduler. This allows for the seamless download of the CSV file and the insertion of data into the database at the scheduled time.

* The automation setup involves:

1. Creating scheduled tasks that point to the Python executable and the respective script paths.

![image](https://github.com/user-attachments/assets/97be939d-6885-45eb-a0c7-0d39e529e322)


2. Setting the schedule to run every Monday at 🕟 4:30 AM, ensuring data is updated weekly.

![image](https://github.com/user-attachments/assets/5b3055a5-9b59-4c10-a5bf-3598e86028a0)


---



## Logging and Scheduling

 **Logs**: Each execution logs important details like the number of rows affected, the server instance, and the date.
    ![image](https://github.com/user-attachments/assets/ab0c2644-d1b2-40ff-b1cc-b44786fd5e04)



 **Scheduling**: For this we use the SQL Server Agent 🛠️

 1.- Create a new job:

   ![image](https://github.com/user-attachments/assets/415a3628-a6bb-444f-bbb1-e10388825ccf)
   
 2.- Input the query to eliminate duplicates and store logs:

   ![image](https://github.com/user-attachments/assets/15c44f21-a76a-4633-b8d2-4eec7a733abd)
   
 3.- Set the process to automatically run every Monday at 🕔 5:00 AM:

   ![image](https://github.com/user-attachments/assets/a340e6d9-668b-4601-8895-ec6666ae9375)



---

## Troubleshooting

- Make sure the `.env` file contains the correct database credentials. 🙌🏻✅
  
- Make sure your computer is powered on and not in sleep mode during the scheduled time. ❌🖥️💤
  
- You can check the task history in Task Scheduler to see if it has run successfully. 🔎🧾

---

## End

- Is this possible on Cloud Services like GCP or AWS? Of course! this is just for showing the basic concepts on a local enviroment... 😎

---
