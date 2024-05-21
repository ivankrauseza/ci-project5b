import xml.etree.ElementTree as ET
from datetime import datetime


def log_transaction(transaction):
    log_entry = ET.Element('transaction')
    user = ET.SubElement(log_entry, 'user')
    user.text = transaction.user.username
    product = ET.SubElement(log_entry, 'product')
    product.text = transaction.product.name
    quantity = ET.SubElement(log_entry, 'quantity')
    quantity.text = str(transaction.quantity)
    type_ = ET.SubElement(log_entry, 'type')
    type_.text = transaction.get_type_display()
    date_added = ET.SubElement(log_entry, 'date_added')
    date_added.text = transaction.date_added.isoformat()

    tree = ET.ElementTree(log_entry)
    log_filename = f'transaction_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xml'

    with open(log_filename, 'wb') as f:
        tree.write(f)
