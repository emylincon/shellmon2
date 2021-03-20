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
        return f"Server('{self.id}', '{self.node_ip}')"


class Utilization(Base):
    __tablename__ = 'utilization'
    id = Column(Integer, primary_key=True)
    cpu = Column(Float, nullable=False)
    mem = Column(Float, nullable=False)
    net = Column(Float, nullable=False)
    sto = Column(Float, nullable=False)
    bat = Column(Float, nullable=False)
    datetime = Column(String, nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'), nullable=False)

    def __repr__(self):
        return f"Utilization('{self.id}', '{self.cpu}', '{self.mem}', '{self.net}', " \
               f"'{self.sto}', '{self.bat}', '{self.datetime}')"


engine = create_engine('sqlite:///:memory:')
# engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


# session = Session()
# u = Server(node_ip='192.168.1.1')
# a = Utilization(cpu=20.1, mem=11.1, net=12.1, sto=10.5, bat=30.33, datetime='12/06/COM2021', server_id=1)
# session.add(u)
# session.add(a)
# session.commit()
#
# us = session.query(Server).all()
# print(us)
# print(us[0].util)
#
# # t = session.query(Server).filter_by(node_ip='192.168.1.1').all()
# t = session.query(Server).filter_by(node_ip='192.168.1.1').first()
# print(t)
# t = session.query(Server).filter_by(node_ip='192.168.1.2').first()
# print(f'here: {t}')
# session.close()


class Database:
    def __init__(self):
        self.session = Session()

    def is_node(self, node):
        """
        checks if node is in database
        :param node: str ip_address
        :return: node id or False
        :rtype: bool or str
        """
        query = self.session.query(Server).filter_by(node_ip=node).first()
        if query:
            return query.id
        else:
            return False

    def add_data(self, data):
        """

        :param data:{
                'node_ip': '1.2.3.4',
                't_stamp': '1234',
                'util':{
                        'cpu': 10,
                        'mem': 20,
                        'net': 30,
                        'sto': 40,
                        'bat': 50
                        }
                }
        :return: True or False
        :rtype: bool
        """
        try:
            server_id = self.is_node(data['node_ip'])
            if not server_id:
                self.session.add(Server(node_ip=data['node_ip']))
                self.session.commit()
                server_id = self.is_node(data['node_ip'])
            util = data['util']
            self.session.add(Utilization(cpu=util['cpu'],
                                         mem=util['mem'],
                                         net=util['net'],
                                         sto=util['sto'],
                                         bat=util['bat'],
                                         datetime=f"{data['t_stamp']}",
                                         server_id=server_id))
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def fetch_data(self, node):
        server_obj = self.session.query(Server).filter_by(node_ip=node).first()
        if server_obj:
            return server_obj.util
        else:
            return None
