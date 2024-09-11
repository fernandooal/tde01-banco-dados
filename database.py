from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Criação da base para as tabelas
Base = declarative_base()

# Modelo da tabela Product
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

# Configuração do banco de dados (usando SQLite por simplicidade)
engine = create_engine('sqlite:///vending_machine.db')

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)

# Configuração da sessão para interagir com o banco
Session = sessionmaker(bind=engine)
session = Session()

# Funções utilitárias para manipular o banco de dados
def add_product_to_db(session, name, price, stock):
    new_product = Product(name=name, price=price, stock=stock)
    session.add(new_product)
    session.commit()

def get_all_products(session):
    return session.query(Product).all()

def update_product_stock(session, product_id, new_stock):
    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        product.stock = new_stock
        session.commit()
