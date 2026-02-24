import frappe

def execute():
    # 1. Individual Box Label Print Format
    label_html = """
{% for invoice_name in doc.sales_invoices %}
  {% set invoice = frappe.get_doc("Sales Invoice", invoice_name.sales_invoice) %}
  
  <div class="page-break" style="page-break-after: always; padding: 20px; font-family: sans-serif; border: 2px solid #000; border-radius: 8px; max-width: 4in; min-height: 5in; box-sizing: border-box; margin: 0 auto;">
     <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 15px;">
        <h2 style="margin: 0; font-size: 24px;">BOX SCANNED</h2>
        <p style="margin: 5px 0 0; font-size: 18px; font-weight: bold;">{{ invoice.name }}</p>
     </div>
     
     <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
        <div style="flex: 1; padding-right: 10px;">
           <p style="margin: 0 0 5px; font-size: 14px;"><strong>Customer:</strong><br>{{ invoice.customer }}</p>
           <p style="margin: 0; font-size: 14px;"><strong>Order Pick:</strong><br>{{ doc.name }}</p>
        </div>
        <div style="flex-shrink: 0;">
           <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={{ frappe.utils.get_url_to_form('Order Pick', doc.name) }}" style="width: 80px; height: 80px; border: 1px solid #ccc; padding: 2px;" alt="QR Code" />
        </div>
     </div>
     
     <table style="width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 15px;">
        <thead>
           <tr>
              <th style="border-bottom: 2px solid #000; text-align: left; padding: 5px 2px;">Item Code</th>
              <th style="border-bottom: 2px solid #000; text-align: left; padding: 5px 2px;">Name</th>
              <th style="border-bottom: 2px solid #000; text-align: right; padding: 5px 2px;">Qty</th>
           </tr>
        </thead>
        <tbody>
           {% set total_qty = 0 %}
           {% for item in invoice.items %}
           <tr>
              <td style="border-bottom: 1px solid #eee; padding: 5px 2px; font-weight: bold;">{{ item.item_code }}</td>
              <td style="border-bottom: 1px solid #eee; padding: 5px 2px;">{{ item.item_name }}</td>
              <td style="border-bottom: 1px solid #eee; text-align: right; padding: 5px 2px; font-weight: bold; font-size: 14px;">{{ item.qty }}</td>
           </tr>
           {% set total_qty = total_qty + item.qty %}
           {% endfor %}
        </tbody>
        <tfoot>
           <tr>
              <td colspan="2" style="text-align: right; padding: 10px 5px; font-size: 14px; font-weight: bold;">TOTAL BOX QTY:</td>
              <td style="text-align: right; padding: 10px 5px; font-size: 18px; font-weight: 900;">{{ total_qty }}</td>
           </tr>
        </tfoot>
     </table>
  </div>
{% endfor %}
    """

    if not frappe.db.exists("Print Format", "Order Pick Box Label"):
        pf = frappe.new_doc("Print Format")
        pf.name = "Order Pick Box Label"
        pf.doc_type = "Order Pick"
        pf.custom_format = 1
        pf.print_format_type = "Jinja"
        pf.html = label_html
        pf.insert(ignore_permissions=True)

    # 2. Summary Manifest Print Format
    manifest_html = """
<div style="font-family: sans-serif; padding: 20px;">
   <div style="border-bottom: 2px solid #000; margin-bottom: 20px; padding-bottom: 10px; display: flex; justify-content: space-between;">
      <div>
         <h1 style="margin: 0; font-size: 28px;">Order Pick Manifest</h1>
         <h3 style="margin: 5px 0 0; color: #555;">{{ doc.name }}</h3>
      </div>
      <div style="text-align: right;">
         <p style="margin: 0;"><strong>Date:</strong> {{ frappe.utils.getdate(doc.creation).strftime('%Y-%m-%d') }}</p>
         <p style="margin: 5px 0 0;"><strong>Status:</strong> {{ doc.status }}</p>
      </div>
   </div>

   <h3 style="margin-top: 20px; border-bottom: 1px solid #ddd; padding-bottom: 5px;">Included Invoices</h3>
   <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 30px;">
      <thead>
         <tr style="background-color: #f8f9fa;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Invoice</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Customer</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Total Items</th>
         </tr>
      </thead>
      <tbody>
         {% set grand_total = 0 %}
         {% for row in doc.sales_invoices %}
            {% set inv = frappe.get_doc("Sales Invoice", row.sales_invoice) %}
            {% set inv_total = 0 %}
            {% for item in inv.items %}
               {% set inv_total = inv_total + item.qty %}
            {% endfor %}
         <tr>
            <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">{{ inv.name }}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">{{ inv.customer_name or inv.customer }}</td>
            <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">{{ inv_total }}</td>
         </tr>
         {% set grand_total = grand_total + inv_total %}
         {% endfor %}
      </tbody>
      <tfoot>
         <tr style="background-color: #f1f5f9;">
            <td colspan="2" style="border: 1px solid #ddd; padding: 10px 8px; text-align: right; font-weight: bold;">ROUTING GRAND TOTAL:</td>
            <td style="border: 1px solid #ddd; padding: 10px 8px; text-align: right; font-weight: bold; font-size: 16px;">{{ grand_total }}</td>
         </tr>
      </tfoot>
   </table>
</div>
    """

    if not frappe.db.exists("Print Format", "Order Pick Manifest"):
        pf = frappe.new_doc("Print Format")
        pf.name = "Order Pick Manifest"
        pf.doc_type = "Order Pick"
        pf.custom_format = 1
        pf.print_format_type = "Jinja"
        pf.html = manifest_html
        pf.insert(ignore_permissions=True)

    frappe.db.commit()
