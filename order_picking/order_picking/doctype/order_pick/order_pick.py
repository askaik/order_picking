import frappe
from frappe.model.document import Document
from frappe.utils import now

class OrderPick(Document):
	def on_submit(self):
		if not self.invoices:
			return

		# Create Dispatch Orders entry
		dispatch_doc = frappe.new_doc("Dispatch Orders")
		dispatch_doc.dispatch_date = now()

		# Fetch fields from the Sales Invoices to populate the Dispatch Order List
		for item in self.invoices:
			si = frappe.get_doc("Sales Invoice", item.sales_invoice)
			dispatch_doc.append("table_sruu", {
				"sales_invoice": item.sales_invoice,
				"customer_purchase_order_number": si.po_no,
				"customer_name": si.customer_name,
				"mobile_number": si.contact_mobile or ""
			})
		
		# insert the Dispatch Orders as Draft
		dispatch_doc.insert(ignore_permissions=True)

		# write back the Dispatch Order ID to each invoice in the Order Pick
		for item in self.invoices:
			item.db_set("dispatch_order", dispatch_doc.name)

		# Display a pop-up alert to the operator
		frappe.msgprint(frappe._("Draft Dispatch Order created: {0}").format(
			f"<a href='/app/dispatch-orders/{dispatch_doc.name}'>{dispatch_doc.name}</a>"
		))
