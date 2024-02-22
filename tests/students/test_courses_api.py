import pytest
import random
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


# проверка получения первого курса (retrieve-логика)
@pytest.mark.django_db
def test_get_course(client, courses_factory):
    course = courses_factory(_quantity=1)
    course_id = course[0].id
    response = client.get(f'/api/v1/courses/{course_id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course[0].name


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_list_courses(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_get_courses_filtered_id(client, courses_factory):
    courses = courses_factory(_quantity=10)
    random_number = random.randint(0, 9)
    course_random = courses[random_number]
    course_id = course_random.id
    response = client.get('/api/v1/courses/', {'id': course_id})
    assert response.status_code == 200
    data = response.json()[0]
    assert data['id'] == course_id


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_get_courses_filtered_name(client, courses_factory):
    courses = courses_factory(_quantity=10)
    random_number = random.randint(0, 9)
    course_random = courses[random_number]
    course_name = course_random.name
    response = client.get('/api/v1/courses/', {'name': course_name})
    assert response.status_code == 200
    data = response.json()[0]
    assert data['name'] == course_name


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'test course'})
    assert response.status_code == 201
    assert Course.objects.count() == count+1


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, courses_factory):
    course = courses_factory(_quantity=1)
    course_id = course[0].id
    new_name_course = 'new name'
    response = client.patch(f'/api/v1/courses/{course_id}/', data={'name': new_name_course})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == new_name_course


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    course = courses_factory(_quantity=1)
    course_id = course[0].id
    count = Course.objects.count()
    response = client.delete(f'/api/v1/courses/{course_id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count-1
