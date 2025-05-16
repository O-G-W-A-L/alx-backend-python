# Python Generators

---

## About

This project guides you through **advanced use of Python generators** to handle large datasets, batch process records, lazily paginate, and compute aggregates (like average age) without loading everything into memory. You’ll connect to a MySQL database (`ALX_prodev`), seed it with user data, then implement four focused tasks, each demonstrating a different generator pattern.

---

## Learning Objectives

- **Master Generators**: Build and consume Python `yield`‑based generators.  
- **Large Data Handling**: Stream rows, process in batches, and paginate lazily.  
- **Memory Efficiency**: Compute aggregates (average age) without loading full datasets.  
- **Database Integration**: Use SQL queries from Python (no SQL `AVG()`) for dynamic data access.  
- **Performance Optimization**: Apply lazy evaluation to real‑world scenarios.

---

## Prerequisites

- Python 3.x installed  
- MySQL (or MariaDB) server running locally  
- `mysql-connector-python` package installed  
- Basic Git & GitHub fluency

---

## Repository Structure
```bash
python-generators-0x00/
├── 0-main.py
├── seed.py
├── user_data.csv
├── 0-stream_users.py
├── 1-main.py
├── 1-batch_processing.py
├── 2-main.py
├── 2-lazy_paginate.py
├── 3-main.py
├── 4-stream_ages.py
└── README.md
```
---

## Tasks Overview

### Task 0: Database Seeding  
- **seed.py**:  
  - Connect to MySQL server  
  - Create `ALX_prodev` database and `user_data` table  
  - Load `user_data.csv` (UUID, name, email, age)

### Task 1: Stream Rows  
- **0-stream_users.py**:  
  - `stream_users()` generator  
  - Yields one user record at a time (dictionary)  
  - Single loop using `yield`

### Task 2: Batch Processing  
- **1-batch_processing.py**:  
  - `stream_users_in_batches(batch_size)` generator  
  - `batch_processing(batch_size)` filters users over 25  
  - ≤ 3 loops total, uses `yield`

### Task 3: Lazy Pagination  
- **2-lazy_paginate.py**:  
  - `paginate_users(page_size, offset)` fetches one page  
  - `lazy_paginate(page_size)` generator, single loop, yields pages on demand

### Task 4: Memory‑Efficient Aggregation  
- **4-stream_ages.py**:  
  - `stream_user_ages()` generator yields ages  
  - `average_age()` computes and prints average via two loops, no SQL `AVG()`

---

## How to Run

1. **Clone** the repo and `cd` into `python-generators-0x00`.  
2. **Install** dependencies:  
   ```bash
   pip install mysql-connector-python

