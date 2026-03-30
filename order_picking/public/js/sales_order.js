frappe.ui.form.on("Sales Order", {
	refresh: function (frm) {
		// Override the status indicator when B2B status is set
		if (frm.doc.custom_b2b_status === "Consignment Delivered") {
			frm.page.set_indicator("Consignment Delivered", "green");
		}
	}
});
