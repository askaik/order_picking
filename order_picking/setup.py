import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_migrate():
	"""
	Run after bench migrate.
	This ensures the custom_ready_to_dispatch field is always present
	in the Sales Invoice doctype without relying on fixtures.
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
			}
		]
	}
	create_custom_fields(custom_fields, update=True)
