import datetime
import os
import peewee
from werkzeug import secure_filename

__author__ = "Francesco Mirabelli, Marco Tinacci"
__copyright__ = "Copyright 2017"
__email__ = "ceskomira90@gmail.com, marco.tinacci@gmail.com"

DATABASE = {
    'name': 'ecommerce.db',
    'engine': 'peewee.SqliteDatabase',
}

db = peewee.SqliteDatabase(DATABASE['name'])

PRICE_PRECISION = 2


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
    price = peewee.FloatField()
    description = peewee.TextField()

    def __str__(self):
        return '{}, {}, {}'.format(
            self.name,
            round(float(self.price), PRICE_PRECISION),
            self.description)

    def json(self):
        return {
            'name': self.name,
            'price': round(float(self.price), PRICE_PRECISION),
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
