# School REST API

This Django REST Framework app manages schools, classrooms, teachers, and students.

## Files and responsibilities

- `apis/models.py` defines the database tables and their relationships.
- `apis/migrations/` contains the database changes generated from the models.
- `apis/serializers.py` validates request data and shapes JSON responses.
- `apis/filters.py` defines the supported query-string filters using `django-filter`.
- `apis/views/v1/` contains the CRUD endpoints; each resource has its own viewset.
- `apis/urls.py` registers viewsets with the router under `/api/v1/`.
- `apis/tests.py` tests the endpoints, filters, and related response data.
- `exam_app/settings.py` enables Django REST Framework and `django-filter`.

## Data relationships

- A school has many classrooms.
- A classroom belongs to one school and has many students.
- Teachers and classrooms have a many-to-many relationship, with each teacher's
  classrooms restricted to one school.
- A student belongs to one classroom.

Classroom `grade` and `section` are positive numbers. Gender values are `male`,
`female`, or `other`.

### Deletion behavior

The deletion behavior is defined by `on_delete=models.CASCADE` on the classroom's
school relationship and the student's classroom relationship:

- Deleting a school also deletes its classrooms and the students in those
  classrooms.
- Teacher records are not deleted when a school is deleted. Their links to
  classrooms that were deleted are removed.

This is the behavior implemented in the models; it is an implementation choice
because the exam requirements do not specify what should happen to related
records on deletion.

## Run locally

From this directory:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Run the API tests with:

```powershell
python manage.py test apis
```

The endpoints are available at `/api/v1/schools/`, `/api/v1/classrooms/`,
`/api/v1/teachers/`, and `/api/v1/students/`. They support the usual `GET`,
`POST`, `PUT`, `PATCH`, and `DELETE` operations provided by Django REST Framework.

## Filters

- `GET /api/v1/schools/?name=central`
- `GET /api/v1/classrooms/?school=1`
- `GET /api/v1/teachers/?school=1&classroom=2&firstname=som&lastname=lee&gender=female`
- `GET /api/v1/students/?school=1&classroom=2&firstname=som&lastname=lee&gender=female`

Name filters are case-insensitive partial matches. School and classroom filters
use database IDs.

To assign teachers to classrooms, send classroom IDs in the teacher's
`classrooms` list. To assign a student, send one classroom ID in `classroom`.
