# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
from cucumber.entities import Order, OrderEvent
from datetime import datetime, timedelta

def test_latest_order_event():
    now = datetime.utcnow()
    order = Order(latest_status=None, created_at=now, updated_at=now)
    assert order.latest_order_event is None

    order.order_events.append(OrderEvent(id=1, status='引き取り待機', created_at=now))
    order.latest_status = '引き取り待機'
    assert order.latest_order_event.id == 1

    order.order_events.append(OrderEvent(id=2, status='引き取り完了', created_at=now + timedelta(hours=1)))
    order.latest_status = '引き取り完了'
    assert order.latest_order_event.id == 2

    order.order_events.append(OrderEvent(id=3, status='仕入れ待機', created_at=now + timedelta(hours=2)))
    order.latest_status = '仕入れ待機'
    assert order.latest_order_event.id == 3

    order.order_events.append(OrderEvent(id=4, status='引き取り完了', created_at=now + timedelta(hours=3)))
    order.latest_status = '引き取り完了'
    assert order.latest_order_event.id == 4

    order.latest_status = '整合性破壊'
    with pytest.raises(RuntimeError):
        order.latest_order_event
