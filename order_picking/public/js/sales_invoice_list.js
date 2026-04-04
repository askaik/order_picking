frappe.listview_settings['Sales Invoice'] = {
	get_indicator: function (doc) {
		if (doc.status === "Paid") {
			return [__("Paid"), "green", "status,=,Paid"];
		} else if (doc.status === "Partly Paid") {
			return [__("Partly Paid"), "orange", "status,=,Partly Paid"];
		} else if (doc.status === "Overdue") {
			return [__("Overdue"), "red", "status,=,Overdue"];
		} else if (doc.status === "Unpaid") {
			return [__("Unpaid"), "orange", "status,=,Unpaid"];
		} else if (doc.status === "Submitted") {
			return [__("Submitted"), "blue", "status,=,Submitted"];
		} else {
			return [__(doc.status), frappe.utils.get_indicator_color(doc.status), "status,=," + doc.status];
		}
	}
};
