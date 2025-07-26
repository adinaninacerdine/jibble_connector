# Copyright 2024 Huri Money
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class JibbleSyncWizard(models.TransientModel):
    _name = "jibble.sync.wizard"
    _description = "Jibble Synchronization Wizard"

    from_date = fields.Date(
        string="From Date",
        default=lambda self: fields.Date.today() - timedelta(days=7),
        help="Start date for synchronization",
    )
    to_date = fields.Date(
        string="To Date",
        default=fields.Date.today,
        help="End date for synchronization",
    )

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

        try:
            # Perform automatic sync for last 24 hours
            from_date = datetime.now() - timedelta(days=1)
            to_date = datetime.now()
            
            result = self._sync_time_entries(
                from_date.strftime("%Y-%m-%d"),
                to_date.strftime("%Y-%m-%d")
            )
            
            # Create log entry for cron sync
            self.env["jibble.sync.log"].create(
                {
                    "sync_type": "cron",
                    "status": "success",
                    "message": f"Cron synchronization completed - {result['synced']} entries synced",
                    "technical_details": f"Synced from {from_date} to {to_date}",
                }
            )
            
        except Exception as e:
            _logger.error(f"Cron sync failed: {str(e)}")
            self.env["jibble.sync.log"].create(
                {
                    "sync_type": "cron",
                    "status": "error",
                    "message": f"Cron synchronization failed: {str(e)}",
                    "technical_details": str(e),
                }
            )

    def manual_sync_jibble(self):
        """Manual synchronization trigger"""
        try:
            result = self._sync_time_entries(
                self.from_date.strftime("%Y-%m-%d"),
                self.to_date.strftime("%Y-%m-%d")
            )
            
            # Create log entry for manual sync
            self.env["jibble.sync.log"].create(
                {
                    "sync_type": "manual",
                    "status": "success",
                    "message": f"Manual synchronization completed - {result['synced']} entries synced",
                    "technical_details": f"Synced from {self.from_date} to {self.to_date}",
                }
            )

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Synchronization Complete",
                    "message": f"Successfully synced {result['synced']} time entries",
                    "type": "success",
                },
            }
            
        except Exception as e:
            _logger.error(f"Manual sync failed: {str(e)}")
            self.env["jibble.sync.log"].create(
                {
                    "sync_type": "manual",
                    "status": "error",
                    "message": f"Manual synchronization failed: {str(e)}",
                    "technical_details": str(e),
                }
            )
            
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Synchronization Failed",
                    "message": str(e),
                    "type": "danger",
                },
            }

    def _sync_time_entries(self, from_date, to_date):
        """Sync time entries from Jibble API"""
        api_service = self.env["jibble.api"]
        synced_count = 0
        errors = []

        try:
            # Get time entries from Jibble
            time_entries = api_service.get_time_entries(from_date, to_date)
            
            if not time_entries:
                return {"synced": 0, "errors": ["No time entries found"]}

            for entry in time_entries.get("data", []):
                try:
                    self._process_time_entry(entry)
                    synced_count += 1
                except Exception as e:
                    error_msg = f"Error processing entry {entry.get('id')}: {str(e)}"
                    _logger.error(error_msg)
                    errors.append(error_msg)

            return {"synced": synced_count, "errors": errors}

        except Exception as e:
            raise UserError(f"Failed to sync time entries: {str(e)}")

    def _process_time_entry(self, entry):
        """Process a single time entry from Jibble"""
        # Find employee by Jibble User ID
        employee = self.env["hr.employee"].search([
            ("jibble_user_id", "=", entry.get("personId")),
            ("jibble_sync_enabled", "=", True)
        ], limit=1)

        if not employee:
            _logger.warning(f"No employee found for Jibble user ID: {entry.get('personId')}")
            return

        # Check if entry already exists
        existing_attendance = self.env["hr.attendance"].search([
            ("jibble_entry_id", "=", entry.get("id"))
        ], limit=1)

        if existing_attendance:
            # Update existing attendance
            self._update_attendance(existing_attendance, entry)
        else:
            # Create new attendance
            self._create_attendance(employee, entry)

    def _create_attendance(self, employee, entry):
        """Create new attendance record from Jibble entry"""
        check_in = self._parse_jibble_datetime(entry.get("start"))
        check_out = self._parse_jibble_datetime(entry.get("end")) if entry.get("end") else None

        attendance_vals = {
            "employee_id": employee.id,
            "check_in": check_in,
            "check_out": check_out,
            "jibble_entry_id": entry.get("id"),
            "jibble_activity": entry.get("activity", {}).get("name"),
            "jibble_project": entry.get("project", {}).get("name"),
            "jibble_location": entry.get("location", {}).get("name"),
            "sync_status": "synced",
        }

        attendance = self.env["hr.attendance"].create(attendance_vals)
        
        # Create timesheet if enabled
        create_timesheet = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("jibble_connector.create_timesheet", False)
        )
        
        if create_timesheet and check_in and check_out:
            self._create_timesheet_entry(employee, attendance, entry)

    def _update_attendance(self, attendance, entry):
        """Update existing attendance record"""
        check_in = self._parse_jibble_datetime(entry.get("start"))
        check_out = self._parse_jibble_datetime(entry.get("end")) if entry.get("end") else None

        attendance.write({
            "check_in": check_in,
            "check_out": check_out,
            "jibble_activity": entry.get("activity", {}).get("name"),
            "jibble_project": entry.get("project", {}).get("name"),
            "jibble_location": entry.get("location", {}).get("name"),
            "sync_status": "synced",
        })

    def _create_timesheet_entry(self, employee, attendance, entry):
        """Create timesheet entry from attendance"""
        if not hasattr(self.env, "account.analytic.line"):
            return  # Timesheet module not installed

        # Calculate duration in hours
        duration = (attendance.check_out - attendance.check_in).total_seconds() / 3600

        timesheet_vals = {
            "employee_id": employee.id,
            "date": attendance.check_in.date(),
            "name": entry.get("activity", {}).get("name") or "Time tracking from Jibble",
            "unit_amount": duration,
            "project_id": None,  # Could be mapped from Jibble project
        }

        try:
            self.env["account.analytic.line"].create(timesheet_vals)
        except Exception as e:
            _logger.warning(f"Failed to create timesheet entry: {str(e)}")

    def _parse_jibble_datetime(self, datetime_str):
        """Parse Jibble datetime string to Odoo datetime"""
        if not datetime_str:
            return None
        
        try:
            # Jibble uses ISO format: 2024-07-26T08:00:00.000Z
            if datetime_str.endswith("Z"):
                datetime_str = datetime_str[:-1] + "+00:00"
            
            dt = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
            return dt.replace(tzinfo=None)  # Odoo expects naive datetime
        except ValueError as e:
            _logger.error(f"Failed to parse datetime {datetime_str}: {str(e)}")
            return None