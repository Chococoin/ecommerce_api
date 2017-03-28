import datetime
import peewee

DATABASE = {
    'name': 'ecommerce.db',
    'engine': 'peewee.SqliteDatabase',
}

db = peewee.SqliteDatabase(DATABASE['name'])


class BaseModel(peewee.Model):
    """Common features of models"""

    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        """Automatically update updated_at time during save"""
        self.modified = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = db


class Item(BaseModel):
    """Item model"""
    name = peewee.CharField(unique=True)
    price = peewee.DecimalField(decimal_places=2, auto_round=True)
    description = peewee.TextField()

    def __str__(self):
        return '{}, {}, {}'.format(
            self.name,
            self.price,
            self.description)

    def json(self):
        return {
            'name': self.name,
            'price': float(self.price),
            'description': self.description
        }


class Picture(BaseModel):
    """Picture model"""

    image = peewee.CharField()

    def json(self):
        return {
            'image': self.image
        }

    def __str__(self):
        return self.image


class ItemPicture(BaseModel):
    """Item-Picture cross-table"""
    item = peewee.ForeignKeyField(Item)
    picture = peewee.ForeignKeyField(Picture)


def connect():
    """
    Establish a connection to the database, create tables
    if not existing already
    """
    if db.is_closed():
        db.connect()
        Item.create_table(fail_silently=True)
        Picture.create_table(fail_silently=True)


def close():
    """Close the database connection"""
    if not db.is_closed():
        db.close()
