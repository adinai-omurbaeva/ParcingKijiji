from peewee import *
 
class BaseModel(Model):
    class Meta:
        database = dbhandle
 
 
class Ad(BaseModel):
    id = PrimaryKeyField(null=False)
    image = CharField(max_length=255)
    title = CharField(max_length=255)
    location = CharField(max_length=255)
    date = DateField()
    bedrooms = CharField(max_length=255)
    description = CharField(max_length=255)
    price = CharField(max_length=255)
    currency = CharField(max_length=255)

    class Meta:
        db_table = "ads"
        order_by = ('date',)