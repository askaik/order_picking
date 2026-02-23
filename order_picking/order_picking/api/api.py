import frappe
from frappe import _, msgprint

@frappe.whitelist()
def get_invoice_items(scan_input):
	"""
	Fetch items from a Sales Invoice given its standard name or WooCommerce po_no.
	If an item has packed items (Product Bundle), fetch those instead of the parent.
	"""
	# Find invoice by name or po_no
	invoice = frappe.get_all(
		"Sales Invoice",
		filters={"docstatus": 1, "name": scan_input},
		limit=1
	)
	
	if not invoice:
		invoice = frappe.get_all(
			"Sales Invoice",
			filters={"docstatus": 1, "po_no": scan_input},
			limit=1
		)

	if not invoice:
		frappe.throw(_("Sales Invoice not found for: {0}").format(scan_input))

	invoice_doc = frappe.get_doc("Sales Invoice", invoice[0].name)
	
	items_to_pick = {}

	# Helper to accurately aggregate quantities
	def add_to_pick_list(item_code, qty):
		if item_code in items_to_pick:
			items_to_pick[item_code] += qty
		else:
			items_to_pick[item_code] = qty

	for item in invoice_doc.items:
		# Check if this item is a product bundle (has packed items)
		packed_items = frappe.get_all(
			"Packed Item",
			filters={"parent": invoice_doc.name, "parent_item": item.item_code},
			fields=["item_code", "qty"]
		)
		
		if packed_items:
			# It's a bundle, fetch packed items
			for p_item in packed_items:
				add_to_pick_list(p_item.item_code, p_item.qty)
		else:
			# Not a bundle, regular item
			add_to_pick_list(item.item_code, item.qty)

	# Format response
	return {
		"invoice_name": invoice_doc.name,
		"po_no": invoice_doc.po_no,
		"items": [{"item_code": k, "qty": v} for k, v in items_to_pick.items()]
	}

@frappe.whitelist()
def get_active_order_pick():
	"""
	Returns the current Draft Order Pick session for the user, or creates one.
	"""
	active_picks = frappe.get_all("Order Pick", filters={"docstatus": 0, "owner": frappe.session.user}, limit=1)
	if active_picks:
		return active_picks[0].name
	else:
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
	doc = frappe.get_doc("Order Pick", order_pick_id)
	doc.submit()
	return True

