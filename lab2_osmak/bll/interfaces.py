from abc import ABC, abstractmethod
from typing import List
from dal.models import User, Tester, TestPlan, TestCase, TestStep, TestResult
from presentation.interfaces import IOutputStrategy

class IUserService(ABC):
    @abstractmethod
    def import_users_from_csv(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

class ITesterService(ABC):
    @abstractmethod
    def import_testers_from_csv(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_all_testers(self) -> List[Tester]:
        pass

class ITestPlanService(ABC):
    @abstractmethod
    def import_test_plans_from_csv(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_all_test_plans(self) -> List[TestPlan]:
        pass

class ITestCaseService(ABC):
    @abstractmethod
    def import_test_cases_from_csv(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_all_test_cases(self) -> List[TestCase]:
        pass

class ITestStepService(ABC):
    @abstractmethod
    def import_test_steps_from_csv(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_all_test_steps(self) -> List[TestStep]:
        pass

class ITestResultService(ABC):
    @abstractmethod
    def import_test_results_from_csv(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_all_test_results(self) -> List[TestResult]:
        pass

class IDataImportService(ABC):
    @abstractmethod
    def import_all_data_from_csv(self, file_path: str, output_strategy: IOutputStrategy) -> None:
        pass