# Copyright 2024 Huri Money
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class JibbleSyncLog(models.Model):
    _name = "jibble.sync.log"
    _description = "Jibble Synchronization Log"
    _order = "create_date desc"
    _rec_name = "display_name"

    display_name = fields.Char(
        compute="_compute_display_name", 
        store=True
    )
    sync_type = fields.Selection(
        [
            ("webhook", "Webhook"),
            ("cron", "Scheduled Task"),
            ("manual", "Manual"),
        ],
        required=True,
        help="Type of synchronization trigger",
    )
    status = fields.Selection(
        [
            ("success", "Success"),
            ("warning", "Warning"),
            ("error", "Error"),
        ],
        required=True,
        help="Status of the synchronization",
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        help="Related employee",
        groups="hr.group_hr_user",
    )
    jibble_entry_id = fields.Char(
        string="Jibble Entry ID",
        help="ID of the Jibble time entry",
        groups="hr.group_hr_user",
    )
    message = fields.Text(
        string="Message",
        help="Human readable message",
    )
    technical_details = fields.Text(
        string="Technical Details",
        help="Technical information for debugging",
        groups="base.group_system",
    )

    @api.depends("create_date", "sync_type", "status")
    def _compute_display_name(self):
        for record in self:
            if record.create_date:
                date_str = record.create_date.strftime("%Y-%m-%d %H:%M")
                record.display_name = f"{record.sync_type} - {record.status} - {date_str}"
            else:
                record.display_name = f"{record.sync_type} - {record.status}"