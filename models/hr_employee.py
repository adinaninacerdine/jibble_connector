# Copyright 2024 Huri Money
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    jibble_user_id = fields.Char(
        string="Jibble User ID",
        help="Unique identifier of the user in Jibble",
        groups="hr.group_hr_user",
    )
    jibble_email = fields.Char(
        string="Jibble Email",
        help="Email used in Jibble",
        groups="hr.group_hr_user",
    )
    jibble_sync_enabled = fields.Boolean(
        string="Jibble Synchronization",
        default=True,
        help="Enable automatic synchronization with Jibble",
        groups="hr.group_hr_user",
    )
    last_jibble_sync = fields.Datetime(
        string="Last Jibble Sync",
        readonly=True,
        help="Last successful synchronization with Jibble",
        groups="hr.group_hr_user",
    )