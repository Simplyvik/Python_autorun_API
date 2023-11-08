from robocorp.tasks import task


@task
def consumer_send_object_as_response():
    message = "Hello"
    message = message + " World! consumer"
    print(message)
