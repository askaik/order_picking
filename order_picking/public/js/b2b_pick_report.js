frappe.ui.form.on('B2B Pick Report', {
	refresh(frm) {
		frm.add_custom_button(__('Print Summary'), () => {
			frm.call_button_print_summary();
		}, __('Print'));

		// Also add as a primary button for quick access
		frm.page.set_secondary_action(__('Print Summary'), () => {
			frm.call_button_print_summary();
		});
	}
});

// Attach the print function to the form instance
frappe.ui.form.on('B2B Pick Report', {
	onload(frm) {
		frm.call_button_print_summary = async function () {
			const doc = frm.doc;
			const item_codes = (doc.items || []).map(i => i.item_code);

			// Fetch barcodes for all items
			let barcodeMap = {};
			if (item_codes.length) {
				const res = await frappe.call({
					method: 'order_picking.api.api.get_item_barcodes',
					args: { item_codes: JSON.stringify(item_codes) }
				});
				barcodeMap = res.message || {};
			}

			const td = (content, style) =>
				`<td style="padding:6px 10px;border:1px solid #ddd;font-size:12px;${style||''}">${content}</td>`;

			const rows = (doc.items || []).map((item, idx) => {
				const over = item.picked_qty > item.order_qty && item.order_qty > 0;
				const barcodes = (barcodeMap[item.item_code] || []).join(', ');
				const skuCell = item.item_code + (barcodes
					? `<br><span style="font-weight:normal;font-size:10px;color:#888;font-family:monospace">${barcodes}</span>`
					: '');
				return `<tr>
					${td(idx + 1, 'color:#999')}
					${td(`<strong>${skuCell}</strong>`)}
					${td(item.item_name || '')}
					${td(item.order_qty, 'text-align:right')}
					${td(item.picked_qty + (over ? ' &#9888;' : ''), `text-align:right;font-weight:bold;color:${over ? '#dc2626' : '#16a34a'}`)}
					${td(item.uom || 'Nos')}
					${td(item.source_warehouse || '', 'font-size:11px;color:#888')}
					${td(item.target_warehouse || '', 'font-size:11px;color:#888')}
				</tr>`;
			}).join('');

			const logRows = (doc.log || []).map((log, idx) =>
				`<tr>
					<td style="padding:4px 8px;border:1px solid #eee;font-size:11px;color:#999">${idx + 1}</td>
					<td style="padding:4px 8px;border:1px solid #eee;font-size:11px">${log.time || ''}</td>
					<td style="padding:4px 8px;border:1px solid #eee;font-size:11px;font-weight:bold">${log.item_code || ''}</td>
					<td style="padding:4px 8px;border:1px solid #eee;font-size:11px;font-family:monospace">${log.barcode || ''}</td>
					<td style="padding:4px 8px;border:1px solid #eee;font-size:11px;text-align:right;font-weight:bold">${log.qty || 0}</td>
					<td style="padding:4px 8px;border:1px solid #eee;font-size:11px">&times;${log.multiplier || ''} (${log.uom_factor || ''})</td>
				</tr>`
			).join('');

			const badge = (text, bg, color) =>
				`<span style="display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:bold;margin-right:6px;background:${bg};color:${color}">${text}</span>`;

			const html = `<html><head><title>B2B Pick Summary — ${doc.sales_order || doc.name}</title>
<style>
  body{font-family:system-ui,sans-serif;padding:30px;color:#333}
  h1{margin:0 0 6px;font-size:20px}
  h3{margin:24px 0 8px;font-size:13px;text-transform:uppercase;color:#555}
  table{border-collapse:collapse;width:100%}
  th{background:#f3f4f6;text-align:left;padding:8px 10px;border:1px solid #ddd;font-size:11px;text-transform:uppercase}
  .meta{color:#666;font-size:12px;margin:0 0 4px}
  .sub{color:#999;font-size:11px;margin:0 0 20px}
  hr{border:none;border-top:1px dashed #ddd;margin:20px 0}
</style>
</head><body>
<h1>B2B Order Pick &mdash; Completion Summary</h1>
<p class="meta"><strong>Sales Order:</strong> ${doc.sales_order || '&mdash;'} &nbsp; <strong>Customer:</strong> ${doc.customer_name || '&mdash;'}</p>
<p class="meta">
  ${badge('MR: ' + (doc.material_request || '&mdash;'), '#fef3c7', '#92400e')}
  ${badge('SE: ' + (doc.stock_entry || '&mdash;'), '#d1fae5', '#065f46')}
  ${doc.is_partial ? badge('Partial Pick', '#fde8d8', '#9a3412') : badge('Fully Picked', '#d1fae5', '#065f46')}
</p>
<p class="meta"><strong>Picked By:</strong> ${doc.picked_by || '&mdash;'} &nbsp; <strong>Pick Date:</strong> ${doc.pick_date || '&mdash;'}</p>
<p class="sub">Printed: ${new Date().toLocaleString()}</p>
<hr>
<h3>Transfer Items</h3>
<table>
  <thead><tr>
    <th>#</th><th>Item Code / Barcode</th><th>Item Name</th>
    <th style="text-align:right">Order Qty</th><th style="text-align:right">Picked Qty</th>
    <th>UOM</th><th>Source WH</th><th>Dest WH</th>
  </tr></thead>
  <tbody>${rows}</tbody>
</table>
${logRows ? `<h3>Scan Log (${(doc.log || []).length} scans)</h3>
<table>
  <thead><tr><th>#</th><th>Time</th><th>Item</th><th>Barcode</th><th style="text-align:right">Qty</th><th>Details</th></tr></thead>
  <tbody>${logRows}</tbody>
</table>` : ''}
</body></html>`;

			const w = window.open('', '_blank');
			w.document.write(html);
			w.document.close();
			w.focus();
			w.print();
		};
	}
});
