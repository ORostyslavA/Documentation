from typing import List
import csv
from .interfaces import IUserService, ITesterService, ITestPlanService, ITestCaseService, ITestStepService, ITestResultService, IDataImportService
from dal.interfaces import IUserRepository, ITesterRepository, ITestPlanRepository, ITestCaseRepository, ITestStepRepository, ITestResultRepository, IDataImporter
from dal.models import User, Tester, TestPlan, TestCase, TestStep, TestResult, TestStatus
from datetime import datetime

class UserService(IUserService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def import_users_from_csv(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('type') == 'user':
                    user = User(name=row['name'], email=row['email'])
                    self.user_repo.add_user(user)

    def get_all_users(self) -> List[User]:
        return self.user_repo.get_all_users()

class TesterService(ITesterService):
    def __init__(self, tester_repo: ITesterRepository):
        self.tester_repo = tester_repo

    def import_testers_from_csv(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('type') == 'tester':
                    tester = Tester(user_id=int(row['user_id']), experience_years=int(row.get('experience_years', 0)))
                    self.tester_repo.add_tester(tester)

    def get_all_testers(self) -> List[Tester]:
        return self.tester_repo.get_all_testers()

class TestPlanService(ITestPlanService):
    def __init__(self, test_plan_repo: ITestPlanRepository):
        self.test_plan_repo = test_plan_repo

    def import_test_plans_from_csv(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('type') == 'test_plan':
                    test_plan = TestPlan(name=row['name'], description=row.get('description'), created_at=datetime.fromisoformat(row.get('created_at')))
                    self.test_plan_repo.add_test_plan(test_plan)

    def get_all_test_plans(self) -> List[TestPlan]:
        return self.test_plan_repo.get_all_test_plans()

class TestCaseService(ITestCaseService):
    def __init__(self, test_case_repo: ITestCaseRepository):
        self.test_case_repo = test_case_repo

    def import_test_cases_from_csv(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('type') == 'test_case':
                    test_case = TestCase(test_plan_id=int(row['test_plan_id']), name=row['name'], description=row.get('description'))
                    self.test_case_repo.add_test_case(test_case)

    def get_all_test_cases(self) -> List[TestCase]:
        return self.test_case_repo.get_all_test_cases()

class TestStepService(ITestStepService):
    def __init__(self, test_step_repo: ITestStepRepository):
        self.test_step_repo = test_step_repo

    def import_test_steps_from_csv(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('type') == 'test_step':
                    test_step = TestStep(test_case_id=int(row['test_case_id']), step_number=int(row['step_number']), description=row['description'], expected_result=row.get('expected_result'))
                    self.test_step_repo.add_test_step(test_step)

    def get_all_test_steps(self) -> List[TestStep]:
        return self.test_step_repo.get_all_test_steps()

class TestResultService(ITestResultService):
    def __init__(self, test_result_repo: ITestResultRepository):
        self.test_result_repo = test_result_repo

    def import_test_results_from_csv(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('type') == 'test_result':
                    test_result = TestResult(test_case_id=int(row['test_case_id']), tester_id=int(row['tester_id']), status=TestStatus(row['status']), executed_at=datetime.fromisoformat(row.get('executed_at')), notes=row.get('notes'))
                    self.test_result_repo.add_test_result(test_result)

    def get_all_test_results(self) -> List[TestResult]:
        return self.test_result_repo.get_all_test_results()

class DataImportService(IDataImportService):
    def __init__(self, data_importer: IDataImporter):
        self.data_importer = data_importer

    def import_all_data_from_csv(self, file_path: str) -> None:
        self.data_importer.import_from_csv(file_path)