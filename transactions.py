"""只使用已知付款和退款的有效购买表。"""
from common import money

def purchases(data,asof):
    events={};orders={}
    for e in data['transactions']:
        if e['known']>asof or e['time']>asof:continue
        if e['event'] in events:
            if events[e['event']]!=e:raise ValueError('支付事件冲突')
            continue
        events[e['event']]=e
    for e in sorted(events.values(),key=lambda e:(e['time'],e['event'])):
        n=money(e['amount']);k=e['order']
        if n<0:raise ValueError('支付金额负数')
        if e['kind']=='paid':
            if k in orders:raise ValueError('订单重复支付')
            orders[k]={'order':k,'customer':e['customer'],'time':e['time'],'net':n,'events':[e['event']]}
        elif e['kind']=='refund':
            if k not in orders or orders[k]['customer']!=e['customer'] or orders[k]['net']<n:raise ValueError('退款无来源或超额')
            orders[k]['net']-=n;orders[k]['events'].append(e['event'])
        else:raise ValueError('支付事件类型未知')
    return [dict(r,net=str(r['net'])) for r in orders.values() if r['net']>0]
