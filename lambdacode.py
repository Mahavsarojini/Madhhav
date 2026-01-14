import boto3

ssm = boto3.client('ssm')
INSTANCE_ID = "i-0e2cde15687788470"   # Replace with your EC2 Instance ID

def lambda_handler(event, context):
    action = event.get("action", "stop")   # default = stop
    service = event.get("service", "nginx")

    if action == "start":
        command = f"sudo systemctl start {service}"
        message = f"{service} started successfully"

    elif action == "stop":
        command = f"sudo systemctl stop {service}"
        message = f"{service} stopped successfully"

    else:
        return {
            "status": "FAILED",
            "message": "Invalid action. Use start or stop."
        }

    response = ssm.send_command(
        InstanceIds=[INSTANCE_ID],
        DocumentName="AWS-RunShellScript",
        Parameters={
            "commands": [command]
        }
    )

    return {
        "status": "SUCCESS",
        "message": message,
        "command_id": response["Command"]["CommandId"]
    }
