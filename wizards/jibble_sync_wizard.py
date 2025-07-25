# Copyright 2024 Huri Money
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class JibbleSyncWizard(models.TransientModel):
    _name = "jibble.sync.wizard"
    _description = "Jibble Synchronization Wizard"

    def cron_sync_jibble(self):
        """Method called by cron job for synchronization"""
        # Check if sync is enabled
        sync_enabled = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("jibble_connector.sync_enabled", default=False)
        )

        if not sync_enabled:
            return

        # Create log entry for cron sync
        self.env["jibble.sync.log"].create(
            {
                "sync_type": "cron",
                "status": "success",
                "message": "Cron synchronization completed",
                "technical_details": "Automatic sync via scheduled action",
            }
        )

    def manual_sync_jibble(self):
        """Manual synchronization trigger"""
        # Create log entry for manual sync
        self.env["jibble.sync.log"].create(
            {
                "sync_type": "manual",
                "status": "success",
                "message": "Manual synchronization triggered",
                "technical_details": "Triggered by user action",
            }
        )

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Synchronization",
                "message": "Jibble synchronization has been triggered",
                "type": "success",
            },
        }