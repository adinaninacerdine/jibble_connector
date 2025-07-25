# Copyright 2024 Huri Money
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    jibble_entry_id = fields.Char(
        string="Jibble Entry ID",
        help="Unique identifier from Jibble",
        index=True,
        groups="hr.group_hr_user",
    )
    jibble_activity = fields.Char(
        string="Jibble Activity",
        help="Activity name from Jibble",
        groups="hr.group_hr_user",
    )
    jibble_project = fields.Char(
        string="Jibble Project",
        help="Project name from Jibble",
        groups="hr.group_hr_user",
    )
    jibble_location = fields.Char(
        string="Jibble Location",
        help="Location information from Jibble",
        groups="hr.group_hr_user",
    )
    sync_status = fields.Selection(
        [
            ("synced", "Synchronized"),
            ("pending", "Pending"),
            ("error", "Error"),
        ],
        default="synced",
        help="Synchronization status with Jibble",
        groups="hr.group_hr_user",
    )
    sync_error_message = fields.Text(
        string="Sync Error Message",
        help="Error message if synchronization failed",
        groups="base.group_system",
    )