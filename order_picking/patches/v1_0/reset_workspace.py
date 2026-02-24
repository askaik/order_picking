import frappe

def execute():
	"""
	Forcefully delete the existing Workspace to resolve any Custom vs Standard
	database conflicts, and reload from our explicit app JSON.
	"""
	if frappe.db.exists("Workspace", "Order Picking"):
		try:
			frappe.delete_doc("Workspace", "Order Picking", force=1, ignore_permissions=True)
			frappe.db.commit()
		except Exception:
			pass
	
	try:
		frappe.reload_doc("order_picking", "workspace", "order_picking")
	except Exception:
		pass
