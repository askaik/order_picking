frappe.listview_settings['Sales Invoice'] = frappe.listview_settings['Sales Invoice'] || {};

frappe.listview_settings['Sales Invoice'].get_indicator = function (doc) {
	// Native-accurate color mapping with user requirements
	const status_colors = {
		"Paid": "green",
		"Partly Paid": "yellow",
		"Overdue": "red",
		"Unpaid": "orange",
		"Submitted": "blue",
		"Draft": "red",
		"Cancelled": "red",
		"Credit Note": "gray",
		"Credit Note Issued": "gray",
		"Return": "gray"
	};

	if (doc.status && status_colors[doc.status]) {
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	}

	// Fallback to standard ERPNext indicator logic
	const fallback = frappe.utils.get_indicator && frappe.utils.get_indicator(doc, "Sales Invoice");
	return fallback || [__(doc.status || ""), "gray", "status,=," + (doc.status || "")];
};

// Ensure critical fields are always fetched for the status calculation
if (!frappe.listview_settings['Sales Invoice'].add_fields) {
	frappe.listview_settings['Sales Invoice'].add_fields = [];
}
["customer", "outstanding_amount", "grand_total", "status", "docstatus"].forEach(f => {
	if (!frappe.listview_settings['Sales Invoice'].add_fields.includes(f)) {
		frappe.listview_settings['Sales Invoice'].add_fields.push(f);
	}
});
