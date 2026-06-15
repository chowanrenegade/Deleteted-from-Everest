import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def load_and_map(file_path, is_everest=True):
    """Loads file, extracts specific columns, and renames them."""
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == '.csv':
            df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
        else:
            df = pd.read_excel(file_path, dtype=str, keep_default_na=False)
    except Exception as e:
        raise ValueError(f"Could not read file: {e}")

    # Column Mapping Logic
    if is_everest:
        cols = {'Code': 'part_number'}
    else:
        # Added 'Active' column for the website mapping
        cols = {'Sku': 'part_number', 'Active': 'active_status'}

    # Verify columns exist
    for original_col in cols.keys():
        if original_col not in df.columns:
            raise ValueError(f"Missing column: '{original_col}' in {os.path.basename(file_path)}")

    # Filter to only necessary columns and rename
    df = df[list(cols.keys())].rename(columns=cols)
    
    # Clean Part Numbers: Uppercase and strip spaces
    df['part_number'] = df['part_number'].astype(str).str.strip().str.upper()
    
    # Clean Active Status (Website only)
    if not is_everest:
        df['active_status'] = df['active_status'].astype(str).str.strip().str.upper()
    
    return df

def run_comparison():
    file_web = entry_web.get()
    file_ev = entry_ev.get()

    if not file_web or not file_ev:
        messagebox.showerror("Error", "Please select both files first.")
        return

    try:
        # 1. Load and Format
        df_web = load_and_map(file_web, is_everest=False)
        df_ev = load_and_map(file_ev, is_everest=True)

        # FILTER: Skip items where Active is not 'YES'
        # This ignores 'No', blanks, or any other status
        df_web = df_web[df_web['active_status'] == 'YES']

        if df_web.empty:
            messagebox.showinfo("No Active Parts", "There are no active parts in the website file to check.")
            return

        # 2. Left Join: Keep active website parts, match with Everest
        merged_df = pd.merge(df_web, df_ev, on='part_number', how='left', indicator=True)

        # 3. Identify missing parts (Exist on website as YES, missing from Everest)
        missing_from_everest = merged_df[merged_df['_merge'] == 'left_only']

        # 4. Save File Dialog
        if not missing_from_everest.empty:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                initialfile="discontinued_parts.txt",
                title="Save Discontinued Parts Report"
            )
            
            if save_path:
                with open(save_path, 'w') as f:
                    f.write(f"DISCONTINUED PARTS REPORT (Active on Website, Missing from Everest)\n")
                    f.write("These parts are currently Active but missing from Everest. Disable them.\n")
                    f.write("="*65 + "\n\n")
                    
                    for part in missing_from_everest['part_number']:
                        f.write(f"{part}\n")
                        
                messagebox.showinfo("Success", f"Found {len(missing_from_everest)} active parts missing from Everest.\nReport saved to: {save_path}")
        else:
            messagebox.showinfo("All Clear", "All active website parts were found on Everest!")

    except Exception as e:
        messagebox.showerror("Processing Error", str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("Discontinued Product Auditor")
root.geometry("500x420") # Tweak height slightly for new text label

def browse(entry_field):
    fn = filedialog.askopenfilename(filetypes=[("All Data Files", "*.xlsx *.xls *.csv")])
    if fn:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, fn)

# UI Elements
tk.Label(root, text="Website Spreadsheet", font=('Arial', 10, 'bold')).pack(pady=(20,0))
tk.Label(root, text="(Needs 'Sku' and 'Active' columns)", font=('Arial', 8, 'italic')).pack()
entry_web = tk.Entry(root, width=50)
entry_web.pack(pady=5)
tk.Button(root, text="Browse Website File", command=lambda: browse(entry_web)).pack(pady=5)

tk.Label(root, text="Everest Spreadsheet", font=('Arial', 10, 'bold')).pack(pady=(20,0))
tk.Label(root, text="(Needs 'Code' column)", font=('Arial', 8, 'italic')).pack()
entry_ev = tk.Entry(root, width=50)
entry_ev.pack(pady=5)
tk.Button(root, text="Browse Everest File", command=lambda: browse(entry_ev)).pack(pady=5)

tk.Button(root, text="FIND DISCONTINUED PARTS", command=run_comparison, 
          bg="#e74c3c", fg="white", font=('Arial', 12, 'bold'), height=2).pack(pady=25, fill='x', padx=50)

root.mainloop()
