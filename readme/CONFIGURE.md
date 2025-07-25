# Configuration Guide

## Initial Setup

### 1. Module Installation

1. Install the module from Apps menu:
   - Go to **Apps**
   - Search for "Jibble Connector"
   - Click **Install**

2. The module will automatically:
   - Create necessary database tables
   - Set up security rules
   - Configure default settings

### 2. Basic Configuration

Navigate to **Settings > HR > Jibble Integration**:

#### Required Settings
- **Enable Jibble Synchronization**: Check this box to activate the integration
- **Jibble API Key**: Your API key from Jibble dashboard
- **Jibble Organization ID**: Your organization identifier from Jibble

#### Optional Settings
- **Webhook Secret**: Secret key for webhook signature verification (recommended)
- **Sync Interval**: Minutes between automatic synchronizations (default: 15)
- **Create Timesheet Entries**: Auto-create timesheet records from attendance

### 3. Jibble API Setup

#### Obtaining API Credentials

1. **Login to Jibble**:
   - Go to [Jibble Dashboard](https://app.jibble.io)
   - Login with your admin account

2. **Access API Settings**:
   - Navigate to **Settings > Integrations**
   - Find **API Access** section
   - Generate or copy your API key

3. **Find Organization ID**:
   - In Jibble dashboard, check URL or Settings
   - Organization ID is usually visible in the URL or account settings

#### Webhook Configuration

1. **In Jibble Dashboard**:
   - Go to **Settings > Webhooks**
   - Click **Add Webhook**

2. **Configure Webhook**:
   - **URL**: `https://your-odoo-domain.com/jibble/webhook`
   - **Events**: Select all time entry events:
     - `timeEntry.created`
     - `timeEntry.updated`
     - `timeEntry.deleted`
   - **Secret**: Enter the same secret configured in Odoo

## Employee Configuration

### Mapping Jibble Users to Odoo Employees

For each employee who uses Jibble:

1. **Go to HR > Employees**
2. **Edit employee record**
3. **In Jibble Integration section**:
   - **Jibble User ID**: Enter the user's ID from Jibble
   - **Jibble Email**: Enter the email used in Jibble
   - **Jibble Synchronization**: Enable checkbox

#### Finding Jibble User IDs

**Method 1: From Jibble Dashboard**
- Go to **People** section in Jibble
- Click on user profile
- User ID is shown in the URL or profile details

**Method 2: From API Call**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://api.jibble.io/v1/users?organizationId=YOUR_ORG_ID"
```

## Advanced Configuration

### Scheduled Synchronization

The module automatically creates a scheduled action for periodic sync:

1. **Go to Settings > Technical > Automation > Scheduled Actions**
2. **Find "Jibble: Synchronize Attendance"**
3. **Configure**:
   - **Active**: Enable/disable automatic sync
   - **Interval**: Adjust sync frequency
   - **Next Execution**: Set next run time

### Security Configuration

#### User Permissions

Ensure users have appropriate access:

- **HR Users**: Can view sync logs and employee Jibble settings
- **HR Managers**: Can configure integration settings and manage all sync operations
- **System Administrators**: Full access to technical settings

#### Network Security

For webhook reception:
- Ensure your Odoo server is accessible from Jibble servers
- Configure firewall to allow HTTPS traffic on webhook endpoint
- Use HTTPS for secure data transmission

### Database Configuration

#### Indexing for Performance

The module automatically creates indexes on:
- `hr.employee.jibble_user_id`
- `hr.attendance.jibble_entry_id`
- `jibble.sync.log.create_date`

#### Cleanup Policies

Consider setting up automated cleanup for sync logs:

```python
# Example: Delete logs older than 90 days
self.env['jibble.sync.log'].search([
    ('create_date', '<', fields.Datetime.now() - timedelta(days=90))
]).unlink()
```

## Testing Configuration

### Webhook Testing

1. **Test webhook endpoint**:
```bash
curl -X POST https://your-odoo.com/jibble/webhook \
     -H "Content-Type: application/json" \
     -H "X-Jibble-Signature: test-signature" \
     -d '{"eventType": "test", "payload": {}}'
```

2. **Check sync logs**:
   - Go to **HR > Jibble Sync Logs**
   - Verify webhook events are being received

### Manual Sync Testing

1. **Trigger manual sync**:
   - Use the sync wizard (if implemented)
   - Or create a test time entry in Jibble
   - Check if it appears in Odoo attendance

2. **Verify data mapping**:
   - Check that all fields are correctly mapped
   - Verify timestamps are in correct timezone
   - Confirm employee mapping is working

## Troubleshooting Configuration

### Common Issues

1. **Webhook not working**:
   - Verify URL is accessible from internet
   - Check webhook secret matches
   - Review Odoo logs for errors

2. **Employee not found errors**:
   - Verify Jibble User ID is correctly set
   - Check employee record exists and is active
   - Confirm sync is enabled for employee

3. **API authentication failures**:
   - Verify API key is correct and active
   - Check organization ID matches
   - Ensure API key has required permissions

### Debug Mode

Enable debug logging by adding to Odoo configuration:

```ini
[logger_jibble_connector]
level = DEBUG
handlers = console
qualname = odoo.addons.jibble_connector
```

## Production Considerations

### Performance Optimization

- Adjust sync interval based on usage patterns
- Monitor webhook response times
- Consider batch processing for large datasets

### Monitoring

Set up monitoring for:
- Webhook endpoint availability
- Sync success rates
- API rate limiting
- Error frequencies

### Backup and Recovery

- Include Jibble configuration in backup procedures
- Document API credentials for disaster recovery
- Test restore procedures including webhook reconfiguration