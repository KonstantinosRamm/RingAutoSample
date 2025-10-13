# 🧵 Textile Quality Control – Ring Spinning Machines

## 📌 Overview
In the textile industry, daily quality control requires sampling from **ring spinning machines**. Each machine may have up to **1200 spindles**, but only **48 specific samples** must be selected in sequence. Traditionally, this process is tracked manually in notebooks, which often caused **time delays** and **human errors**.

This project provides a **digital tool** to streamline the workflow, combining backend logic with a frontend dashboard. It supports **CRUD operations**—you can **create, read, update, and delete** machine entries—making machine management fast and reliable.


---
## 🔗 Routes
- `/` → Main page for sample selection and dashboard.  
- `/edit` → Modify existing machines (last samples, date picked, nominal count of the yarn).  
- `/delete` → Delete an existing machine.  
- `/add` → Add a new machine.  
- `/machines` → View all available machines and switch them on or off.  
- `/numbers` → View all machine samples for each block.  

---

## 💡 Features
- Tracks the last sampled numbers for each machine  
- Automatically calculates the **next samples** in sequence  
- Suggests the **next machine** to sample based on the oldest last sampling  
- Allows **manual input/correction** when necessary
- REST API implemented in Flask
> ⚡ Can you guess what happens if you cause an Error 500?  
> Play it and find out… 😏🎮

---
## 🖥 REST API
- `/machines`       GET     Get all machines 
- `/machines/id`    GET     Get a specific machine
- `/machines`       PATCH   Update one or more machines 
- `/machines`       POST    Add a new machine 
- `/machines/<id>`  DELETE  Delete a machine by ID
  [API examples](docs/api.md)
> All API endpoints accept and return data in **JSON format**.

---

## ⚠️ Disclaimer & Table Customization

The sampling tables included in this project are specific to our factory setup. 
The total spindles, block distribution, and sample positions may vary in other factories, 
even for the same machine model (e.g., Rieter G30, G35, G8).

All sampling patterns and procedures follow the **Uster Standards**, ensuring proper 
representation and consistency of yarn quality measurements.

### How the Table Keys Work
- Each key in the machine table represents a **block of 12 samples**, e.g., "13-24".  
- The keys form a **cyclic mapping** of samples:  
  - To find the samples for a given key, the system uses the **first two numbers of the previous block**, e.g., "1-12". If invalid numbers are provided, sampling starts from the first number.  
  - For the **first key**, the system uses the **first two numbers of the last key** to start the cycle.  
- This ensures that all sample numbers for a machine can be accessed in sequence **without errors**, even when the table loops.


### How to Add or Modify Machine Tables
1. Open `machines.py`.
2. Add a new dictionary for the machine model, following the existing format:
   ```python
   NEW_MACHINE = {
       "n-(n+11)": [1,13,...],
       "1-13": [sample_numbers...],
       ...
       "n-(n+11)": [sample_numbers]
   }
3. Add the new machine to `machine_dictionary`
    ```python
    machine_dictionary = {
      "previews_machine" : previous_machine,
      "NEW_MACHINE" : NEW_MACHINE
    }

---

## 🎯 Motivation
The tool was created to solve real operational pain at work:  
- Manual tracking was **time-consuming**  
- High risk of **selecting the wrong machine** for sampling  
- Ensures **systematic, chronological selection** across multiple machines  

---

## INSTALLATION
- [DEBIAN](docs/linux.md)

---

## FUTURE IMPROVEMENTS
- [TO DO](docs/todo.md)

---





