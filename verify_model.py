#!/usr/bin/env python3
"""Exact rational checks for the declared Ammons evidence-pooling model.

Uses only the Python standard library. These are mathematical model checks,
not LLM observations and not an empirical validation of the pooling assumption.

Run:
    python3 verify_model.py

The JSON on stdout reports the same four primary check counts as the original
execution. Supplementary assertions check the anonymous family weights and
threshold boundary cases within the same existing grid.
"""

from fractions import Fraction as F
import json


def total_variation(p, q):
    """Total variation for equally sized finite rational probability vectors."""
    return sum(abs(x - y) for x, y in zip(p, q)) / 2


def verify():
    vectors = [
        (F(a, 4), F(b, 4), F(4 - a - b, 4))
        for a in range(5)
        for b in range(5 - a)
    ]
    identity = threshold = scarcity = residual = 0

    for baseline in vectors:
        for work in vectors:
            novelty = total_variation(baseline, work)
            for background_mass in (F(1), F(2), F(4)):
                for evidence_mass in (F(0), F(1), F(3), F(8)):
                    weight = evidence_mass / (background_mass + evidence_mass)
                    mixture = tuple(
                        (background_mass * x + evidence_mass * y)
                        / (background_mass + evidence_mass)
                        for x, y in zip(baseline, work)
                    )
                    effect = total_variation(mixture, baseline)
                    assert effect == weight * novelty
                    identity += 1

                    for epsilon in (F(0), F(1, 4), F(1, 2), F(3, 4)):
                        if 0 < epsilon < novelty:
                            assert (effect > epsilon) == (
                                evidence_mass
                                > epsilon * background_mass / (novelty - epsilon)
                            )
                            threshold += 1
                        elif novelty <= epsilon:
                            # The strict materiality threshold is unreachable.
                            assert effect <= epsilon
                        else:
                            # Remaining case: epsilon = 0 and novelty > 0.
                            assert epsilon == 0 and novelty > 0
                            assert (effect > 0) == (evidence_mass > 0)

                    if evidence_mass > 0:
                        assert (
                            evidence_mass
                            * novelty
                            / (2 * background_mass + evidence_mass)
                            <= effect
                        )
                        scarcity += 1

                    for actual_response in vectors:
                        model_discrepancy = total_variation(
                            actual_response, mixture
                        )
                        assert (
                            abs(total_variation(actual_response, baseline) - effect)
                            <= model_discrepancy
                        )
                        residual += 1

    # Nineteen equal-weight dependence groups: one three-entry group,
    # four two-entry groups, and fourteen singleton groups, totaling 25 entries.
    component_weights = [F(1, 57)] * 3 + [F(1, 38)] * 8 + [F(1, 19)] * 14
    assert len(component_weights) == 25
    assert sum(component_weights) == 1
    assert 3 * F(1, 57) == F(1, 19)
    assert 2 * F(1, 38) == F(1, 19)

    results = {
        "scope": "exact rational model verification, not LLM observations",
        "pooling_identities": identity,
        "threshold_cases": threshold,
        "scarcity_comparisons": scarcity,
        "residual_bounds": residual,
        "balanced_components": len(component_weights),
        "balanced_groups": 19,
        "component_weight_sum": str(sum(component_weights)),
        "threshold_boundary_assertions": "included within the existing grid",
    }
    expected = {
        "pooling_identities": 2700,
        "threshold_cases": 3024,
        "scarcity_comparisons": 2025,
        "residual_bounds": 40500,
    }
    assert all(results[key] == value for key, value in expected.items())
    return results


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
