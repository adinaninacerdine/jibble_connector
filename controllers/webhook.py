# Copyright 2024 Huri Money
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import hashlib
import hmac
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class JibbleWebhook(http.Controller):
    @http.route(
        "/jibble/webhook",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def handle_webhook(self, **kwargs):
        """Endpoint to receive Jibble webhooks"""
        try:
            # Verify webhook signature
            if not self._verify_webhook_signature(request):
                _logger.warning("Invalid webhook signature received")
                return {"status": "error", "message": "Invalid signature"}

            # Get webhook data
            data = json.loads(request.httprequest.data)
            event_type = data.get("eventType")

            _logger.info(f"Received Jibble webhook: {event_type}")

            # Process based on event type
            if event_type == "timeEntry.created":
                self._handle_time_entry_created(data["payload"])
            elif event_type == "timeEntry.updated":
                self._handle_time_entry_updated(data["payload"])
            elif event_type == "timeEntry.deleted":
                self._handle_time_entry_deleted(data["payload"])
            else:
                _logger.info(f"Unhandled event type: {event_type}")

            return {"status": "success"}

        except Exception as e:
            _logger.error(f"Error processing Jibble webhook: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _verify_webhook_signature(self, request):
        """Verify webhook signature"""
        webhook_secret = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("jibble_connector.webhook_secret")
        )

        signature = request.httprequest.headers.get("X-Jibble-Signature")
        if not signature or not webhook_secret:
            return False

        payload = request.httprequest.data
        expected_signature = hmac.new(
            webhook_secret.encode("utf-8"), payload, hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    def _handle_time_entry_created(self, payload):
        """Handle time entry creation"""
        request.env["jibble.sync.log"].sudo().create(
            {
                "sync_type": "webhook",
                "status": "success",
                "jibble_entry_id": payload.get("id"),
                "message": f"Time entry created: {payload.get('id')}",
                "technical_details": json.dumps(payload),
            }
        )

    def _handle_time_entry_updated(self, payload):
        """Handle time entry update"""
        request.env["jibble.sync.log"].sudo().create(
            {
                "sync_type": "webhook",
                "status": "success",
                "jibble_entry_id": payload.get("id"),
                "message": f"Time entry updated: {payload.get('id')}",
                "technical_details": json.dumps(payload),
            }
        )

    def _handle_time_entry_deleted(self, payload):
        """Handle time entry deletion"""
        request.env["jibble.sync.log"].sudo().create(
            {
                "sync_type": "webhook",
                "status": "warning",
                "jibble_entry_id": payload.get("id"),
                "message": f"Time entry deleted: {payload.get('id')}",
                "technical_details": json.dumps(payload),
            }
        )