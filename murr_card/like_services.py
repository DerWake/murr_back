from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import MurrLike

Murren = get_user_model()

def add_like(obj, user):
    """Лайкает Murr.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    MurrLike.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)

def remove_like(obj, user):
    """Удаляет лайк с Murr.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    MurrLike.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()
def add_or_remove_like(obj, user) -> bool:
    """Удаляет или ставит лайк в зависимости от прошлых действий Murren'a на Murr.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    if MurrLike.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user).exists():
        return remove_like(obj, user)
    else:
        return add_like(obj, user)
