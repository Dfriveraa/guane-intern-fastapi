from tortoise import fields
from tortoise.models import Model


class Dog(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    is_adopted = fields.BooleanField(default=False)
    picture = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    publisher = fields.ForeignKeyField("models.User",
                                       related_name="registered_dogs",
                                       on_delete=fields.SET_NULL,
                                       null=True)
    adopter = fields.ForeignKeyField("models.User",
                                     related_name="adopted_dogs",
                                     on_delete=fields.CASCADE,
                                     null=True)

    class Meta:
        table = "dogs"
