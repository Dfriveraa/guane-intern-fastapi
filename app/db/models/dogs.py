from tortoise import fields
from tortoise.models import Model


class Dogs(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    is_adopted = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "dogs"

# class Dog(Base):
#     __tablename__ = "dogs"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True)
#     picture = Column(String)
#     is_adopted = Column(Boolean, default=False)
#     created_date = Column(DateTime, default=datetime.now())
#     publisher_id = Column(Integer, ForeignKey("users.id"))
#     adopter_id = Column(Integer, ForeignKey("users.id"))
#     publisher = relationship("User", back_populates="registered_dogs", foreign_keys=[publisher_id])
#     adopter = relationship("User", back_populates="adopted_dogs", foreign_keys=[adopter_id])


# Base.metadata.create_all(bind=engine)
