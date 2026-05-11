from abc import ABC, abstractmethod
from typing import List, Optional
from .models import User, Tester, TestPlan, TestCase, TestStep, TestResult
from presentation.interfaces import IOutputStrategy

class IUserRepository(ABC):
    @abstractmethod
    def add_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

class ITesterRepository(ABC):
    @abstractmethod
    def add_tester(self, tester: Tester) -> None:
        pass

    @abstractmethod
    def get_tester_by_id(self, tester_id: int) -> Optional[Tester]:
        pass

    @abstractmethod
    def get_all_testers(self) -> List[Tester]:
        pass

class ITestPlanRepository(ABC):
    @abstractmethod
    def add_test_plan(self, test_plan: TestPlan) -> None:
        pass

    @abstractmethod
    def get_test_plan_by_id(self, test_plan_id: int) -> Optional[TestPlan]:
        pass

    @abstractmethod
    def get_all_test_plans(self) -> List[TestPlan]:
        pass

class ITestCaseRepository(ABC):
    @abstractmethod
    def add_test_case(self, test_case: TestCase) -> None:
        pass

    @abstractmethod
    def get_test_case_by_id(self, test_case_id: int) -> Optional[TestCase]:
        pass

    @abstractmethod
    def get_all_test_cases(self) -> List[TestCase]:
        pass

class ITestStepRepository(ABC):
    @abstractmethod
    def add_test_step(self, test_step: TestStep) -> None:
        pass

    @abstractmethod
    def get_test_step_by_id(self, test_step_id: int) -> Optional[TestStep]:
        pass

    @abstractmethod
    def get_all_test_steps(self) -> List[TestStep]:
        pass

class ITestResultRepository(ABC):
    @abstractmethod
    def add_test_result(self, test_result: TestResult) -> None:
        pass

    @abstractmethod
    def get_test_result_by_id(self, test_result_id: int) -> Optional[TestResult]:
        pass

    @abstractmethod
    def get_all_test_results(self) -> List[TestResult]:
        pass

class IDataImporter(ABC):
    @abstractmethod
    def import_from_csv(self, file_path: str, output_strategy: IOutputStrategy) -> None:
        pass