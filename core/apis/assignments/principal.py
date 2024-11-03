from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema
from ..teachers.schema import TeacherSchema

principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    teachers = Teacher.get_all_teachers()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)



@principal_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    assignments = Assignment.get_all_submitted_and_graded()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    grade_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.re_grade(_id=grade_payload.id, grade=grade_payload.grade, auth_principal=p)
    db.session.commit()
    assignment_dump = AssignmentSchema().dump(assignment)

    return APIResponse.respond(data=assignment_dump)

