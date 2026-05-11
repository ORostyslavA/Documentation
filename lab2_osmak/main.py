import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from dal.database import SessionLocal, create_tables
from dal.implementations import UserRepository, TesterRepository, TestPlanRepository, TestCaseRepository, TestStepRepository, TestResultRepository, DataImporter
from bll.implementations import DataImportService
import json
from presentation.implementations import ConsoleOutputStrategy, KafkaOutputStrategy

def main():
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Drop and create tables
    from dal.database import engine
    from dal.models import Base
    Base.metadata.drop_all(bind=engine)
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

    # Choose output strategy based on config
    if config['output_strategy'] == 'console':
        output_strategy = ConsoleOutputStrategy()
    elif config['output_strategy'] == 'kafka':
        kafka_config = config['kafka']
        output_strategy = KafkaOutputStrategy(kafka_config['bootstrap_servers'], kafka_config['topic'])
    else:
        raise ValueError("Invalid output_strategy in config")

    # Import data
    data_import_service.import_all_data_from_csv('data.csv', output_strategy)

    print("Data imported successfully")

if __name__ == "__main__":
    main()