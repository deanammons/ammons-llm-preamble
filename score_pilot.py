#!/usr/bin/env python3
"""Recompute the exact paired pilot statistics from retained real outputs.

No packages, model calls, or network access are required. The program never
generates model responses. Use --record to append an observed final response:
  python3 score_pilot.py --record <<'JSON'
  {"task_name":"p01", "response":"...exact final response..."}
  JSON
Run without arguments to regenerate results.json and print the summary.
"""
import argparse
import datetime
import itertools
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

def apply_rule(coefficients, u, v):
    a, b, c = coefficients
    return (a*u+b*v+c) % 11

def expected(problem):
    direct = problem['queries']['direct']
    x,y,z = problem['queries']['nested']
    c = problem['target_coefficients']
    return {'direct':apply_rule(c,*direct),
            'nested':apply_rule(c,apply_rule(c,x,y),z)}

def score_response(text, truth):
    try:
        parsed = json.loads(text)
        valid = (isinstance(parsed, dict) and set(parsed)=={'direct','nested'}
                 and all(type(parsed[k]) is int and 0<=parsed[k]<=10 for k in truth))
    except (TypeError, ValueError):
        parsed = None
        valid = False
    correctness = {k:int(valid and parsed[k]==v) for k,v in truth.items()}
    return {'parsed':parsed,'valid_format':valid,'correct':correctness,
            'n_correct':sum(correctness.values()),'mean_correct':sum(correctness.values())/2}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--record',action='store_true')
    args=ap.parse_args()
    protocol=json.loads((ROOT/'protocol.json').read_text())
    responses=json.loads((ROOT/'responses.json').read_text())
    execution={x['task_name']:x for x in protocol['execution_order']}
    problems={x['id']:x for x in protocol['problems']}
    if args.record:
        new=json.load(sys.stdin)
        name=new['task_name']
        if name not in execution: raise ValueError('Unplanned task name')
        if any(r['task_name']==name for r in responses):
            raise ValueError('Response already recorded; no overwrite')
        if not isinstance(new['response'],str):raise TypeError('Response must be original text')
        new.update(execution[name])
        new['received_recorded_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        responses.append(new)
        (ROOT/'responses.json').write_text(json.dumps(responses,indent=2)+'\n')
        print(json.dumps({'recorded':name,'n_responses':len(responses)}))
        return
    output_by_domain={}
    for response in responses:
        domain=response['domain']; arm=response['arm']
        if arm in output_by_domain.get(domain,{}):raise ValueError('Duplicated arm')
        truth=expected(problems[domain])
        assert truth==problems[domain]['expected']
        scored=score_response(response['response'],truth)
        output_by_domain.setdefault(domain,{})[arm]=dict(response,**scored)
    pairs=[]
    incomplete=[]
    for domain in sorted(problems):
        observed=output_by_domain.get(domain,{})
        if set(observed)!={'work','control'}:
            incomplete.append({'domain':domain,'observed_arms':sorted(observed)})
            continue
        work,control=observed['work'],observed['control']
        pairs.append({'domain':domain,'expected':expected(problems[domain]),
                      'work':work,'control':control,
                      'delta_count':work['n_correct']-control['n_correct'],
                      'delta_mean':work['mean_correct']-control['mean_correct']})
    n=len(pairs)
    if not n:raise ValueError('No balanced pairs')
    deltas=[x['delta_count'] for x in pairs]
    observed=sum(deltas)
    permuted=[sum(sign*d for sign,d in zip(signs,deltas))
              for signs in itertools.product([-1,1],repeat=n)]
    n_plus=sum(d>0 for d in deltas);n_minus=sum(d<0 for d in deltas)
    n_nonzero=n_plus+n_minus
    if n_nonzero:
        one=sum(math.comb(n_nonzero,k) for k in range(n_plus,n_nonzero+1))/2**n_nonzero
        two=min(1,2*sum(math.comb(n_nonzero,k) for k in range(min(n_plus,n_minus)+1))/2**n_nonzero)
    else:one=two=1.0
    totals={a:sum(p[a]['n_correct'] for p in pairs) for a in ['work','control']}
    by_question={a:{q:sum(p[a]['correct'][q] for p in pairs) for q in ['direct','nested']}
                 for a in ['work','control']}
    summary={'planned_pairs':protocol['n_domain_pairs'],'completed_balanced_pairs':n,
             'n_fresh_contexts_recorded':len(responses),'answers_per_context':2,
             'valid_formats':sum(r[a]['valid_format'] for r in pairs for a in ['work','control']),
             'correct_answers':totals,'answers_per_arm':2*n,
             'mean_accuracy':{a:totals[a]/(2*n) for a in totals},
             'paired_mean_change':observed/(2*n),
             'per_question_correct':by_question,
             'positive_pairs':n_plus,'negative_pairs':n_minus,'zero_pairs':n-n_nonzero,
             'exact_paired_label_test':{'statistic':'sum of within-domain correct-count differences',
                                      'observed':observed,'assignments':len(permuted),
                                      'directional_p':sum(t>=observed for t in permuted)/len(permuted),
                                      'two_sided_p':sum(abs(t)>=abs(observed) for t in permuted)/len(permuted)},
             'exact_sign_test':{'directional_p':one,'two_sided_p':two,'n_nonzero':n_nonzero},
             'incomplete_pairs':incomplete,
             'assumptions':'Paired-label exchangeability under a sharp no-effect null; independent domain-pair units, randomized work/control order; no item-level independence assumption.',
             'scope':'Encounter-time uptake of newly generated function instances, not training or a universal scarcity law.',
             'model_identity':protocol['model_identity']}
    result={'summary':summary,'pairs':pairs}
    (ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
