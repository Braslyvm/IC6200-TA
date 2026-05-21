import pytest

from probability import (
    PROBS,
    calculate_probabilities,
    joint_probability,
    normalize,
    powerset,
    update,
)


def test_probs_contains_expected_values():
    assert PROBS == {
        "gene": {2: 0.01, 1: 0.03, 0: 0.96},
        "trait": {
            2: {True: 0.65, False: 0.35},
            1: {True: 0.56, False: 0.44},
            0: {True: 0.01, False: 0.99},
        },
        "mutation": 0.01,
    }


def test_powerset_handles_empty_set():
    assert powerset(set()) == [set()]


def test_powerset_returns_all_subsets():
    result = {frozenset(subset) for subset in powerset({"Alice", "Bob"})}

    assert result == {
        frozenset(),
        frozenset({"Alice"}),
        frozenset({"Bob"}),
        frozenset({"Alice", "Bob"}),
    }


@pytest.mark.parametrize(
    ("one_gene", "two_genes", "have_trait", "expected"),
    [
        (set(), {"Person"}, {"Person"}, 0.01 * 0.65),
        ({"Person"}, set(), set(), 0.03 * 0.44),
        (set(), set(), {"Person"}, 0.96 * 0.01),
    ],
)
def test_joint_probability_uses_unconditional_gene_probabilities_for_founders(
    one_gene,
    two_genes,
    have_trait,
    expected,
):
    people = {"Person": {"mother": None, "father": None}}

    assert joint_probability(people, one_gene, two_genes, have_trait) == pytest.approx(
        expected
    )


@pytest.mark.parametrize(
    ("one_gene", "two_genes", "have_trait", "expected"),
    [
        (set(), {"Mother", "Father", "Child"}, {"Child"}, 0.99 * 0.99 * 0.65),
        ({"Child"}, {"Mother"}, set(), (0.99 * 0.99 + 0.01 * 0.01) * 0.44),
        ({"Mother"}, set(), {"Child"}, 0.5 * 0.99 * 0.01),
    ],
)
def test_joint_probability_applies_parent_inheritance_and_mutation(
    one_gene,
    two_genes,
    have_trait,
    expected,
):
    people = {"Child": {"mother": "Mother", "father": "Father"}}

    assert joint_probability(people, one_gene, two_genes, have_trait) == pytest.approx(
        expected
    )


def test_update_adds_probability_to_matching_gene_and_trait_buckets():
    probabilities = {
        "Alice": {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}},
        "Bob": {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}},
        "Charlie": {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}},
    }

    update(
        probabilities,
        one_gene={"Bob"},
        two_genes={"Alice"},
        have_trait={"Alice", "Charlie"},
        p=0.25,
    )

    assert probabilities == {
        "Alice": {
            "gene": {2: 0.25, 1: 0, 0: 0},
            "trait": {True: 0.25, False: 0},
        },
        "Bob": {
            "gene": {2: 0, 1: 0.25, 0: 0},
            "trait": {True: 0, False: 0.25},
        },
        "Charlie": {
            "gene": {2: 0, 1: 0, 0: 0.25},
            "trait": {True: 0.25, False: 0},
        },
    }


def test_normalize_preserves_ratios_and_makes_distributions_sum_to_one():
    probabilities = {
        "Person": {
            "gene": {2: 2, 1: 3, 0: 5},
            "trait": {True: 1, False: 3},
        }
    }

    normalize(probabilities)

    assert probabilities["Person"]["gene"] == pytest.approx({2: 0.2, 1: 0.3, 0: 0.5})
    assert probabilities["Person"]["trait"] == pytest.approx(
        {True: 0.25, False: 0.75}
    )
    assert sum(probabilities["Person"]["gene"].values()) == pytest.approx(1)
    assert sum(probabilities["Person"]["trait"].values()) == pytest.approx(1)


def test_calculate_probabilities_for_single_founder_with_unknown_trait():
    people = {"Person": {"mother": None, "father": None, "trait": None}}

    probabilities = calculate_probabilities(people)

    assert probabilities["Person"]["gene"] == pytest.approx(PROBS["gene"])
    assert probabilities["Person"]["trait"] == pytest.approx(
        {True: 0.0329, False: 0.9671}
    )


@pytest.mark.parametrize(
    ("known_trait", "expected_trait"),
    [
        (True, {True: 1, False: 0}),
        (False, {True: 0, False: 1}),
    ],
)
def test_calculate_probabilities_respects_known_trait_evidence(
    known_trait,
    expected_trait,
):
    people = {"Person": {"mother": None, "father": None, "trait": known_trait}}

    probabilities = calculate_probabilities(people)

    assert probabilities["Person"]["trait"] == pytest.approx(expected_trait)
