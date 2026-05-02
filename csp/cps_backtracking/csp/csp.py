from collections import deque


class Course:
    def __init__(self, name, domain) -> None:
        self.name = name
        self.domain = domain
        self.value = None

    def assign(self, value):
        self.value = value

    def remove_assignment(self):
        self.value = None

    def __str__(self) -> str:
        return f"{self.name}: {self.value}"


def initialize(variables, domain) -> list[Course]:
    courses = []

    for variable in variables:
        course = Course(name=variable, domain=domain.copy())
        courses.append(course)

    return courses


def is_consistent(course: Course, assigned_courses: list[Course], constraints) -> bool:
    assigned_by_name = {
        assigned_course.name: assigned_course for assigned_course in assigned_courses
    }

    for constraint in constraints:
        left, right = constraint.split("!=")

        if course.name != left and course.name != right:
            continue

        other_name = right if course.name == left else left
        other_course = assigned_by_name.get(other_name)

        if other_course is None or other_course.value is None:
            continue

        if course.value == other_course.value:
            return False

    return True


def backtracking(
    course: Course,
    remaining_courses: list[Course],
    assigned_courses: list[Course],
    constraints: list[str],
) -> bool:
    for day in course.domain:
        course.assign(day)

        if not is_consistent(course, assigned_courses, constraints):
            course.remove_assignment()

            continue

        assigned_courses.append(course)

        if not remaining_courses:
            return True

        next_course = remaining_courses[0]
        next_remaining_courses = remaining_courses[1:]

        if backtracking(
            next_course, next_remaining_courses, assigned_courses, constraints
        ):
            return True

        assigned_courses.pop()
        course.remove_assignment()

    return False


def _neighbors(name: str, constraints: list[str]):
    resultado = []
    for x in constraints:
        left, right = x.split("!=")

        if name == left:
            resultado.append(right)
        elif name == right:
            resultado.append(left)
    return resultado


    #     for each constraint in constraints
    #         left, right <- split the constraint by "!="

    #         if name is equal to left
    #             add right to result
    #         else if name is equal to right
    #             add left to result

    #     return result


def _arc_satisfied(x: str, y: str, X: Course, Y: Course, constraints: list[str]):

    for b in constraints:
        left, right = b.split("!=")
        if (X.name == left and Y.name == right) or (X.name == right and Y.name == left):
            if x == y:
                return False
    return True

    #     for each constraint in constraints
    #         left, right <- split the constraint by "!="

    #         if (X is left and Y is right) or (X is right and Y is left)
    #             if x val is equal to y val
    #                 return false

    #     return true

def revise(X: Course, Y: Course, constraints: list[str]):
    revised = False

    for x_value in X.domain[:]:
        # aquí aplicas el "not" correctamente
        if not any(
            _arc_satisfied(x_value, y_value, X, Y, constraints)
            for y_value in Y.domain
        ):
            X.domain.remove(x_value)
            revised = True

    return revised

    #     revised <- false

    #     for each x in a copy of X domain
    #         if no value y in Y domain satisfies arc satisfied(x, y, X, Y, constraints)
    #             remove x from X domain
    #             revised <- true

    #     return revised


def ac3(courses: list[Course], constraints: list[str]):
    course_map = {course.name: course for course in courses}
    queue = deque()

    for constraint in constraints:
        left, right = constraint.split("!=")

        queue.append((left, right))
        queue.append((right, left))
    while queue:
        x, y = queue.popleft()
        X = course_map[x]
        Y = course_map[y]

        if revise(X, Y, constraints):
            if not X.domain:
                return False

            for z in _neighbors(x, constraints):
                if z != y:
                    queue.append((z, x))
    return True

    #     course map <- dictionary of courses using the name as key
    #     queue <- empty deque

    #     for each constraint in constraints
    #         left, right <- split the constraint by "!="

    #         add (left, right) to queue
    #         add (right, left) to queue

    #     while queue is not empty
    #         x name, y name <- take the first element from queue
    #         X <- course with x name from course map
    #         Y <- course with y name from course map

    #         if revise(X, Y, constraints)
    #             if X domain is empty
    #                 return false
    #             for each z name in neighbors(x name, constraints)
    #                 if z name is not equal to y name
    #                     add (z name, x name) to queue

    #     return true


def select_mrv(unassigned: list[Course], constraints: list[str]):
    x = []

    for course in unassigned:
        if x == [] or len(course.domain) < len(x[0].domain):
            x = [course]
        elif len(course.domain) == len(x[0].domain):
            x.append(course)

    return x[0]



    #     return the course in unassigned with the smallest domain


def _degree(course: Course, unassigned_names, constraints: list[str]):

    count = 0
    for x in constraints:
        left, right = x.split("!=")

        if course.name == left and right in unassigned_names:
            count += 1
        elif course.name == right and left in unassigned_names:
            count += 1
    return count    
    #     count <- 0

    #     for each constraint in constraints
    #         left, right <- split the constraint by "!="

    #         if course name is equal to left and right is in unassigned names
    #             increment count by 1

    #         else if course name is equal to right and left is in unassigned names
    #             increment count by 1

    #     return count
    raise Exception("Not implemented")


def select_degree(unassigned: list[Course], constraints: list[str]):
    unassigned_names = {course.name for course in unassigned}
    x = []
    for course in unassigned:
        degree = _degree(course, unassigned_names, constraints)
        if x == [] or degree > _degree(x[0], unassigned_names, constraints):
            x = [course]
        elif degree == _degree(x[0], unassigned_names, constraints):
            x.append(course)

    return x[0]

    #     unassigned names <- set of names of unassigned courses

    #     for each course compute degree as the number of constraints
    #         involving that course where the other variable is also unassigned

    #     return the course with the highest degree

def select_mrv_degree(unassigned: list[Course], constraints: list[str]):
    min_size = select_mrv(unassigned, constraints)
    candidates = [course for course in unassigned if len(course.domain) == len(min_size.domain)]
    if len(candidates) == 1:
        return candidates[0]
    unassigned_names = {course.name for course in unassigned}
    x = []
    for course in candidates:
        degree = _degree(course, unassigned_names, constraints)
        if x == [] or degree > _degree(x[0], unassigned_names, constraints):
            x = [course]
        elif degree == _degree(x[0], unassigned_names, constraints):
            x.append(course)
    return x[0] 




    #     min size <- smallest domain size among unassigned courses
    #     candidates <- all unassigned courses whose domain size equals min size

    #     if there is only one candidate
    #         return that candidate

    #     unassigned names <- set of names of unassigned courses

    #     for each candidate compute degree as the number of constraints
    #         involving that candidate where the other variable is also unassigned

    #     return the candidate with the highest degree


def _select_first(unassigned: list[Course], constraints: list[str]):
    return unassigned[0]
    #     return the first course in unassigned
    raise Exception("Not implemented")


def backtracking_with_inference(
    unassigned: list[Course],
    assigned: list[Course],
    constraints: list[str],
    select=_select_first,
):
    if not unassigned:
        return True 
    course = select(unassigned, constraints)
    remaining = [c for c in unassigned if c != course]
    for day in course.domain:
        course.assign(day)

        if not is_consistent(course, assigned, constraints):
            course.remove_assignment()
            continue

        assigned.append(course)

        saved_domains = {c.name: c.domain[:] for c in remaining + assigned}
        course.domain = [day]

        if ac3(remaining + assigned, constraints):
            if backtracking_with_inference(remaining, assigned, constraints, select):
                return True

        for c in remaining + assigned:
            c.domain = saved_domains[c.name]

        assigned.pop()
        course.remove_assignment()
    return False    
    #     if unassigned is empty
    #         return true

    #     course <- select var(unassigned, constraints)
    #     remaining <- all courses in unassigned except course

    #     for each day in a copy of course domain
    #         assign that day to the course

    #         if the assignment is not consistent
    #             remove the assignment from the course
    #             continue with the next day

    #         add course to assigned
    #         all courses <- assigned combined with remaining
    #         saved domains <- save a copy of the domain of every course in all courses
    #         set course domain to contain only that day
    #         inference ok <- ac3(all courses, constraints)

    #         if inference ok
    #             if backtracking with inference(remaining, assigned, constraints, select var)
    #                 return true

    #         restore the domain of every course from saved domains
    #         remove course from assigned
    #         remove the assignment from the course
    #     return false
