from gui.admin_dashboard import (
    InventoryAdmin,
    AccountAdmin
)
from gui.manager_dashboard import *
from gui.technician_dashboard import *


admin_access_list = {
    'Home': 'Full',
    # 'Inventory': 'Inventory (View, Add/Edit, Stock Logs)',
    'Inventory': InventoryAdmin,
    'Request': '(Request Item, Approve Requests)',
    'Purchase Orders': 'Create/Track',
    'Suppliers': 'Manage',
    'Reports': 'Generate',
    'User Management': 'Full',
    'Settings': 'Full',
    'Help': '---',
    'Account': AccountAdmin,
}

manager_access_list = {
    'Home': 'Full',
    'Inventory': 'Inventory (View, Stock Logs, Optional Override)',
    'Request': '(Approve Requests)',
    'Purchase Orders': 'Approve PO',
    'Suppliers': 'View/Edit',
    'Reports': 'Full',
    'User Management': 'Full',
    'Settings': 'Full',
    'Help': '---'
}

technician_access_list = {
    'Home': 'View Summary',
    'Inventory': 'Inventory (View)',
    'Request': '(Request Item)',
    'Purchase Orders': 'NONE',
    'Suppliers': 'NONE',
    'Reports': 'NONE',
    'User Management': 'NONE',
    'Settings': 'NONE',
    'Help': '---'
}