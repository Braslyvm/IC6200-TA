from itertools import combinations



PROBS = {

    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    "trait": {
        2: {
            True  : 0.65,
            False: 0.35
        },
        1: {
            True: 0.56,
            False: 0.44
        },
        0: {
            True: 0.01,
            False: 0.99
        }
    },
    "mutation": 0.01
}

def powerset(s):
    result = []
    for i in range(len(s) + 1):
        for combo in combinations(s, i):
            result.append(set(combo))

    return result


def joint_probability(people, one_gene, two_genes, have_trait):
    probability = 1

    for person in people:
        if person in two_genes:
            gene = 2
        elif person in one_gene:
            gene = 1
        else:
            gene = 0

        trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]

        if mother is None and father is None:
            gene_probability = PROBS["gene"][gene]
        else:
            def parent_pass(parent):
                if parent in two_genes:
                    return 1 - PROBS["mutation"]
                elif parent in one_gene:
                    return 0.5
                else:
                    return PROBS["mutation"]

            mother_pass = parent_pass(mother)
            father_pass = parent_pass(father)

            if gene == 2:
                gene_probability = mother_pass * father_pass
            elif gene == 1:
                gene_probability = (
                    mother_pass * (1 - father_pass)
                    + (1 - mother_pass) * father_pass
                )
            else:
                gene_probability = (1 - mother_pass) * (1 - father_pass)

        trait_probability = PROBS["trait"][gene][trait]
        probability *= gene_probability * trait_probability

    return probability


def calculate_probabilities(people):
    """
    Calculate normalized gene and trait probability distributions for each person.

    Input:
        people = {
            "Person": {"mother": None, "father": None, "trait": None}
        }

    Output:
        {
            "Person": {
                "gene": {2: 0.01, 1: 0.03, 0: 0.96},
                "trait": {True: 0.0329, False: 0.9671}
            }
        }
    """
    probabilities = {
        person: {
            "gene": {2: 0, 1: 0, 0: 0},
            "trait": {True: 0, False: 0}
        }
        for person in people
    }

    names = set(people)

    for have_trait in powerset(names):

        fails_evidence = any(
            people[person]["trait"] is not None
            and people[person]["trait"] != (person in have_trait)
            for person in names
        )

        if fails_evidence:
            continue

        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    normalize(probabilities)
    return probabilities





def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to probabilities a new joint probability p.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in have_gene and have_trait, respectively.

    Input:
        probabilities = {
            "Harry": {
                "gene": {2: 0, 1: 0, 0: 0},
                "trait": {True: 0, False: 0}
            }
        }
        one_gene = {"Harry"}
        two_genes = set()
        have_trait = {"Harry"}
        p = 0.5

    Output:
        {
            "Harry": {
                "gene": {2: 0, 1: 0.5, 0: 0},
                "trait": {True: 0.5, False: 0}
            }
        }
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p  

def normalize(probabilities):
    """
    Update probabilities such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).

    Input:
        probabilities = {
            "Harry": {
                "gene": {2: 2, 1: 2, 0: 6},
                "trait": {True: 1, False: 3}
            }
        }

    Output:
        {
            "Harry": {
                "gene": {2: 0.2, 1: 0.2, 0: 0.6},
                "trait": {True: 0.25, False: 0.75}
            }
        }
    """
    for person in probabilities:
        gene_total = sum(probabilities[person]["gene"].values())
        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] /= gene_total

        trait_total = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= trait_total













