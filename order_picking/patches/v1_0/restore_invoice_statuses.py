import frappe
from datetime import datetime

def execute():
	"""
	Recovery patch: Restore workflow statuses on Sales Invoices that were reset.
	
	This patch recalculates and restores the correct workflow status for all
	submitted Sales Invoices based on their payment status.
	"""
	restore_sales_invoice_statuses()


def restore_sales_invoice_statuses():
	"""Restore workflow statuses for all Sales Invoices"""
	
	# Get all submitted Sales Invoices
	invoices = frappe.get_all(
		"Sales Invoice",
		filters={
			"docstatus": 1,  # Only submitted invoices
		},
		fields=["name", "status", "outstanding_amount", "grand_total", "due_date"]
	)
	
	restored_count = 0
	failed_count = 0
	
	for invoice in invoices:
		try:
			doc = frappe.get_doc("Sales Invoice", invoice.name)
			
			# Calculate the correct status based on payment
			new_status = calculate_invoice_status(doc)
			
			# If status is different from current, update it
			if new_status and new_status != doc.status:
				doc.db_set("status", new_status, update_modified=False)
				restored_count += 1
		except Exception as e:
			failed_count += 1
			frappe.logger().error(f"Error updating {invoice.name}: {str(e)}")
	
	frappe.db.commit()
	
	if restored_count > 0:
		frappe.logger().info(f"Restored workflow status for {restored_count} invoices")


def calculate_invoice_status(invoice):
	"""
	Calculate correct workflow status for a Sales Invoice based on payment status.
	
	Returns one of: 'Paid', 'Unpaid', 'Partly Paid', 'Overdue', or None
	"""
	import math
	
	if invoice.docstatus != 1:  # Only for submitted invoices
		return None
	
	outstanding = invoice.outstanding_amount or 0
	total = invoice.grand_total or 0
	due_date = invoice.due_date
	
	# If outstanding is 0 or negative, it's Paid
	if outstanding <= 0:
		return "Paid"
	
	# If outstanding equals total, it's Unpaid
	if math.isclose(outstanding, total, rel_tol=1e-2):
		return "Unpaid"
	
	# If outstanding is between 0 and total, it's Partly Paid
	if 0 < outstanding < total:
		return "Partly Paid"
	
	# Check if it's overdue
	if due_date:
		try:
			due = datetime.strptime(str(due_date), "%Y-%m-%d").date()
			today = datetime.now().date()
			if due < today and outstanding > 0:
				return "Overdue"
		except:
			pass
	
	return None
