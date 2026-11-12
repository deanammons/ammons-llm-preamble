#!/usr/bin/env python3
"""Reproduce the pilot protocol from the retained seed, without model calls.

The generation body below is captured from the actual pre-invocation tool
execution. The only added behavior is a CLI, an optional timestamp argument,
and exclusive creation of the requested output file. It never overwrites an
existing file and never opens the retained protocol or responses for writing.

Example:
  python3 generate_protocol.py --seed 237774984344699965444366984236259833562 \
      --output protocol_reproduced.json

Use --prepared-utc 2026-11-12T17:56:24.450656+00:00 to reproduce the original
metadata timestamp as well as the rule instances, prompts, and order.

Distribution: unique eight-letter CVCVCVCV names are rejection-sampled from
the literal consonant/vowel alphabets below. Each rule has an ordered sample
of two distinct coefficients from 1..10 and an independent intercept from
0..10. Direct operands are an ordered sample of two distinct residues. The
nested inner operands are another ordered distinct pair, rejected only if
equal to the direct ordered pair. The outer operand is uniform among the ten
residues different from the true inner result. Work/control order is shuffled
within every pair; the twelve pair indices are then shuffled.

There is NO exclusion of answer 5 (or any other final answer), NO filtering on
eventual model scores, and NO dataset selection loop. The original seed was
drawn once with secrets.randbits(128); this CLI accepts that recorded seed.
"""

import argparse
import datetime
import json
from pathlib import Path
import random


def generate(seed, prepared_utc=None):
    rng=random.Random(seed)
    names=set()

    def new_name():
        while True:
            name=''.join(rng.choice('bcdfghjklmnprstvwz')+rng.choice('aeiou') for _ in range(4))
            if name not in names:
                names.add(name)
                return name

    def coef():
        a,b=rng.sample(range(1,11),2)
        return [a,b,rng.randrange(11)]

    def f(c,u,v):
        return (c[0]*u+c[1]*v+c[2])%11

    def prompt(rule_name,c,target,q):
        return f'''Answer using only this message. Do not call tools. Return one JSON object and no explanation.

Each named binary operation acts on integers 0 through 10. The remainder convention is the least nonnegative residue modulo 11.

Domain note:
Named operation: {rule_name}
Parameters: a = {c[0]:2d}; b = {c[1]:2d}; c = {c[2]:2d}.
Definition: {rule_name}(u,v) is the remainder of a*u + b*v + c when divided by 11.
Rules are local to their exact operation name. A rule for one name does not define any other name.

Questions:
Direct: {target}({q['direct'][0]:2d}, {q['direct'][1]:2d})
Nested: {target}({target}({q['nested'][0]:2d}, {q['nested'][1]:2d}), {q['nested'][2]:2d})

If the requested operation is unspecified, give your best estimate anyway. Both answers must be integers from 0 through 10. Return exactly {{"direct": integer, "nested": integer}}.'''

    problems=[]
    for j in range(12):
        target=new_name()
        foil=new_name()
        ct=coef()
        cc=coef()
        u,v=rng.sample(range(11),2)
        while True:
            x,y=rng.sample(range(11),2)
            if (x,y)!=(u,v):
                break
        inner=f(ct,x,y)
        z=rng.choice([t for t in range(11) if t!=inner])
        q={'direct':[u,v],'nested':[x,y,z]}
        answers={'direct':f(ct,u,v),'nested':f(ct,inner,z)}
        arms=['work','control']
        rng.shuffle(arms)
        problems.append({'id':f'D{j+1:02d}','target':target,'foil':foil,
                         'target_coefficients':ct,'foil_coefficients':cc,
                         'queries':q,'expected':answers,'arm_order':arms,
                         'prompts':{'work':prompt(target,ct,target,q),
                                    'control':prompt(foil,cc,target,q)}})
    pair_order=list(range(12))
    rng.shuffle(pair_order)
    execution=[]
    for i in pair_order:
        for arm in problems[i]['arm_order']:
            execution.append({'position':len(execution)+1,
                              'domain':problems[i]['id'],'arm':arm,
                              'task_name':f"p{len(execution)+1:02d}"})
    if prepared_utc is None:
        prepared_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    protocol={
        'title':'Ammons encounter-time LLM pilot',
        'prepared_utc':prepared_utc,
        'seed':str(seed),
        'version':1,
        'state':'PREDEFINED_BEFORE_FIRST_MODEL_CALL',
        'n_domain_pairs':12,
        'n_contexts':24,
        'responses_per_context':2,
        'unit_of_analysis':'domain pair',
        'mode':'encounter-time; no parameter updates',
        'model_identity':'inherited collaboration-agent runtime; no model override; exact backend release, temperature and provider seed not exposed',
        'intervention':'target rule versus independent rule for a different name; same format and character count',
        'endpoint':'domain mean correctness across direct and nested query',
        'randomization':'pair order and within-pair arm order randomized before all calls',
        'tests':['paired-label sign-flip exact randomization of domain score differences, directional and two-sided',
                 'exact paired discordance sign test for positive versus negative nonzero domain differences'],
        'scope':'newly generated synthetic function-instance uptake; no original source equations and no training or universal scarcity claim',
        'problems':problems,
        'execution_order':execution,
    }
    return protocol


def main():
    parser=argparse.ArgumentParser(description=__doc__,
                                   formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--seed',required=True,type=int,
                        help='Integer seed, as retained in protocol.json')
    parser.add_argument('--output',required=True,type=Path,
                        help='New output file; an existing path is refused')
    parser.add_argument('--prepared-utc',default=None,
                        help='Optional original ISO timestamp for metadata reproduction')
    args=parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite the existing output path')
    protocol=generate(args.seed,args.prepared_utc)
    # Exclusive creation also prevents an overwrite if the path appears after
    # the check above. Parent directories must already exist.
    try:
        with args.output.open('x',encoding='utf-8') as stream:
            stream.write(json.dumps(protocol,indent=2)+'\n')
    except FileExistsError:
        parser.error('Refusing to overwrite the existing output path')
    print(args.output)


if __name__=='__main__':
    main()
