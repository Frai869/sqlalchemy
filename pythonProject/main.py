import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

def populate_db(session):
    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

def get_shops(in_pub):
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher.books).join(Book.stocks1).join(Stock.shop).join(Stock.sales)
    if in_pub.isdigit():
        q_ = q.filter(Publisher.id == in_pub).all()
    else:
        q_ = q.filter(Publisher.name == in_pub).all()
    for title_, shop_, sale_, date_ in q_:
        print(f"{title_: <40} | {shop_: <10} | {sale_: <8} | {date_.strftime('%d-%m-%Y')}")
    session.close()

if __name__ == '__main__':
    login = input(str('Введите login:'))
    password = input(str('Введите password:'))
    DSN = f'postgresql://{login}:{password}@localhost:5432/orm_db'
    in_pub = input("Введите имя издателя или его идентификатор:")
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    populate_db(session)
    get_shops(in_pub)