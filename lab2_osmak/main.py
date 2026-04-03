import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from dal.database import SessionLocal, create_tables
from dal.implementations import UserRepository, TesterRepository, TestPlanRepository, TestCaseRepository, TestStepRepository, TestResultRepository, DataImporter
from bll.implementations import DataImportService

def main():
    # Create tables
    create_tables()

    # Dependency Injection
    db: Session = SessionLocal()
    user_repo = UserRepository(db)
    tester_repo = TesterRepository(db)
    test_plan_repo = TestPlanRepository(db)
    test_case_repo = TestCaseRepository(db)
    test_step_repo = TestStepRepository(db)
    test_result_repo = TestResultRepository(db)
    data_importer = DataImporter(db, user_repo, tester_repo, test_plan_repo, test_case_repo, test_step_repo, test_result_repo)
    data_import_service = DataImportService(data_importer)

    # Import data
    data_import_service.import_all_data_from_csv('data.csv')

    print("Data imported successfully")

if __name__ == "__main__":
    main()