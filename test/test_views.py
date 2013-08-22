# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek

import unittest
import transaction

from pyramid import testing

from feedduty.models import DBSession


class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from feedduty.models import (
            BaseModel,
            MyModel,
            )
        DBSession.configure(bind=engine)
        BaseModel.metadata.create_all(engine)
        with transaction.manager:
            model = MyModel(name='one', value=55)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from feedduty.views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'dashboards')
