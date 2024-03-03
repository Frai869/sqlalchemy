import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

login = input(str('Введите login:'))
password = input(str('Введите password:'))
DSN = f'postgresql://{login}:{password}@localhost:5432/orm_db'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

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

in_pub = input('Введите идентификатор издателя (Publisher_id):')
q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher.books).join(Book.stocks1).join(Stock.shop).join(Stock.sales).filter(Publisher.id == in_pub)
# print(q)
print('У запрашиваемого издательства проданы книги (наименование, магазин, стоимость, дата покупки):')
for b in q:
    print(b)
session.close()





