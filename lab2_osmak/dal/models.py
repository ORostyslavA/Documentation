from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class TestStatus(enum.Enum):
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    NOT_RUN = "not_run"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    # Assuming Tester inherits or has relation
    tester = relationship("Tester", back_populates="user", uselist=False)

class Tester(Base):
    __tablename__ = 'testers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    experience_years = Column(Integer)
    user = relationship("User", back_populates="tester")
    test_results = relationship("TestResult", back_populates="tester")

class TestPlan(Base):
    __tablename__ = 'test_plans'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime)
    test_cases = relationship("TestCase", back_populates="test_plan")

class TestCase(Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True)
    test_plan_id = Column(Integer, ForeignKey('test_plans.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    test_plan = relationship("TestPlan", back_populates="test_cases")
    test_steps = relationship("TestStep", back_populates="test_case")
    test_results = relationship("TestResult", back_populates="test_case")

class TestStep(Base):
    __tablename__ = 'test_steps'
    id = Column(Integer, primary_key=True)
    test_case_id = Column(Integer, ForeignKey('test_cases.id'), nullable=False)
    step_number = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    expected_result = Column(String)
    test_case = relationship("TestCase", back_populates="test_steps")

class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True)
    test_case_id = Column(Integer, ForeignKey('test_cases.id'), nullable=False)
    tester_id = Column(Integer, ForeignKey('testers.id'), nullable=False)
    status = Column(SQLEnum(TestStatus), nullable=False)
    executed_at = Column(DateTime)
    notes = Column(String)
    test_case = relationship("TestCase", back_populates="test_results")
    tester = relationship("Tester", back_populates="test_results")