"""当前来源接口的核心和错误路径。"""
import unittest,tempfile
from pathlib import Path
from common import read,Releases,money,digest

class CommonTests(unittest.TestCase):
    def test_snapshot_and_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            store=Releases(d);raw={'value':'20.10'};key=store.publish(raw)
            self.assertEqual(store.open(key),raw);self.assertEqual(store.publish(raw),key)
            Path(d,key).write_bytes(b'changed')
            with self.assertRaises(ValueError):store.open(key)
    def test_exact_money(self):
        self.assertEqual(str(money('0.1')+money('0.2')),'0.3')
        with self.assertRaises(ValueError):money(float('nan'))

from transactions import purchases
from history import histories,future_labels
class DomainTests(unittest.TestCase):
    def test_future_refund_hidden(self):
        d=read();self.assertEqual(purchases(d,100)[1]['net'],'30');self.assertEqual(purchases(d,120)[1]['net'],'20')
        self.assertEqual(histories(d,100)[1]['frequency'],0)
        labels=future_labels(d,100,90,200);self.assertIsNone(labels[2]['count']);self.assertEqual(labels[0]['count'],0)
    def test_refund_overflow(self):
        d=read();d['transactions'][-1]['amount']='100'
        with self.assertRaises(ValueError):purchases(d,120)
