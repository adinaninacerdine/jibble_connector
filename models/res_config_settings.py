# Copyright 2024 Huri Money
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    jibble_sync_enabled = fields.Boolean(
        string="Enable Jibble Synchronization",
        config_parameter="jibble_connector.sync_enabled",
        help="Enable automatic synchronization with Jibble",
    )
    jibble_api_key = fields.Char(
        string="Jibble API Key",
        config_parameter="jibble_connector.api_key",
        help="API key for Jibble integration",
    )
    jibble_organization_id = fields.Char(
        string="Jibble Organization ID",
        config_parameter="jibble_connector.organization_id",
        help="Organization ID in Jibble",
    )
    jibble_webhook_secret = fields.Char(
        string="Webhook Secret",
        config_parameter="jibble_connector.webhook_secret",
        help="Secret key for webhook validation",
    )
    jibble_sync_interval = fields.Integer(
        string="Sync Interval (minutes)",
        default=15,
        config_parameter="jibble_connector.sync_interval",
        help="Interval in minutes for automatic synchronization",
    )
    jibble_create_timesheet = fields.Boolean(
        string="Create Timesheet Entries",
        config_parameter="jibble_connector.create_timesheet",
        help="Automatically create timesheet entries from attendance",
    )
    jibble_api_secret = fields.Char(
        string="Jibble API Secret",
        config_parameter="jibble_connector.api_secret",
        help="API secret for Jibble integration",
    )
    
    def test_jibble_connection(self):
        """Test connection to Jibble API"""
        api_service = self.env["jibble.api"]
        result = api_service.test_connection()
        
        if result["success"]:
            message = result["message"]
            if "data" in result:
                message += f"\n\nData preview: {str(result['data'])[:200]}..."
            
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Connection Test",
                    "message": message,
                    "type": "success",
                },
            }
        else:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Connection Test Failed",
                    "message": result["message"],
                    "type": "danger",
                },
            }
    
    def discover_jibble_organization(self):
        """Discover organization ID automatically"""
        api_service = self.env["jibble.api"]
        result = api_service.discover_organization()
        
        if result["success"]:
            data = result["data"]
            message = f"Organization data found!\n\nURL: {result['url']}\nData: {str(data)[:300]}..."
            
            # Try to extract organization ID if present
            org_id = None
            if isinstance(data, dict):
                org_id = data.get("organizationId") or data.get("organization", {}).get("id")
            elif isinstance(data, list) and data:
                org_id = data[0].get("id") if "id" in data[0] else None
                
            if org_id:
                message += f"\n\nFound Organization ID: {org_id}\n(Copy this to Organization ID field)"
            
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Organization Discovery",
                    "message": message,
                    "type": "success",
                },
            }
        else:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Discovery Failed",
                    "message": result["message"],
                    "type": "warning",
                },
            }
    
    def debug_jibble_api(self):
        """Advanced debugging of Jibble API"""
        api_service = self.env["jibble.api"]
        result = api_service.debug_api_detailed()
        
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "API Debug Results",
                "message": result["message"],
                "type": "info",
            },
        }