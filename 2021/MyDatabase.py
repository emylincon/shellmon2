from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html


class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    node_ip = Column(String, nullable=False)
    util = relationship('Utilization', backref='utils', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.node_ip}')"


class Utilization(Base):
    __tablename__ = 'utilization'
    id = Column(Integer, primary_key=True)
    cpu = Column(Float, nullable=False)
    mem = Column(Float, nullable=False)
    net = Column(Float, nullable=False)
    sto = Column(Float,  nullable=False)
    bat = Column(Float, nullable=False)
    datetime = Column(String, nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.cpu}', '{self.mem}', '{self.net}', " \
               f"'{self.sto}', '{self.bat}', '{self.datetime}')"


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()
u = Server(node_ip='192.168.1.1')
a = Utilization(cpu=20.1, mem=11.1, net=12.1, sto=10.5, bat=30.33, datetime='12/06/2021', server_id=1)
session.add(u)
session.add(a)
session.commit()

us = session.query(Server).all()
print(us)
print(us[0].util)

# t = session.query(Server).filter_by(node_ip='192.168.1.1').all()
t = session.query(Server).filter_by(node_ip='192.168.1.1').first()
print(t)
session.close()
