from sqlalchemy import event, inspect
from app.models.users import User
from app.models.providers import Provider
from app.models.service_image import ServiceImage
from app.models.message import Message
from app.services.upload_service import delete_image_from_s3

def delete_old_image(target, field_name):
    """Checks if an image field has changed and deletes the old image from S3."""
    insp = inspect(target)
    attr = insp.attrs.get(field_name)
    if attr:
        history = attr.history
        if history.has_changes():
            # history.deleted contains the old values
            for old_value in history.deleted:
                if old_value and isinstance(old_value, str) and old_value != getattr(target, field_name):
                    delete_image_from_s3(old_value)

# User events
@event.listens_for(User, "before_update")
def user_before_update(mapper, connection, target):
    delete_old_image(target, "profile_image")

@event.listens_for(User, "after_delete")
def user_after_delete(mapper, connection, target):
    if target.profile_image:
        delete_image_from_s3(target.profile_image)

# Provider events
@event.listens_for(Provider, "before_update")
def provider_before_update(mapper, connection, target):
    delete_old_image(target, "profile_image")

@event.listens_for(Provider, "after_delete")
def provider_after_delete(mapper, connection, target):
    if target.profile_image:
        delete_image_from_s3(target.profile_image)

# ServiceImage events
@event.listens_for(ServiceImage, "after_delete")
def service_image_after_delete(mapper, connection, target):
    if target.image_url:
        delete_image_from_s3(target.image_url)

# Message events
@event.listens_for(Message, "after_delete")
def message_after_delete(mapper, connection, target):
    if target.image_url:
        delete_image_from_s3(target.image_url)

def init_image_events():
    """Dummy function to ensure this module is imported and listeners are registered."""
    pass
