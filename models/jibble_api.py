# Copyright 2024 Huri Money
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
import logging
from datetime import datetime, timedelta

import requests

from odoo import api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class JibbleApi(models.AbstractModel):
    _name = "jibble.api"
    _description = "Jibble API Service"

    @api.model
    def _get_api_config(self):
        """Get API configuration from settings"""
        get_param = self.env["ir.config_parameter"].sudo().get_param
        return {
            "api_key": get_param("jibble_connector.api_key"),
            "api_secret": get_param("jibble_connector.api_secret"),
            "organization_id": get_param("jibble_connector.organization_id"),
            "sync_enabled": get_param("jibble_connector.sync_enabled", False),
        }

    @api.model
    def _get_headers(self):
        """Get headers for API requests"""
        config = self._get_api_config()
        if not config["api_key"]:
            raise UserError("Jibble API Key is not configured")
        
        return {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @api.model
    def _make_request(self, method, endpoint, data=None):
        """Make API request to Jibble"""
        config = self._get_api_config()
        if not config["sync_enabled"]:
            _logger.info("Jibble synchronization is disabled")
            return None

        base_url = "https://workspace.prod.jibble.io/v1"
        url = f"{base_url}/{endpoint}"
        headers = self._get_headers()

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            else:
                raise UserError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            _logger.error(f"Jibble API request failed: {str(e)}")
            raise UserError(f"Failed to connect to Jibble API: {str(e)}")

    @api.model
    def get_organization_people(self):
        """Get all people from Jibble organization"""
        config = self._get_api_config()
        if not config["organization_id"]:
            raise UserError("Jibble Organization ID is not configured")
        
        # Try different endpoint formats
        endpoint = "People"  # Simplified endpoint
        return self._make_request("GET", endpoint)

    @api.model
    def get_time_entries(self, from_date=None, to_date=None, person_id=None):
        """Get time entries from Jibble"""
        config = self._get_api_config()
        if not config["organization_id"]:
            raise UserError("Jibble Organization ID is not configured")
        
        # Default to last 7 days if no dates provided
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")

        endpoint = "TimeEntries"
        params = {
            "from": from_date,
            "to": to_date,
        }
        
        if person_id:
            params["personId"] = person_id

        # Add params to endpoint
        param_string = "&".join([f"{k}={v}" for k, v in params.items()])
        endpoint = f"{endpoint}?{param_string}"
        
        return self._make_request("GET", endpoint)

    @api.model
    def test_connection(self):
        """Test connection to Jibble API"""
        config = self._get_api_config()
        api_key = config["api_key"]
        
        if not api_key:
            return {"success": False, "message": "API Key not configured"}
        
        # Test different API configurations based on common patterns
        test_configs = [
            # Standard Bearer token
            {
                "url": "https://api.jibble.io/v1",
                "headers": {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                "endpoints": ["me", "organizations", "people", "users"]
            },
            # Alternative API URLs
            {
                "url": "https://workspace.prod.jibble.io/v1",
                "headers": {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                "endpoints": ["me", "organizations", "people", "users"]
            },
            # X-API-Key header format
            {
                "url": "https://api.jibble.io/v1",
                "headers": {
                    "X-API-Key": api_key,
                    "Content-Type": "application/json"
                },
                "endpoints": ["me", "organizations", "people", "users"]
            },
            # Token without Bearer prefix
            {
                "url": "https://api.jibble.io/v1",
                "headers": {
                    "Authorization": api_key,
                    "Content-Type": "application/json"
                },
                "endpoints": ["me", "organizations", "people", "users"]
            },
            # API Key in query parameter
            {
                "url": "https://api.jibble.io/v1",
                "headers": {
                    "Content-Type": "application/json"
                },
                "endpoints": [f"me?api_key={api_key}", f"organizations?api_key={api_key}"]
            }
        ]
        
        for config_test in test_configs:
            for endpoint in config_test["endpoints"]:
                try:
                    url = f"{config_test['url']}/{endpoint}"
                    response = requests.get(url, headers=config_test["headers"], timeout=10)
                    
                    _logger.info(f"Testing {url} - Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        auth_method = "Bearer" if "Bearer" in str(config_test["headers"]) else "X-API-Key" if "X-API-Key" in str(config_test["headers"]) else "Direct"
                        return {
                            "success": True,
                            "message": f"✅ SUCCESS!\n\nEndpoint: {endpoint}\nURL: {config_test['url']}\nAuth: {auth_method}\n\nUse this configuration!",
                            "data": data[:3] if isinstance(data, list) else data,
                            "config": config_test
                        }
                    elif response.status_code == 401:
                        continue  # Try next config
                    elif response.status_code == 403:
                        return {
                            "success": False,
                            "message": f"Access forbidden for endpoint {endpoint}. Check permissions."
                        }
                        
                except requests.exceptions.RequestException as e:
                    _logger.debug(f"Failed {url}: {str(e)}")
                    continue
        
        return {
            "success": False,
            "message": "❌ Authentication failed with all tested configurations.\n\nTested:\n- Bearer token auth\n- X-API-Key header\n- Query parameter\n- Multiple URLs\n\nPlease verify:\n1. Your API key is correct\n2. API key has proper permissions\n3. Check Jibble documentation for changes"
        }
    
    @api.model  
    def discover_organization(self):
        """Try to discover organization ID automatically"""
        config = self._get_api_config()
        api_key = config["api_key"]
        
        if not api_key:
            return {"success": False, "message": "API Key not configured"}
            
        # Try to get user info first
        test_urls = [
            "https://workspace.prod.jibble.io/v1/me",
            "https://api.jibble.io/v1/me",
            "https://workspace.prod.jibble.io/v1/Organizations"
        ]
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        for url in test_urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return {"success": True, "data": data, "url": url}
            except:
                continue
                
        return {"success": False, "message": "Could not discover organization"}
    
    @api.model
    def debug_api_detailed(self):
        """Detailed debugging of API calls with full response info"""
        config = self._get_api_config()
        api_key = config["api_key"]
        
        if not api_key:
            return {"message": "❌ No API Key configured"}
        
        debug_info = []
        debug_info.append(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]} (masked)")
        debug_info.append(f"📏 Key Length: {len(api_key)} characters")
        debug_info.append(f"🔤 Key Format: {'UUID-like' if '-' in api_key else 'Other'}")
        debug_info.append("")
        debug_info.append("🧪 DETAILED TESTING:")
        
        # Test configurations with detailed logging
        test_configs = [
            {
                "name": "Standard Bearer Token",
                "url": "https://api.jibble.io/v1",
                "headers": {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                "endpoints": ["me", "user", "profile"]
            },
            {
                "name": "X-API-Key Header",
                "url": "https://api.jibble.io/v1", 
                "headers": {"X-API-Key": api_key, "Content-Type": "application/json"},
                "endpoints": ["me", "user", "profile"]
            },
            {
                "name": "Workspace URL + Bearer",
                "url": "https://workspace.prod.jibble.io/v1",
                "headers": {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                "endpoints": ["me", "user", "profile"]
            }
        ]
        
        for i, config_test in enumerate(test_configs, 1):
            debug_info.append(f"\n--- Test {i}: {config_test['name']} ---")
            debug_info.append(f"URL: {config_test['url']}")
            debug_info.append(f"Headers: {config_test['headers']}")
            
            for endpoint in config_test["endpoints"]:
                try:
                    url = f"{config_test['url']}/{endpoint}"
                    response = requests.get(url, headers=config_test["headers"], timeout=10)
                    
                    debug_info.append(f"\n  📡 {endpoint}:")
                    debug_info.append(f"    Status: {response.status_code}")
                    debug_info.append(f"    Headers: {dict(response.headers)}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            debug_info.append(f"    ✅ SUCCESS! Data: {str(data)[:100]}...")
                            return {"message": "\n".join(debug_info)}
                        except:
                            debug_info.append(f"    ✅ SUCCESS! Raw: {response.text[:100]}...")
                            return {"message": "\n".join(debug_info)}
                    else:
                        debug_info.append(f"    ❌ Error: {response.text[:100]}...")
                        
                except Exception as e:
                    debug_info.append(f"    💥 Exception: {str(e)}")
        
        debug_info.append("\n❌ ALL TESTS FAILED")
        debug_info.append("\n💡 SUGGESTIONS:")
        debug_info.append("1. Verify API key in Jibble settings")
        debug_info.append("2. Check if API key has expired")
        debug_info.append("3. Confirm API access is enabled")
        debug_info.append("4. Try regenerating the API key")
        
        return {"message": "\n".join(debug_info)}