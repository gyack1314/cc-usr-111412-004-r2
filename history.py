"""客户观察范围、历史摘要和有完整随访的评估标签。"""
from transactions import purchases
from common import money

def histories(data,asof):
    ps=purchases(data,asof);out=[];seen=set()
    for c in data['customers']:
        if c['id'] in seen or c['coverage_end']<c['joined']:raise ValueError('客户观察范围非法')
        seen.add(c['id'])
        if c['joined']>asof:continue
        end=min(asof,c['coverage_end']);rows=[p for p in ps if p['customer']==c['id'] and c['joined']<=p['time']<=end]
        out.append({'customer':c['id'],'age':end-c['joined'],'frequency':len(rows),'last':max((p['time'] for p in rows),default=None),'net':str(sum((money(p['net']) for p in rows),money('0'))),'observed_through':end,'orders':[p['order'] for p in rows]})
    if any(p['customer'] not in seen for p in ps):raise ValueError('付款客户未在名册')
    return out

def future_labels(data,decision,horizon,evaluation_asof):
    end=decision+horizon;ps=purchases(data,evaluation_asof);out=[]
    for c in data['customers']:
        if c['joined']>decision:continue
        complete=c['coverage_end']>=end and evaluation_asof>=end
        rows=[p for p in ps if p['customer']==c['id'] and decision<p['time']<=end]
        out.append({'customer':c['id'],'complete':complete,'count':len(rows) if complete else None,'net':str(sum((money(p['net']) for p in rows),money('0'))) if complete else None})
    return out
