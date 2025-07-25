# Usage Guide

## Getting Started

Once the Jibble Connector is installed and configured, the synchronization between Jibble and Odoo HR Attendance happens automatically. This guide covers daily usage and monitoring.

## Employee Attendance Flow

### Automatic Synchronization

1. **Employee clocks in/out in Jibble**
2. **Jibble sends webhook notification** (real-time)
3. **Odoo receives and processes** the time entry
4. **Attendance record created/updated** in Odoo
5. **Sync log entry created** for monitoring

### Manual Operations

#### Viewing Employee Attendance

1. **Go to HR > Attendance > Attendances**
2. **Filter by employee** to see their records
3. **Jibble-specific fields**:
   - **Jibble Entry ID**: Reference to original Jibble entry
   - **Jibble Activity**: Activity/task from Jibble
   - **Jibble Project**: Project assignment
   - **Jibble Location**: Location information

#### Employee Management

**To enable/disable sync for an employee**:
1. Go to **HR > Employees**
2. Select employee
3. In **Jibble Integration** section:
   - Toggle **Jibble Synchronization**
   - Update **Jibble User ID** if changed
   - Modify **Jibble Email** if needed

## Monitoring and Logs

### Sync Log Dashboard

**Access**: **HR > Jibble Sync Logs**

#### Log Entry Types

**Success Entries** (Green):
- Successful webhook processing
- Completed scheduled synchronizations
- Successfully created/updated attendance records

**Warning Entries** (Yellow):
- Time entry deletions from Jibble
- Minor data inconsistencies
- Employee mapping issues (non-critical)

**Error Entries** (Red):
- API authentication failures
- Webhook signature validation errors
- Employee not found errors
- Data processing failures

#### Filtering and Search

**Quick Filters**:
- **Today**: Show today's sync activities
- **This Week**: Show current week's logs
- **Success/Warning/Error**: Filter by status

**Search Options**:
- Employee name
- Jibble Entry ID
- Error messages
- Date ranges

**Group By Options**:
- Status
- Sync Type (webhook, cron, manual)
- Employee
- Date

### Real-time Monitoring

#### Dashboard Indicators

Monitor these key metrics:
- **Success Rate**: Percentage of successful syncs
- **Response Time**: Webhook processing speed
- **Error Frequency**: Rate of sync failures
- **Last Sync**: Time of most recent activity

#### Alert Conditions

Set up monitoring for:
- Multiple consecutive failures
- Webhook endpoint downtime
- API rate limit exceeded
- Employee mapping errors

## Common Workflows

### Daily Operations

**Morning Check**:
1. Review overnight sync logs
2. Check for any error entries
3. Verify employee check-ins are syncing

**Issue Resolution**:
1. Identify failed sync entries
2. Check employee Jibble mappings
3. Verify API connectivity
4. Re-process failed entries if needed

### Weekly Maintenance

**Review Sync Performance**:
1. Analyze sync success rates
2. Identify frequently failing employees
3. Update employee mappings as needed
4. Clean up old log entries

**Data Validation**:
1. Compare Jibble and Odoo attendance records
2. Verify project and activity mappings
3. Check timezone conversions
4. Validate working hours calculations

### Monthly Review

**Configuration Audit**:
1. Review API key status
2. Verify webhook configuration
3. Check employee mappings completeness
4. Update sync intervals if needed

**Performance Analysis**:
1. Analyze sync patterns
2. Identify optimization opportunities
3. Review error trends
4. Plan system improvements

## Advanced Usage

### Bulk Operations

#### Mass Employee Update

To update multiple employees' Jibble settings:
1. Export employee list with Jibble fields
2. Update in spreadsheet
3. Import back to Odoo
4. Verify mappings are correct

#### Historical Data Sync

For initial setup or data recovery:
1. Use manual sync functionality
2. Specify date ranges for sync
3. Monitor progress in sync logs
4. Validate imported data

### Integration with Other Modules

#### Timesheet Integration

If timesheet creation is enabled:
1. Attendance records automatically create timesheet entries
2. Project information from Jibble maps to timesheet projects
3. Activity details populate timesheet descriptions

#### Payroll Integration

Attendance data flows to payroll:
1. Working hours calculated from attendance
2. Overtime detection based on schedules
3. Project-based time tracking for billing

### Custom Workflows

#### Approval Processes

Set up attendance approval workflows:
1. Configure approval rules in HR settings
2. Jibble entries create pending attendance records
3. Managers approve/reject via Odoo interface

#### Exception Handling

Handle special cases:
1. Late arrivals notification
2. Extended breaks detection
3. Location-based validation
4. Schedule compliance checking

## Troubleshooting Common Issues

### Sync Delays

**Symptoms**: Attendance appears late in Odoo
**Solutions**:
1. Check webhook configuration
2. Verify network connectivity
3. Review scheduled sync frequency
4. Check for API rate limiting

### Missing Attendance Records

**Symptoms**: Some time entries don't appear in Odoo
**Solutions**:
1. Verify employee Jibble User ID mapping
2. Check if sync is enabled for employee
3. Review sync logs for error messages
4. Validate Jibble entry format

### Duplicate Entries

**Symptoms**: Same time entry appears multiple times
**Solutions**:
1. Check for duplicate webhook calls
2. Verify unique entry ID handling
3. Review sync logic for duplicates
4. Clean up duplicate records

### Data Inconsistencies

**Symptoms**: Time or project data doesn't match
**Solutions**:
1. Verify timezone settings
2. Check project/activity mappings
3. Validate data transformation logic
4. Compare source data in Jibble

## Best Practices

### Daily Usage

1. **Monitor sync logs regularly**
2. **Address errors promptly**
3. **Keep employee mappings updated**
4. **Verify critical attendance records**

### Data Management

1. **Regular backup of sync configurations**
2. **Periodic cleanup of old logs**
3. **Validate data integrity monthly**
4. **Document custom configurations**

### Security

1. **Rotate API keys periodically**
2. **Monitor webhook access logs**
3. **Restrict admin access appropriately**
4. **Use HTTPS for all communications**

### Performance

1. **Optimize sync intervals based on usage**
2. **Monitor webhook response times**
3. **Clean up unnecessary log entries**
4. **Use filters efficiently in views**

## Getting Help

### Self-Help Resources

1. **Sync Logs**: First source for troubleshooting
2. **Configuration Review**: Verify all settings
3. **Employee Mappings**: Check user ID assignments
4. **API Status**: Verify Jibble service status

### Support Channels

1. **GitHub Issues**: Report bugs and feature requests
2. **Documentation**: Reference technical details
3. **Community Forums**: General questions and tips
4. **Professional Support**: For complex implementations

Remember to always test changes in a development environment before applying to production systems.