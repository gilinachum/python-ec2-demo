"""
    Records metric to cloudwatch
    
    Args:
        instance_id (string): 
        busy_wait_in_seconds (int): how to long to keep cpu busy
"""
def record_metric(instance_id, busy_wait_in_seconds):
    import boto3
    client = boto3.client('cloudwatch')
    response = client.put_metric_data(
    Namespace='python-app',
    MetricData=[
        {
            'MetricName': 'calls',
            'Dimensions': [
                {
                    'Name': 'busy_wait_in_seconds',
                    'Value': str(busy_wait_in_seconds)
                },
                {
                    'Name': 'instance_id',
                    'Value': instance_id
                }
            ],
            'Value': 1,
            'Unit': 'None',
            'StorageResolution': 1
        },
    ])
    return response

print(str(record_metric('123', 1)))