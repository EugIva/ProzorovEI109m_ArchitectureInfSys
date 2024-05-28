from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Index, inspect
from sqlalchemy.orm import sessionmaker
import json
import time
from pymongo import MongoClient
import random


class SQLAlchemyManager:
    def __init__(self, db_name: str = 'postgres'):
        try:
            self.engine = create_engine(
                'postgresql://EUGIVA:EUGIVA@postgres:5432/' + db_name)
            self.metadata = MetaData()
            self.metadata.bind = self.engine
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            print(e)

    def create_tables(self):
        users = Table(
            'recipients', self.metadata,
            Column('recipient_id', Integer, primary_key=True),
            Column('recipient_login', String(255)),
            Column('first_name', String(255)),
            Column('second_name', String(255)),
            Column('address', String(255)),
            Column('password', String(255))
        )

        self.metadata.create_all(self.engine)

        Index('recipient_id_index', users.c.recipient_id)
        Index('recipients_login_index', users.c.recipient_login)
        Index('first_name_index', users.c.first_name)
        Index('second_name_index', users.c.second_name)
        Index('address_index', users.c.address)

    def insert_data(self, data, table_name):
        session = self.Session()
        table = self.metadata.tables[table_name]
        session.execute(table.insert(), data)
        session.commit()
        session.close()

    def init_database(self):

        inspector = inspect(self.engine)
        if not inspector.has_table("recipients"):
            print("Initialize DB")
            self.create_tables()
            with open("./recipients.json", "r") as users_file:
                users_data = json.load(users_file)["recipients"]
            self.insert_data(users_data, "recipients")


class DeliveriesIniter:
    def __init__(self):
        self.client = MongoClient(f"mongodb://EUGIVA:EUGIVA@localhost:27017/")
        self.db = self.client.get_database("arch")
        self.collection = self.db.get_collection("deliveries")

    def load_data(self):
        with open("./recipients.json", "r") as data_json:
            data: dict = json.load(data_json)
        users_list = data['recipients']
        deliveries = []
        for _ in range(0, 100):
            delivery = {}
            addreses = [i["address"]
                        for i in (random.choices(users_list, k=2))]
            delivery["from_address"], delivery["to_address"] = addreses[0], addreses[1]
            print(delivery)

            deliveries.append(delivery)


if __name__ == "__main__":
    # sqlalchemy_manager = SQLAlchemyManager(db_name="arch_db")
    # sqlalchemy_manager.init_database()
    # print("Successful initializing")
    deliveries_manager = DeliveriesIniter()
    deliveries_manager.load_data()
