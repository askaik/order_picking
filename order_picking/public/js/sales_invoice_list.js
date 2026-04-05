frappe.listview_settings['Sales Invoice'] = frappe.listview_settings['Sales Invoice'] || {};

// Ensure status-related fields are fetched in the list query
frappe.listview_settings['Sales Invoice'].add_fields = [
	"status", "outstanding_amount", "due_date", "is_return",
	"grand_total", "currency", "company", "docstatus"
];

// Explicit indicator mapping — mirrors native ERPNext colors exactly,
// but guarantees correct display even if the native handler is missing.
frappe.listview_settings['Sales Invoice'].get_indicator = function (doc) {
	if (doc.is_return) {
		return [__("Return"), "gray", "is_return,=,1"];
	}
	const map = {
		"Draft":              ["Draft",              "red",    "status,=,Draft"],
		"Unpaid":             ["Unpaid",             "orange", "status,=,Unpaid"],
		"Partly Paid":        ["Partly Paid",        "yellow", "status,=,Partly Paid"],
		"Paid":               ["Paid",               "green",  "status,=,Paid"],
		"Overdue":            ["Overdue",            "red",    "status,=,Overdue"],
		"Partly Paid and Overdue": ["Partly Paid",   "red",    "status,=,Partly Paid and Overdue"],
		"Credit Note Issued": ["Credit Note Issued", "gray",   "status,=,Credit Note Issued"],
		"Return":             ["Return",             "gray",   "status,=,Return"],
		"Cancelled":          ["Cancelled",          "red",    "status,=,Cancelled"],
		"Internal Transfer":  ["Internal Transfer",  "darkgrey", "status,=,Internal Transfer"],
	};
	const entry = doc.status && map[doc.status];
	if (entry) return entry;
	// Fallback: use docstatus if status field wasn't fetched
	if (doc.docstatus === 0) return [__("Draft"),      "red",   "docstatus,=,0"];
	if (doc.docstatus === 1) return [__("Submitted"),  "blue",  "docstatus,=,1"];
	if (doc.docstatus === 2) return [__("Cancelled"),  "red",   "docstatus,=,2"];
	return [__(""), "gray", ""];
};
