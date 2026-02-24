import frappe
from frappe import _, msgprint

@frappe.whitelist()
def get_invoice_items(scan_input):
	"""
	Fetch items from a Sales Invoice given its standard name or WooCommerce po_no.
	If an item has packed items (Product Bundle), fetch those instead of the parent.
	"""
	try:
		# Check standard name first using fast db get
		invoice_name = frappe.db.get_value("Sales Invoice", {"name": scan_input}, "name")
		
		# Check po_no if standard name fails
		if not invoice_name:
			invoice_name = frappe.db.get_value("Sales Invoice", {"po_no": scan_input}, "name")
			
		if not invoice_name:
			return {"error": f"Sales Invoice not found for: {scan_input}"}

		invoice_doc = frappe.get_doc("Sales Invoice", invoice_name)
		
		# Prevent scanning if already picked and ready
		if getattr(invoice_doc, "custom_ready_to_dispatch", 0) == 1:
			return {"error": f"Sales Invoice {invoice_name} has already been marked as picked!"}

		items_to_pick = {}

		# Safe extraction of packed items
		packed_items = invoice_doc.get("packed_items") or []
		bundle_parent_items = set([getattr(p, "parent_item", "") for p in packed_items if getattr(p, "parent_item", "")])

		# Safe extraction of normal items
		for item in invoice_doc.get("items") or []:
			i_code = getattr(item, "item_code", None) or getattr(item, "item_name", "Unknown")
			barcode = getattr(item, "barcode", "")
			if not barcode and i_code:
				barcode = frappe.db.get_value("Item Barcode", {"parent": i_code}, "barcode") or ""
				
			if i_code not in bundle_parent_items:
				if i_code not in items_to_pick:
					items_to_pick[i_code] = {"qty": 0, "barcode": barcode}
				items_to_pick[i_code]["qty"] += getattr(item, "qty", 0)
				if barcode and not items_to_pick[i_code]["barcode"]:
					items_to_pick[i_code]["barcode"] = barcode

		# Include packed items safely
		for p_item in packed_items:
			p_code = getattr(p_item, "item_code", None) or getattr(p_item, "item_name", "Unknown")
			if p_code not in items_to_pick:
				items_to_pick[p_code] = {"qty": 0, "barcode": frappe.db.get_value("Item Barcode", {"parent": p_code}, "barcode") or ""}
			items_to_pick[p_code]["qty"] += getattr(p_item, "qty", 0)

		# Format response
		return {
			"invoice_name": invoice_doc.name,
			"po_no": getattr(invoice_doc, "po_no", ""),
			"items": [{"item_code": k, "qty": v["qty"], "barcode": v["barcode"]} for k, v in items_to_pick.items() if v["qty"] > 0]
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"Order Picking Error: {scan_input}")
		return {"error": f"Backend Error: {str(e)}"}

@frappe.whitelist()
def get_active_order_pick(force_new=0):
	"""
	Returns the current Draft Order Pick session for the user, or creates one.
	"""
	if not int(force_new):
		active_picks = frappe.get_all("Order Pick", filters={"docstatus": 0, "owner": frappe.session.user}, limit=1)
		if active_picks:
			return active_picks[0].name

	new_pick = frappe.new_doc("Order Pick")
	new_pick = frappe.new_doc("Order Pick")
	new_pick.picking_date = frappe.utils.now()
	new_pick.picked_by = frappe.session.user
	new_pick.insert(ignore_permissions=True)
	return new_pick.name

@frappe.whitelist()
def mark_invoice_as_ready(invoice_name, order_pick_id=None):
	"""
	Check the 'custom_ready_to_dispatch' field on the submitted invoice.
	If order_pick_id is provided, also attach the invoice to the Order Pick session.
	"""
	if not frappe.db.exists("Sales Invoice", invoice_name):
		frappe.throw(_("Sales Invoice {0} not found").format(invoice_name))

	# Update the field specifically on the database to bypass submit restrictions
	frappe.db.set_value("Sales Invoice", invoice_name, "custom_ready_to_dispatch", 1)
	
	# Attach to the active session
	if order_pick_id:
		order_pick = frappe.get_doc("Order Pick", order_pick_id)
		# Ensure it's not already added
		exists = next((i for i in order_pick.invoices if i.sales_invoice == invoice_name), None)
		if not exists:
			order_pick.append("invoices", {
				"sales_invoice": invoice_name
			})
			order_pick.save(ignore_permissions=True)

	# Add a comment to the timeline for visibility
	invoice_doc = frappe.get_doc("Sales Invoice", invoice_name)
	invoice_doc.add_comment("Info", _("Order fully picked and marked as Ready to Dispatch via Order Picking App."))

	return True

@frappe.whitelist()
def submit_order_pick(order_pick_id):
	"""
	Submits the Order Pick session. The document's on_submit logic will
	create the Dispatch Order draft automatically.
	"""
	try:
		doc = frappe.get_doc("Order Pick", order_pick_id)
		doc.flags.ignore_permissions = True
		doc.submit()
		return {"status": "success"}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Order Pick Submit Error")
		frappe.throw(f"Submission failed: {str(e)}")

