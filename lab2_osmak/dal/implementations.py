from sqlalchemy.orm import Session
from typing import List, Optional
import csv
from .interfaces import IUserRepository, ITesterRepository, ITestPlanRepository, ITestCaseRepository, ITestStepRepository, ITestResultRepository, IDataImporter
from .models import User, Tester, TestPlan, TestCase, TestStep, TestResult, TestStatus
from datetime import datetime

class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, user: User) -> None:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()

class TesterRepository(ITesterRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_tester(self, tester: Tester) -> None:
        self.db.add(tester)
        self.db.commit()
        self.db.refresh(tester)

    def get_tester_by_id(self, tester_id: int) -> Optional[Tester]:
        return self.db.query(Tester).filter(Tester.id == tester_id).first()

    def get_all_testers(self) -> List[Tester]:
        return self.db.query(Tester).all()

class TestPlanRepository(ITestPlanRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_test_plan(self, test_plan: TestPlan) -> None:
        self.db.add(test_plan)
        self.db.commit()
        self.db.refresh(test_plan)

    def get_test_plan_by_id(self, test_plan_id: int) -> Optional[TestPlan]:
        return self.db.query(TestPlan).filter(TestPlan.id == test_plan_id).first()

    def get_all_test_plans(self) -> List[TestPlan]:
        return self.db.query(TestPlan).all()

class TestCaseRepository(ITestCaseRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_test_case(self, test_case: TestCase) -> None:
        self.db.add(test_case)
        self.db.commit()
        self.db.refresh(test_case)

    def get_test_case_by_id(self, test_case_id: int) -> Optional[TestCase]:
        return self.db.query(TestCase).filter(TestCase.id == test_case_id).first()

    def get_all_test_cases(self) -> List[TestCase]:
        return self.db.query(TestCase).all()

class TestStepRepository(ITestStepRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_test_step(self, test_step: TestStep) -> None:
        self.db.add(test_step)
        self.db.commit()
        self.db.refresh(test_step)

    def get_test_step_by_id(self, test_step_id: int) -> Optional[TestStep]:
        return self.db.query(TestStep).filter(TestStep.id == test_step_id).first()

    def get_all_test_steps(self) -> List[TestStep]:
        return self.db.query(TestStep).all()

class TestResultRepository(ITestResultRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_test_result(self, test_result: TestResult) -> None:
        self.db.add(test_result)
        self.db.commit()
        self.db.refresh(test_result)

    def get_test_result_by_id(self, test_result_id: int) -> Optional[TestResult]:
        return self.db.query(TestResult).filter(TestResult.id == test_result_id).first()

    def get_all_test_results(self) -> List[TestResult]:
        return self.db.query(TestResult).all()

class DataImporter(IDataImporter):
    def __init__(self, db: Session, user_repo: IUserRepository, tester_repo: ITesterRepository, test_plan_repo: ITestPlanRepository, test_case_repo: ITestCaseRepository, test_step_repo: ITestStepRepository, test_result_repo: ITestResultRepository):
        self.db = db
        self.user_repo = user_repo
        self.tester_repo = tester_repo
        self.test_plan_repo = test_plan_repo
        self.test_case_repo = test_case_repo
        self.test_step_repo = test_step_repo
        self.test_result_repo = test_result_repo

    def import_from_csv(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entity_type = row.get('type')
                if entity_type == 'user':
                    user = User(name=row['name'], email=row['email'])
                    self.user_repo.add_user(user)
                elif entity_type == 'tester':
                    tester = Tester(user_id=int(row['user_id']), experience_years=int(row.get('experience_years', 0)))
                    self.tester_repo.add_tester(tester)
                elif entity_type == 'test_plan':
                    test_plan = TestPlan(name=row['name'], description=row.get('description'), created_at=datetime.fromisoformat(row.get('created_at')))
                    self.test_plan_repo.add_test_plan(test_plan)
                elif entity_type == 'test_case':
                    test_case = TestCase(test_plan_id=int(row['test_plan_id']), name=row['name'], description=row.get('description'))
                    self.test_case_repo.add_test_case(test_case)
                elif entity_type == 'test_step':
                    test_step = TestStep(test_case_id=int(row['test_case_id']), step_number=int(row['step_number']), description=row['description'], expected_result=row.get('expected_result'))
                    self.test_step_repo.add_test_step(test_step)
                elif entity_type == 'test_result':
                    test_result = TestResult(test_case_id=int(row['test_case_id']), tester_id=int(row['tester_id']), status=TestStatus(row['status']), executed_at=datetime.fromisoformat(row.get('executed_at')), notes=row.get('notes'))
                    self.test_result_repo.add_test_result(test_result)