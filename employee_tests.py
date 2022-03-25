
import requests
from employees_app import BASE_URL, EMPLOYEES_ROUTE


def test_get_employees_response():
    # Prep
    url = BASE_URL + EMPLOYEES_ROUTE
    # Activate
    response = requests.get(url)
    # Test
    assert response.status_code == 200