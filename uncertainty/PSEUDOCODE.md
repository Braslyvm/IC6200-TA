# Pseudocode — Heredity

## utils.py

### load_data(filename)

```
FUNCTION load_data(filename):
    data ← empty dictionary

    OPEN filename as CSV file:
        FOR each row in CSV:
            name   ← row["name"]
            mother ← row["mother"]  OR None if blank
            father ← row["father"]  OR None if blank
            trait  ← True  if row["trait"] == "1"
                     False if row["trait"] == "0"
                     None  otherwise (unknown)

            data[name] ← { name, mother, father, trait }

    RETURN data
```

---

## probability.py

### Constants (PROBS)

```
PROBS = {
    gene:     { 2: 0.01, 1: 0.03, 0: 0.96 }   // prior probs for 2/1/0 gene copies
    trait:    { 2: {T:0.65, F:0.35},             // P(trait | gene count)
                1: {T:0.56, F:0.44},
                0: {T:0.01, F:0.99} }
    mutation: 0.01                               // chance a gene copy mutates during transmission
}
```

### powerset(s)

```
FUNCTION powerset(s):
    // Returns all subsets of s (including empty set and s itself)
    result ← []
    FOR r FROM 0 TO |s|:
        FOR each combination of r elements from s:
            result.append(that combination as a set)
    RETURN result
```

### joint_probability(people, one_gene, two_genes, have_trait)

```
FUNCTION joint_probability(people, one_gene, two_genes, have_trait):
    probability ← 1

    FOR each person in people:
        genes     ← 2 if person in two_genes
                    1 if person in one_gene
                    0 otherwise
        has_trait ← person in have_trait
        mother    ← people[person].mother
        father    ← people[person].father

        IF mother is None AND father is None:
            // No parents known — use unconditional gene probability
            gene_probability ← PROBS["gene"][genes]
        ELSE:
            // Compute probability each parent passes the gene
            FOR each parent in {mother, father}:
                parent_genes ← 2 / 1 / 0 (same lookup as above)

                IF parent_genes == 2:
                    pass_prob ← 1 - PROBS["mutation"]   // almost certainly passes it
                ELSE IF parent_genes == 1:
                    pass_prob ← 0.5                      // 50/50
                ELSE:
                    pass_prob ← PROBS["mutation"]        // almost certainly doesn't pass it

            // passes = [prob_from_mother, prob_from_father]
            IF genes == 2:
                gene_probability ← passes[0] * passes[1]
            ELSE IF genes == 1:
                gene_probability ← passes[0]*(1-passes[1]) + (1-passes[0])*passes[1]
            ELSE:
                gene_probability ← (1-passes[0]) * (1-passes[1])

        probability ← probability * gene_probability * PROBS["trait"][genes][has_trait]

    RETURN probability
```

### update(probabilities, one_gene, two_genes, have_trait, p)

```
FUNCTION update(probabilities, one_gene, two_genes, have_trait, p):
    FOR each person in probabilities:
        genes     ← 2 / 1 / 0  (same lookup)
        has_trait ← person in have_trait

        probabilities[person]["gene"][genes]      += p
        probabilities[person]["trait"][has_trait] += p
```

### normalize(probabilities)

```
FUNCTION normalize(probabilities):
    FOR each person in probabilities:
        FOR each field in {"gene", "trait"}:
            total ← sum of all values in probabilities[person][field]
            FOR each value in that distribution:
                probabilities[person][field][value] /= total
```

### calculate_probabilities(people)

```
FUNCTION calculate_probabilities(people):
    // Initialize all gene/trait accumulators to 0
    probabilities ← { person: { gene:{2:0,1:0,0:0}, trait:{T:0,F:0} }
                      for each person }
    names ← set of all person names

    FOR each subset have_trait of names:
        // Skip if contradicts known evidence
        IF any person has known trait that differs from (person in have_trait):
            CONTINUE

        FOR each subset one_gene of names:
            FOR each subset two_genes of (names - one_gene):
                p ← joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    normalize(probabilities)

    RETURN probabilities
```
