import frappe

def run():
    # Check 5 invoices that should be Paid
    invoices = frappe.get_all("Sales Invoice", 
                             filters={"docstatus": 1}, 
                             fields=["name", "status", "outstanding_amount", "grand_total"], 
                             limit=10)
    
    print("Name | Status | Outstanding | Grand Total")
    print("-" * 50)
    for inv in invoices:
        print(f"{inv.name} | {inv.status} | {inv.outstanding_amount} | {inv.grand_total}")

if __name__ == "__main__":
    run()
