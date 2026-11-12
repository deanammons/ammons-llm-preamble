AMMONS LLM PREAMBLE
Dean Ammons
Research preprint, 12 November 2026

This folder contains the editable LaTeX manuscript, its figures, and the
standard-library programs and retained observations used in the paper.
It contains no original source equations or identities from the anonymous
mathematical comparison corpus. The modulo-11 rules are newly generated
experimental surrogates.

OFFLINE REPRODUCTION
  python3 verify_model.py
  python3 score_pilot.py

The first command checks the mathematical pooling identities with exact
rational arithmetic. The second recomputes every pilot answer and exact paired
statistic from protocol.json and responses.json, writing results.json.
Neither command calls an LLM or simulates model responses.

REGENERATE THE PROTOCOL
  python3 generate_protocol.py --seed 237774984344699965444366984236259833562 --prepared-utc 2026-11-12T17:56:24.450656+00:00 --output NEW_PROTOCOL_FILE.json

The destination must not already exist. The program reproduces the original
specifications, keys, planned prompts, and randomized order from the retained
seed. It does not query a model. Unique operation names and nondegenerate query
constraints are documented in the generator. There was no filtering of final
answer 5 or selection based on model scores.

OBSERVED DATA
The pilot has 12 paired domain instances, 24 fresh LLM contexts, and two answers
per context. The domain pair is the analysis unit. All control outputs were
(5,5); none of the pre-generated keys was 5. One actual work prompt for D06
omitted one formatting space; responses.json retains its actual_prompt and
deviation note. That invocation was not repeated. No other planned condition
or stopping rule changed.

Internal session paths and response recording timestamps have been removed.
Generic invocation labels, randomized order, actual response strings, prompt
overrides, generated specifications, and all score inputs are retained.

COMPILE THE MANUSCRIPT
On a standard TeX Live installation with the packages named in the preamble:
  pdflatex Ammons_LLM_Preamble.tex
  pdflatex Ammons_LLM_Preamble.tex
The two vector PDF figures are already provided. No bibliography processor,
network access, or shell escape is required.

INTERPRETATION
The paper distinguishes proved mathematics, a falsifiable pooling surrogate,
an anonymous semantic instrument-development corpus, and an observed context
pilot. The training derivation is analytical; no new weight-update experiment
is reported. Exact backend model release, temperature, and sampling seed were
not exposed. Fresh model responses may differ on another interface or run.
The exploratory probability bound concerns the fixed 12-domain benchmark,
conditional on independent response pairs and a stable interface.
