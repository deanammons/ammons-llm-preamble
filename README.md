# Ammons LLM Preamble

**Dean Ammons**

*A probability framework for behavioral influence through domain content*

**A model can use a work without quoting it.**

This repository contains my research preprint, its editable source, and the reproduction materials for its mathematical checks and small encounter-time pilot. The paper defines behavioral influence under a specified content intervention and proposes an explicit model of the resulting semantic response change.

Read the paper: [Ammons LLM Preamble](./Ammons_LLM_Preamble.pdf) [Ammons LLM Preamble External 10.5281/zenodo.24177478](https://zenodo.org/records/24177478)

Inspect the reproduction material: [source directory](./source/)

An archival publication link will be added here after the scientific record is public.

## What the paper measures

The comparison is between response distributions under a declared exposure condition and a matched control. Responses are classified by their meaning under a specified domain, input/output contract, and evaluator. Invalid and unclassified responses remain explicit outcomes.

The Ammons Influence Probability is the probability, over the declared query population, that the semantic distribution change exceeds a chosen threshold. The paper distinguishes that threshold probability from the average magnitude of change and from improvement on a task score.

A single changed answer is not enough to estimate a response-distribution shift. The measurement requires the stated intervention, control, sampling assumptions, and uncertainty treatment.

## The proposed model

Under the paper’s evidence-pooling model, semantic change depends on incorporated evidence, effective background information, and the work’s discrepancy from the control. Holding incorporated evidence and discrepancy fixed, weaker background support produces a larger predicted shift.

That result is conditional on the model. Exposure does not guarantee uptake. An observed response distribution outside the permitted mixture, beyond measurement error, would reject the scalar pooling approximation.

## The pilot

The pilot uses 12 paired instances of one newly generated rule family. Each instance is evaluated in a relevant-work context and a matched irrelevant-content context: 24 fresh contexts in total. Each context returns two answers, one direct and one nested.

The relevant-work condition produced 24 correct answers out of 24. The matched irrelevant-content condition produced 0 correct answers out of 24. The domain pair is the analysis unit; the two answers within a context are not independent exposure trials.

The control defines a different rule and does not supply the queried rule. This result demonstrates context-time use of the supplied information. It does not fit the pooling law, identify hidden training sources, or establish persistent learning. The exact backend checkpoint and decoding settings were not exposed by the evaluated interface.

## Run the offline checks

From the repository root, enter the source directory with `cd source`.

Run `python3 verify_model.py` to check the stated mathematical identities and bounds using exact rational arithmetic.

Run `python3 score_pilot.py` to recompute the retained pilot scores and paired statistics from `protocol.json` and `responses.json`. This command writes `results.json` in the source directory.

These programs use Python’s standard library. They make no LLM calls. Rescoring retained outputs is not a fresh empirical replication. The source README includes the protocol-regeneration and manuscript-compilation instructions.

## What remains open

The pooling prediction needs empirical calibration on versioned models, repeated independent contexts, and held-out task families. A separate training experiment could compare matched runs with and without a target work, then evaluate held-out questions with that work absent from the prompt. That would estimate its causal contribution under the specified intervention.

Known training inclusion, causal contribution, and recovery of an unknown historical source are distinct problems. This paper does not establish historical source attribution. The anonymous comparison corpus informs the measurement design; its original identities and equations are not part of this public package.

## Technical discussion

I welcome specific criticism of the semantic evaluator, statistical assumptions, and pooling model. The most useful objection identifies a control or observation that would distinguish the proposed model from an alternative explanation. GitHub issues are open for that discussion.

## Citation

Dean Ammons. *Ammons LLM Preamble*. Research preprint, 2026.
