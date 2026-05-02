from cps_backtracking.csp import backtracking, initialize


# variables <- list of courses
# domain <- list of possible days
# constraints <- list of incompatibilities


# function main
#     courses <- initialize(variables, domain)
#     first course <- first element of courses
#     remaining courses <- all elements except the first
#     assigned courses <- empty list

#     if backtracking(first course, remaining courses, assigned courses, constraints)
#         for each course in courses
#             print the name and assigned value of the course
#     otherwise
#         print "No solution found"


# run main
variables = ["A", "B", "C", "D", "E", "F", "G"]
domain = ["Monday", "Tuesday", "Wednesday"]
constraints = [
    "A!=B",
    "A!=C",
    "B!=C",
    "B!=D",
    "B!=E",
    "C!=E",
    "C!=F",
    "D!=E",
    "E!=F",
    "E!=G",
    "F!=G",
]




def main ():
    courses = initialize(variables ,domain)
    first= courses[0]
    remaining = courses[1:]
    assigned = []
    if backtracking(first, remaining, assigned, constraints):
        for course in courses:
            print(f"{course['name']}: {course['value']}")
    else:
        print("No solution found")
        