A lightweight Python GUI application built with `pandas` and `tkinter` to help e-commerce managers, inventory specialists, and data auditors clean up their product catalogs. 

The tool compares an active website product export against a master ERP/Inventory spreadsheet (Everest) to instantly identify products that are still active online but have been discontinued, removed, or renamed in the inventory system.

---

## 🚀 Features

* **Smart Filtering:** Automatically skips website products already marked as inactive (`Active = No`), saving you from auditing items you've already handled.
* **Data Normalization:** Robust string cleaning strips hidden spaces and standardizes letter casing to prevent false positives.
* **File Flexibility:** Supports both Excel (`.xlsx`, `.xls`) and CSV files.
* **Accidental Data Integrity Check:** Because it looks for exact string matches, **it automatically catches part number updates**. If an item's SKU was changed in Everest (e.g., from `501-173A` to `SRV501-173A`), it will flag the old SKU so you can update or disable it on the website.

---

## 📋 Spreadsheet Requirements

For the program to run successfully, your spreadsheets must contain the following column headers (case-sensitive):

### 1. Website Spreadsheet
* `Sku`: The product part number.
* `Active`: Must contain `Yes` or `No`. The script will *only* check items marked `Yes`.

### 2. Everest Spreadsheet
* `Code`: The product part number used in your master inventory.

---

## 💻 How It Works

1. **Load:** Read both data files, preserving leading zeros (like `05301`).
2. **Filter:** Drops any row from the website data where `Active` is not `Yes`.
3. **Match (Left Join):** Compares the remaining active website SKUs against the Everest inventory codes.
4. **Report:** Generates a clean, line-by-line `.txt` report of every active website SKU that could not be found in Everest.

---

## 🛠️ Installation & Setup

### Prerequisites
Make sure you have Python 3.x installed along with `pandas` and `openpyxl` (required for Excel files).

```bash
pip install pandas openpyxl
