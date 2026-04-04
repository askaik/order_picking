import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_migrate():
	"""
	Run after bench migrate.
	This ensures the custom fields are always present without relying on fixtures.
	"""
	setup_custom_fields()

def setup_custom_fields():
	custom_fields = {
		"Sales Invoice": [
			{
				"fieldname": "custom_ready_to_dispatch",
				"label": "Ready to Dispatch",
				"fieldtype": "Check",
				"insert_after": "status",
				"read_only": 1,
				"in_list_view": 1,
				"in_standard_filter": 1
			},
			{
				"fieldname": "custom_order_ready_to_dispatch",
				"label": "Order Ready to Dispatch",
				"fieldtype": "Check",
				"insert_after": "custom_ready_to_dispatch",
				"read_only": 1,
				"in_list_view": 1,
				"in_standard_filter": 1
			}
		],
		"Sales Order": [
			{
				"fieldname": "custom_b2b_picked",
				"label": "B2B Picked",
				"fieldtype": "Check",
				"insert_after": "status",
				"read_only": 1,
				"in_list_view": 1,
				"in_standard_filter": 1,
				"description": "Checked when order is picked via B2B Order Pick app"
			},
			{
				"fieldname": "custom_b2b_status",
				"label": "B2B Status",
				"fieldtype": "Select",
				"options": "\nConsignment Delivered\nConsignment Partially Delivered",
				"insert_after": "custom_b2b_picked",
				"read_only": 1,
				"in_list_view": 1,
				"in_standard_filter": 1,
				"description": "B2B Order Pick status"
			}
		]
	}
	create_custom_fields(custom_fields, update=True)
