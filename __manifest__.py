# Copyright 2024 Huri Money
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Jibble Connector",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "category": "Human Resources",
    "author": "Huri Money",
    "website": "https://github.com/OCA/hr",
    "summary": "Synchronization between Jibble and Odoo HR Attendance",
    "depends": [
        "hr",
        "hr_attendance",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/ir_cron_data.xml",
        "views/hr_employee_views.xml",
        "views/jibble_sync_log_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "external_dependencies": {
        "python": ["requests"],
    },
    "installable": True,
    "auto_install": False,
    "application": False,
}