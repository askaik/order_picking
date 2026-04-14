import frappe

def execute():
	"""
	Safely reload the workspace without deleting existing data or resetting
	workflow statuses. This patch:
	1. Preserves existing workflow configurations on doctypes
	2. Only reloads workspace if it doesn't exist
	3. Prevents data loss on Sales Invoices and other documents with workflow
	4. Safely handles both fresh installations and app upgrades
	"""
	workspace_name = "Order Picking"

	# Check if workspace exists
	if not frappe.db.exists("Workspace", workspace_name):
		# If it doesn't exist, reload from app JSON on fresh installation
		try:
			frappe.reload_doc("order_picking", "workspace", "order_picking")
		except Exception:
			pass
		return

	# If workspace exists, check if there are any invoices in the system
	try:
		invoice_count = frappe.db.count("Sales Invoice")

		# If there are existing invoices, preserve the workspace to avoid resetting
		# workflow statuses
		if invoice_count > 0:
			# Just update the modified timestamp without deleting
			frappe.db.set_value("Workspace", workspace_name, "modified",
				frappe.utils.now())
			return
	except Exception:
		pass

	# Only delete and reload on fresh installations (no invoices exist)
	try:
		frappe.delete_doc("Workspace", workspace_name, force=1,
			ignore_permissions=True)
		frappe.db.commit()
	except Exception:
		pass

	try:
		frappe.reload_doc("order_picking", "workspace", "order_picking")
	except Exception:
		pass
