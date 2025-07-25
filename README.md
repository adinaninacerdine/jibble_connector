# Jibble Connector for Odoo

[![License: AGPL-3](https://img.shields.io/badge/licence-AGPL--3-blue.svg)](http://www.gnu.org/licenses/agpl-3.0-standalone.html)

## Overview

The Jibble Connector module provides seamless integration between [Jibble](https://jibble.io) time tracking system and Odoo HR Attendance. This module enables automatic synchronization of time entries from Jibble to Odoo, supporting both real-time webhook updates and scheduled synchronization.

## Features

- 🔄 **Real-time synchronization** via webhooks
- ⏰ **Scheduled synchronization** with configurable intervals  
- 👥 **Employee mapping** between Jibble and Odoo
- 📊 **Comprehensive logging** and monitoring
- 🔐 **Secure webhook validation** with HMAC signatures
- ⚙️ **Easy configuration** through Odoo settings
- 📈 **Attendance tracking** with project and activity details

## Installation

### Prerequisites

- Odoo 18.0+
- Python 3.8+
- `requests` library

### Install

1. Clone this repository to your Odoo addons directory:
```bash
git clone https://github.com/HuriMoney/jibble_connector.git /path/to/odoo/addons/
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Update your Odoo apps list and install the module:
   - Go to Apps menu
   - Click "Update Apps List"
   - Search for "Jibble Connector"
   - Install the module

## Configuration

1. **Go to Settings > HR > Jibble Integration**

2. **Enable synchronization** and configure:
   - **API Key**: Your Jibble API key
   - **Organization ID**: Your Jibble organization ID
   - **Webhook Secret**: Secret for webhook validation
   - **Sync Interval**: Minutes between automatic syncs (default: 15)
   - **Create Timesheet**: Auto-create timesheet entries

3. **Map employees** by setting their Jibble User ID in employee records

4. **Configure webhook** in Jibble pointing to: `https://your-odoo.com/jibble/webhook`

## Usage

### Employee Mapping

1. Go to **HR > Employees**
2. Edit employee record
3. In **Jibble Integration** section, set:
   - Jibble User ID
   - Jibble Email
   - Enable synchronization

### Monitoring

View synchronization logs at **HR > Jibble Sync Logs** to monitor:
- Real-time webhook events
- Scheduled sync results
- Error messages and debugging info

## API Integration

### Webhook Events

The module handles these Jibble webhook events:
- `timeEntry.created`
- `timeEntry.updated` 
- `timeEntry.deleted`

### Data Mapping

| Jibble Field | Odoo Field | Description |
|--------------|------------|-------------|
| `userId` | `employee_id` | Via jibble_user_id mapping |
| `clockIn` | `check_in` | Converted to UTC |
| `clockOut` | `check_out` | Converted to UTC |
| `activity.name` | `jibble_activity` | Activity information |
| `project.name` | `jibble_project` | Project information |
| `location` | `jibble_location` | Location data |

## Development

### Project Structure
```
jibble_connector/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── hr_employee.py
│   ├── hr_attendance.py
│   ├── jibble_sync_log.py
│   └── res_config_settings.py
├── views/
│   ├── hr_employee_views.xml
│   ├── jibble_sync_log_views.xml
│   └── res_config_settings_views.xml
├── controllers/
│   └── webhook.py
├── wizards/
│   └── jibble_sync_wizard.py
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
└── data/
    └── ir_cron_data.xml
```

### Running Tests

```bash
# Run module tests
odoo-bin -c config.conf -d test_db -i jibble_connector --test-enable --stop-after-init
```

## Troubleshooting

### Common Issues

1. **Webhook not receiving data**
   - Verify webhook URL is accessible
   - Check webhook secret configuration
   - Review firewall settings

2. **Employee not found**
   - Ensure Jibble User ID is set in employee record
   - Verify user exists in both systems

3. **Sync errors**
   - Check API key permissions
   - Verify organization ID
   - Review sync logs for details

### Debug Mode

Enable debug logging by setting log level to DEBUG for `jibble_connector` logger.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following Odoo coding standards
4. Add tests for new functionality
5. Submit a pull request

## Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review sync logs for error details

## License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Author

**Huri Money** - *Initial work*

---

Made with ❤️ for the Odoo community