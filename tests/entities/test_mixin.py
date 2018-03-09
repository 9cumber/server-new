# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
import cucumber.entities
from mock import patch
from sqlalchemy import BINARY, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.ext.declarative import declarative_base
from tests.conftest import DBCreatorFromSession

Base = declarative_base()
class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)

class DataFetchQueryMixin(Data, cucumber.entities.FetchQueryMixin):
    pass


def setup_data_seed(Session):
    session = Session()
    Base.metadata.create_all(session.get_bind())
    session.add_all([Data(id=1), Data(id=2)])
    session.commit()

def test_fetch_mixin_fetch(Session):
    setup_data_seed(Session)
    with patch('cucumber.entities.db', new_callable=DBCreatorFromSession(Session)):
        fetch_query_mixin = DataFetchQueryMixin()
        assert fetch_query_mixin.fetch(1).id == 1
        assert fetch_query_mixin.fetch(2).id == 2
        fetch_query_mixin.fetch(3)

def test_fetch_mixin_fetch_all(Session):
    setup_data_seed(Session)
    with patch('cucumber.entities.db', new_callable=DBCreatorFromSession(Session)):
        fetch_query_mixin = DataFetchQueryMixin()
        result = fetch_query_mixin.fetch_all()
        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
