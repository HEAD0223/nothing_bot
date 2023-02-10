import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, Boolean, String, DateTime
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

load_dotenv()

host = str(os.getenv("HOST"))
password = str(os.getenv("PASSWORD"))
database = str(os.getenv("DATABASE"))

engine = create_engine(f"postgresql+psycopg2://postgres:{password}@{host}/{database}")

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = 'users'

    id          = Column(BigInteger, primary_key=True)
    username    = Column(String)
    name        = Column(String)
    amount      = Column(Integer, default=0)
    created_at  = Column(DateTime, default=None)
    request     = Column(Boolean, default=False)
    currency    = Column(Integer, default=0)
    withdrawal  = Column(Integer, default=0)
    support     = Column(Boolean, default=False)
    sp_ticket   = Column(Integer)
    referrer_id = Column(String, default=None)
    referral_id = Column(String, default=None)
    buy_amount  = Column(Integer)
    payment_id  = Column(String)
    card_number = Column(String)
    card_month  = Column(Integer)
    card_year   = Column(Integer)
    card_cvv2   = Column(Integer)
    card_fl     = Column(String)
    language    = Column(String)
    admin       = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)