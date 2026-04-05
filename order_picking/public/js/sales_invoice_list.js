// Ensure the status field is fetched so the list view shows payment status
// (Paid, Unpaid, Overdue, Credit Note Issued, etc.) instead of docstatus (Submitted/Draft).
frappe.listview_settings['Sales Invoice'] = frappe.listview_settings['Sales Invoice'] || {};

if (!frappe.listview_settings['Sales Invoice'].add_fields) {
	frappe.listview_settings['Sales Invoice'].add_fields = [];
}
["status", "outstanding_amount", "due_date", "is_return"].forEach(f => {
	if (!frappe.listview_settings['Sales Invoice'].add_fields.includes(f)) {
		frappe.listview_settings['Sales Invoice'].add_fields.push(f);
	}
});
