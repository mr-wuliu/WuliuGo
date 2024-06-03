from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy

from sqlalchemy import (
    Column, ForeignKey,
    Integer, String, DateTime, Boolean, Numeric, Text
)

class SQLAlchemy(BaseSQLAlchemy):
    Column = Column
    ForeignKey = ForeignKey
    Integer = Integer
    String = String
    DateTime = DateTime
    Boolean = Boolean
    Numeric = Numeric
    Text = Text
    # relationship = relationship
