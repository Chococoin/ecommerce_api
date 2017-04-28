"""
Drop any test database tables (user, item, order, orderitem)
and supply a new one db with new down-to-earth data.
"""

from peewee import SqliteDatabase
from models import User, Item, Order, OrderItem, Address
from faker import Factory
from colorama import init, Fore, Style
import os
import sys
import sqlite3
import glob
import random

init(autoreset=True)


TEXT_DISPLAY = Fore.MAGENTA + Style.BRIGHT + """
                      WELCOME TO DEMO CONTENT CREATOR.
                      --------------------------------
                    """ + Fore.WHITE + Style.DIM + """
                Here you could create a new simulated database.
                """
MENU_TEXT = Fore.GREEN + Style.BRIGHT + """
                ***********************************************
                *Press:                                       *
                *(1) To overwrite the database with new data. *
                *(2) Create a new db with a new name.         *
                *(3) delete and exit.                         *
                *(Enter) Just to exit.                        *
                ***********************************************
            """

WARNING_DELETE = Fore.YELLOW + Style.BRIGHT + """
                ##################################################
                #   WARNING: YOU WILL DELETE FILES PERMANENTLY   #
                ##################################################
                """

WARNING_OVERWRITE = Fore.YELLOW + Style.BRIGHT + """
                ##################################################
                #   WARNING: YOU WILL CHANGE FILES PERMANENTLY   #
                ##################################################
                """


def set_db(database):
        Order._meta.database = database
        Item._meta.database = database
        OrderItem._meta.database = database
        User._meta.database = database
        Address._meta.database = database


def write_db():
    """
    Given the SEED 9623954 the first user email is
    'fatima.caputo@tiscali.it', and its password is '9J0.'
    """
    SEED = 9623954
    fake = Factory.create('it_IT')
    fake.seed(SEED)
    random.seed(SEED)

    class CountInsertions:
        def __init__(self, table):
            self.total = 0
            for i in table.select():
                self.total += 1

        def random_pick(self,):
            pick = random.choice(range(1, self.total+1))
            return pick

    def user_creator(num_user=1):
        """Create users from an Italian-like context. Due to param in factory create 'it_iT'."""
        for i in range(0, num_user):
            user_uuid = fake.uuid4()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email_provider = fake.free_email_domain()
            email_user = '{}.{}@{}'.format(first_name.lower(), last_name.lower(), email_provider)
            password = fake.password(length=3, special_chars=False, digits=True,
                                     upper_case=True, lower_case=False)
            User.create(
                user_id=user_uuid,
                first_name=first_name,
                last_name=last_name,
                email=email_user,
                password=User.hash_password(password)
            )

    def item_creator(num_item=1):
        # def item_bundler(item_id, item_price):
        #     """Create a list of items to be handle by other functions."""
        #     list_items = []
        #     temp_pack = {'item_id': item_id, 'item_price': item_price}
        #     list_item.append(temp_pack)
        #     return list_items
        for i in range(0, num_item):
            item_id = fake.uuid4()
            item_name = fake.sentence(nb_words=3, variable_nb_words=True)
            item_price = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
            Item.create(
                item_id=item_id,
                name=item_name,
                price=item_price,
                description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
            )

    def address_creator(num_addr=1):
        LIST_COUNTRIES = ['Belgium', 'France', 'Germany',
                          'Greece', 'Italy', 'Portugal', 'Spain']
        for i in range(1, num_addr):
            country = random.choice(LIST_COUNTRIES)
            user_id = CountInsertions(User)
            Address.create(
                address_id=fake.uuid4(),
                user=user_id.random_pick(),
                country=country,
                city=fake.city(),
                post_code=fake.postcode(),
                address=fake.street_name(),
                phone=fake.phone_number(),
            )

    # WORK TO DO!!!!!!
    # def order_creator(num_order=1):
    #     for i in range(0, num_order):
    #         country = random.choice(LIST_COUNTRIES)
    #         user_id = CountInsertions(User)
    #         order_id = fake.uuid4()
    #         address = '{} {}\n{} {}\n{}'.format((fake.random_digit()+1), fake.street_name(),
    #                                               fake.postcode(), fake.city(), country)
    #         Order.create(
    #             order_id=order_id,
    #             total_price=0,
    #             delivery_address=address,
    #             user_id=user_id
    #         )

    # def order_item_creator(num_order_item=1):
    #     """crei item, poi order, poi orderitem e aggiorni i valori di order"""
    #     class ItemRaffle:
    #         """Help create orders with a different number of items."""
    #         def __init__(self):
    #             self.order = [{ 'order_id': None,
    #                             'date': None,
    #                             'total_price': None,
    #                             'user_id': None,
    #                             'order': {
    #                                     'items': [],
    #                                     'delivery_address': None,
    #                                     'user': None
    #                                     }
    #                         }]
    #             self.num_item = random.randint(1,5)
    #             for i in range(0, self.num_item):
    #                 self.order['order']['items'].append(list_item_data[i])

    #     winner = ItemRaffle()
    #     order_item = winner.order
    #     random.shuffle(LIST_COUNTRIES)
    #     country = LIST_COUNTRIES[0]
    #     random.shuffle(list_users_uuid)
    #     used_uuid = list_users_uuid[0]
    #     address = '{} {}\n{} {}\n '.format(fake.random_digit(), fake.street_name(),
    #                                           fake.city(), fake.postcode(), country[0] )
    #     order_item['order']['delivery_address'] = address
    #     order_item['order']['user'] = list_users_uuid[0]

    # start create users

    user_creator(10)

    # start create addresses

    address_creator(10)

    # start create items

    item_creator(10)

    # start create orders
    # TODO
    # order_creator(1)


def get_databases():
    """create a list with the name of each .db file from main folder."""
    list_of_db = glob.glob('*.db')
    return list_of_db


def print_any_db():
    """In the case there's any db it prints a list in the CLI."""
    list_of_db = get_databases()
    lenght_of_list = len(list_of_db)
    word_db = 'database'
    if lenght_of_list > 1:
        word_db = 'databases'
    print(Fore.YELLOW + Style.BRIGHT
          + 'You\'ve already {} {} in your folder :'.format(lenght_of_list, word_db))
    for index, name_db in enumerate(list_of_db, start=1):
        print(index, '-', name_db)
    else:
        good_bye('Error')


def drops_all_tables(database):
    """Doesn't drop unknown tables."""
    tables = database.get_tables()
    for table in tables:
        if table == 'item':
            Item.drop_table()
        if table == 'order':
            Order.drop_table()
        if table == 'user':
            User.drop_table()
        if table == 'orderitem':
            OrderItem.drop_table()
        if table == 'address':
            Address.drop_table()


def create_tables():
    User.create_table(fail_silently=True)
    Item.create_table(fail_silently=True)
    Order.create_table(fail_silently=True)
    OrderItem.create_table(fail_silently=True)
    Address.create_table(fail_silently=True)


def good_bye(word, default='has'):
    print(Fore.BLUE + Style.BRIGHT + '*-* Your database {1} been {0}. *-*'.format(word, default))
    print(Fore.CYAN + Style.BRIGHT + '*_* Have a nice day! *_*')
    sys.exit()


def remove_unique_db():
    path = get_databases()
    os.remove('../'+path[0])
    good_bye('deleted')


def remove_chosen_db(list_of):
    list_of_db = get_databases()
    lenght_of_list = len(list_of_db)
    print(WARNING_DELETE)
    for index, name_db in enumerate(list_of_db, start=1):
        print('('+str(index)+')'+'.-', name_db+' |', end=' ')
    print('\n')
    choice_a_db = input(Fore.YELLOW + Style.BRIGHT
                        + 'Press the number of database to delete '
                        + 'or hit [ENTER] to exit without changes. > ')
    if choice_a_db is '':
        sys.exit()
    else:
        try:
            choice_a_db = int(choice_a_db)-1
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "Oops! That wasn't a number. Try again...")
            sys.exit()
    while True:
        path = list_of_db[choice_a_db]
        if choice_a_db <= lenght_of_list:
            print(Fore.YELLOW + Style.BRIGHT + 'You\'ve chosen {}'.format(path))
            os.remove(path)
            good_bye('deleted')
        else:
            overwrite_chosen_db(list_of)  # MIND THE BUG!!!
            os.remove(path)


def overwrite_unique_db():
    list_of_db = get_databases()
    name_db = list_of_db[0]
    print(WARNING_OVERWRITE, '\n')
    print(Fore.YELLOW + Style.BRIGHT + 'You\'ve got only a database')
    print('(1)'+'.-', name_db, end='\n')
    print('Are you sure to overwrite {}?'.format(name_db))
    selct = input('if Yes press(1) or [ENTER] to exit without change. >'
                  + Fore.YELLOW + Style.BRIGHT + ' ')
    if selct is '1':
        db = SqliteDatabase(list_of_db[0], autocommit=False)
        set_db(db)
        drops_all_tables(db)
        create_tables()
        write_db()
        good_bye('written')
    if selct is '':
        good_bye('change', default='hasn\'t')
    else:
        overwrite_unique_db()


def overwrite_chosen_db():
    list_of_db = get_databases()
    lenght_of_list = len(list_of_db)
    print(WARNING_OVERWRITE)
    for index, name_db in enumerate(list_of_db, start=1):
        print('('+str(index)+')'+'.-', name_db+' |', end=' ')
    print('\n')
    choice_a_db = input(Fore.YELLOW + Style.BRIGHT
                        + 'Press the number of database to overwrite '
                        + 'or hit [ENTER] to exit without changes. > ')
    if choice_a_db is '':
        sys.exit()
    else:
        try:
            choice_a_db = int(choice_a_db)-1
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "Oops! That wasn't a number. Try again...")
            sys.exit()
    while True:
        if choice_a_db <= lenght_of_list:
            db = SqliteDatabase(list_of_db[choice_a_db], autocommit=False)
            set_db(db)
            print('You\'ve chosen {}'.format(db.database))
            if db.is_closed():
                db.connect()
            drops_all_tables(db)
            create_tables()
            write_db()
            good_bye('written')
        else:
            overwrite_chosen_db()


def main():

    print(TEXT_DISPLAY)
    while True:
            list_of_db = get_databases()
            lenght_of_list = len(list_of_db)
            print(MENU_TEXT)
            selct = input('Press your choice > ')
            if selct == '1':
                if lenght_of_list == 1:
                    overwrite_unique_db()
                if lenght_of_list == 0:
                    print(Fore.YELLOW + Style.BRIGHT
                          + 'No database founded. I\'ll create one for you')
                    db = SqliteDatabase('database.db')
                    set_db(db)
                    create_tables()
                    write_db()
                    good_bye('created')
                else:
                    overwrite_chosen_db()
            if selct == '2':
                name_new_db = input(Fore.YELLOW + Style.BRIGHT
                                    + 'Write the name of the new db. > ')
                sqlite3.connect(name_new_db+'.db')
                db = SqliteDatabase(name_new_db+'.db', autocommit=True)
                if db.is_closed():
                    db.connect()
                print(db.database)
                set_db(db)
                create_tables()
                write_db()
                good_bye('created')
            if selct == '3':
                print(WARNING_DELETE)
                print_any_db()
                if lenght_of_list == 1:
                    remove_unique_db()
                else:
                    remove_chosen_db(list_of_db)
            if selct == '':
                good_bye('change', 'hasn\'t')


if __name__ == '__main__':
    main()
