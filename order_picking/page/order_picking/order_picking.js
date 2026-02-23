frappe.pages['order_picking'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Order Picking',
		single_column: true
	});

	// Initial DOM elements
	$(wrapper).find('.layout-main-section').append(
		frappe.render_template('order_picking', {})
	);

	// App State
	let current_invoice = null;
	let items_to_pick = [];
	let picked_items = [];

	// DOM Selectors
	const $invoice_input = $('#scan_invoice_input');
	const $item_input = $('#scan_item_input');
	const $progress_bar = $('#picking_progress_bar');
	const $progress_text = $('#progress_text');
	const $items_to_pick_list = $('#items_to_pick_list');
	const $picked_items_list = $('#picked_items_list');
	const $ready_btn = $('#mark_ready_btn');

	$item_input.prop('disabled', true); // disabled until invoice is loaded

	// Function to update UI Progress
	function update_progress() {
		let total_items = items_to_pick.reduce((acc, obj) => acc + obj.qty, 0) + picked_items.reduce((acc, obj) => acc + obj.qty, 0);
		let total_picked = picked_items.reduce((acc, obj) => acc + obj.qty, 0);
		
		let percentage = total_items === 0 ? 0 : Math.round((total_picked / total_items) * 100);

		$progress_bar.css('width', percentage + '%');
		$progress_text.text(percentage + '%');

		if(percentage === 100) {
			$progress_bar.removeClass('bg-danger').addClass('bg-success');
			frappe.show_alert({message:__('Order Fully Picked!'), indicator:'green'});
			$item_input.prop('disabled', true);
			$ready_btn.show();
		} else {
			$progress_bar.removeClass('bg-success').addClass('bg-danger');
			$ready_btn.hide();
		}
	}

	// Function to Render Lists
	function render_lists() {
		// Render Items To Pick
		$items_to_pick_list.empty();
		items_to_pick.forEach(item => {
			if (item.qty > 0) {
				$items_to_pick_list.append(`
					<div class="picking-list-item">
						<div class="item-code">${item.item_code}</div>
						<div class="item-qty">${item.qty}</div>
					</div>
				`);
			}
		});

		// Render Picked Items
		$picked_items_list.empty();
		picked_items.forEach(item => {
			$picked_items_list.append(`
				<div class="picking-list-item picked">
					<div class="item-code">${item.item_code}</div>
					<div class="item-qty">${item.qty}</div>
				</div>
			`);
		});

		update_progress();
	}

	// Invoice Scan Event
	$invoice_input.on('keypress', function(e) {
		if(e.which == 13) {
			let scan_val = $(this).val().trim();
			if(!scan_val) return;

			frappe.call({
				method: 'order_picking.order_picking.api.api.get_invoice_items',
				args: {
					scan_input: scan_val
				},
				callback: function(r) {
					if(r.message) {
						current_invoice = r.message.invoice_name;
						items_to_pick = r.message.items; // format: [{item_code: "ART-1", qty: 2}]
						picked_items = [];
						
						frappe.show_alert({message:__(`Loaded invoice ${current_invoice}`), indicator:'green'});
						$invoice_input.val('');
						$item_input.prop('disabled', false).focus();
						render_lists();
					}
				}
			});
		}
	});

	// Item Scan Event
	$item_input.on('keypress', function(e) {
		if(e.which == 13) {
			let scan_val = $(this).val().trim();
			if(!scan_val) return;

			let found_index = items_to_pick.findIndex(i => i.item_code === scan_val || i.barcode === scan_val);

			if(found_index !== -1 && items_to_pick[found_index].qty > 0) {
				// Reduce qty from to_pick
				items_to_pick[found_index].qty--;

				// Add to picked_items
				let picked_index = picked_items.findIndex(i => i.item_code === items_to_pick[found_index].item_code);
				if(picked_index !== -1) {
					picked_items[picked_index].qty++;
				} else {
					picked_items.push({
						item_code: items_to_pick[found_index].item_code,
						qty: 1
					});
				}

				// Flash success visual cue
				$item_input.addClass('flash-success');
				setTimeout(() => $item_input.removeClass('flash-success'), 200);

			} else {
				frappe.show_alert({message:__('Item not found in invoice or already fully picked!'), indicator:'red'});
				frappe.utils.play_sound('error');
			}

			$item_input.val('').focus();
			render_lists();
		}
	});

	// Manual Mark Ready Button 
	$ready_btn.on('click', function() {
		if(current_invoice) {
			frappe.call({
				method: 'order_picking.order_picking.api.api.mark_invoice_as_ready',
				args: {
					invoice_name: current_invoice
				},
				callback: function(r) {
					if(!r.exc) {
						frappe.show_alert({message:__('Invoice marked as Ready to Dispatch!'), indicator:'green'});
						// Reset UI
						current_invoice = null;
						items_to_pick = [];
						picked_items = [];
						render_lists();
						$ready_btn.hide();
						$invoice_input.focus();
					}
				}
			});
		}
	});
};
