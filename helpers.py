import uuid
__all__ = ["generate_uuid"]

# this function will be embedded in the email generator
def generate_uuid():
    return str(uuid.uuid4())