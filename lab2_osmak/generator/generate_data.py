import csv
from faker import Faker
from datetime import datetime

fake = Faker()

def generate_data(num_users=200, num_testers=100, num_test_plans=50, num_test_cases=200, num_test_steps=500, num_test_results=2000):
    data = []
    used_emails = set()

    # Generate users
    for i in range(1, num_users + 1):
        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)
        data.append({
            'type': 'user',
            'id': i,
            'name': fake.name(),
            'email': email
        })

    # Generate testers (subset of users)
    for i in range(1, num_testers + 1):
        data.append({
            'type': 'tester',
            'id': i,
            'user_id': i,  # Assuming first 100 users are testers
            'experience_years': fake.random_int(min=0, max=20)
        })

    # Generate test plans
    for i in range(1, num_test_plans + 1):
        data.append({
            'type': 'test_plan',
            'id': i,
            'name': fake.catch_phrase(),
            'description': fake.text(max_nb_chars=200),
            'created_at': fake.date_time_this_year().isoformat()
        })

    # Generate test cases
    for i in range(1, num_test_cases + 1):
        data.append({
            'type': 'test_case',
            'id': i,
            'test_plan_id': fake.random_int(min=1, max=num_test_plans),
            'name': fake.sentence(),
            'description': fake.text(max_nb_chars=100)
        })

    # Generate test steps
    for i in range(1, num_test_steps + 1):
        data.append({
            'type': 'test_step',
            'id': i,
            'test_case_id': fake.random_int(min=1, max=num_test_cases),
            'step_number': fake.random_int(min=1, max=10),
            'description': fake.sentence(),
            'expected_result': fake.sentence()
        })

    # Generate test results
    statuses = ['passed', 'failed', 'blocked', 'not_run']
    for i in range(1, num_test_results + 1):
        data.append({
            'type': 'test_result',
            'id': i,
            'test_case_id': fake.random_int(min=1, max=num_test_cases),
            'tester_id': fake.random_int(min=1, max=num_testers),
            'status': fake.random_element(statuses),
            'executed_at': fake.date_time_this_year().isoformat(),
            'notes': fake.text(max_nb_chars=100) if fake.boolean() else ''
        })

    return data

if __name__ == "__main__":
    data = generate_data()
    with open('data.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['type', 'id', 'name', 'email', 'user_id', 'experience_years', 'description', 'created_at', 'test_plan_id', 'test_case_id', 'step_number', 'expected_result', 'tester_id', 'status', 'executed_at', 'notes']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print("Data generated and saved to data.csv")