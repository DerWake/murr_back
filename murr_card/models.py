from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

Murren = get_user_model()


class MurrLike(models.Model):
    """Счетчик лайков мурра"""
    user = models.ForeignKey(Murren, on_delete=models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class MurrCard(models.Model):
    title = models.CharField(max_length=224)
    cover = models.ImageField(blank=True, null=True, upload_to='murr_cover/%Y/%m/%d/')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Murren, on_delete=models.CASCADE, related_name='murr_cards')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.cover:
            self.cover.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.cover:

            img = Image.open(self.cover.path)

            if img.mode in ('RGBA', 'LA'):
                fill_color = '#C3A1FF'
                background = Image.new(img.mode[:-1], img.size, fill_color)
                background.paste(img, img.split()[-1])
                img = background
            if img.height > 320 or img.width > 320:
                output_size = (320, 320)
                img.thumbnail(output_size)
                img.save(self.cover.path, 'jpeg')

    @property
    def total_likes(self):
        return self.likes.count()


class EditorImageForMurrCard(models.Model):
    murr_editor_image = models.ImageField(upload_to='editor_image_for_murr_card/%Y/%m/%d/', null=True, max_length=255)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.murr_editor_image.path)
        img = img.convert('RGB')

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.murr_editor_image.path, 'jpeg')
