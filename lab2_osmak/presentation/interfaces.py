from abc import ABC, abstractmethod
from typing import List
from dal.models import User, Tester, TestPlan, TestCase, TestStep, TestResult

class IUserController(ABC):
    @abstractmethod
    def get_users(self) -> List[User]:
        pass

class ITesterController(ABC):
    @abstractmethod
    def get_testers(self) -> List[Tester]:
        pass

class ITestPlanController(ABC):
    @abstractmethod
    def get_test_plans(self) -> List[TestPlan]:
        pass

class ITestCaseController(ABC):
    @abstractmethod
    def get_test_cases(self) -> List[TestCase]:
        pass

class ITestStepController(ABC):
    @abstractmethod
    def get_test_steps(self) -> List[TestStep]:
        pass

class ITestResultController(ABC):
    @abstractmethod
    def get_test_results(self) -> List[TestResult]:
        pass