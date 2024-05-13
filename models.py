from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float,Date
from sqlalchemy.orm import relationship

from database import Base


class customer_request(Base):
    __tablename__ = "customer_request"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    contact_email = Column(String)
    customer_input_date = Column(Date)
    customer_input_address = Column(String)
    content = Column(String)
    url = Column(String)

