from flask import Flask, jsonify, request
from dal.database import SessionLocal
from dal.models import User, Tester, TestPlan, TestCase, TestStep, TestResult
from bll.implementations import UserService, TesterService, TestPlanService, TestCaseService, TestStepService, TestResultService

app = Flask(__name__)

# Initialize database session
def get_db():
    return SessionLocal()

# ============ USER ENDPOINTS ============

@app.route('/api/users', methods=['GET'])
def get_users():
    db = get_db()
    users = db.query(User).all()
    db.close()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user:
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
    return jsonify({'error': 'User not found'}), 404

# ============ TESTER ENDPOINTS ============

@app.route('/api/testers', methods=['GET'])
def get_testers():
    db = get_db()
    testers = db.query(Tester).all()
    db.close()
    return jsonify([{'id': t.id, 'user_id': t.user_id, 'experience_years': t.experience_years} for t in testers])

@app.route('/api/testers/<int:tester_id>', methods=['GET'])
def get_tester(tester_id):
    db = get_db()
    tester = db.query(Tester).filter(Tester.id == tester_id).first()
    db.close()
    if tester:
        return jsonify({'id': tester.id, 'user_id': tester.user_id, 'experience_years': tester.experience_years})
    return jsonify({'error': 'Tester not found'}), 404

# ============ TEST PLAN ENDPOINTS ============

@app.route('/api/test-plans', methods=['GET'])
def get_test_plans():
    db = get_db()
    plans = db.query(TestPlan).all()
    db.close()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description, 'created_at': str(p.created_at)} for p in plans])

@app.route('/api/test-plans/<int:plan_id>', methods=['GET'])
def get_test_plan(plan_id):
    db = get_db()
    plan = db.query(TestPlan).filter(TestPlan.id == plan_id).first()
    db.close()
    if plan:
        return jsonify({'id': plan.id, 'name': plan.name, 'description': plan.description, 'created_at': str(plan.created_at)})
    return jsonify({'error': 'Test plan not found'}), 404

# ============ TEST CASE ENDPOINTS ============

@app.route('/api/test-cases', methods=['GET'])
def get_test_cases():
    db = get_db()
    cases = db.query(TestCase).all()
    db.close()
    return jsonify([{'id': c.id, 'test_plan_id': c.test_plan_id, 'name': c.name, 'description': c.description} for c in cases])

@app.route('/api/test-cases/<int:case_id>', methods=['GET'])
def get_test_case(case_id):
    db = get_db()
    case = db.query(TestCase).filter(TestCase.id == case_id).first()
    db.close()
    if case:
        return jsonify({'id': case.id, 'test_plan_id': case.test_plan_id, 'name': case.name, 'description': case.description})
    return jsonify({'error': 'Test case not found'}), 404

# ============ TEST STEP ENDPOINTS ============

@app.route('/api/test-steps', methods=['GET'])
def get_test_steps():
    db = get_db()
    steps = db.query(TestStep).all()
    db.close()
    return jsonify([{'id': s.id, 'test_case_id': s.test_case_id, 'step_number': s.step_number, 
                     'description': s.description, 'expected_result': s.expected_result} for s in steps])

@app.route('/api/test-steps/<int:step_id>', methods=['GET'])
def get_test_step(step_id):
    db = get_db()
    step = db.query(TestStep).filter(TestStep.id == step_id).first()
    db.close()
    if step:
        return jsonify({'id': step.id, 'test_case_id': step.test_case_id, 'step_number': step.step_number,
                       'description': step.description, 'expected_result': step.expected_result})
    return jsonify({'error': 'Test step not found'}), 404

# ============ TEST RESULT ENDPOINTS ============

@app.route('/api/test-results', methods=['GET'])
def get_test_results():
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
    db = get_db()
    results = db.query(TestResult).limit(limit).offset(offset).all()
    db.close()
    return jsonify([{'id': r.id, 'test_case_id': r.test_case_id, 'tester_id': r.tester_id, 
                     'status': str(r.status), 'executed_at': str(r.executed_at), 'notes': r.notes} for r in results])

@app.route('/api/test-results/<int:result_id>', methods=['GET'])
def get_test_result(result_id):
    db = get_db()
    result = db.query(TestResult).filter(TestResult.id == result_id).first()
    db.close()
    if result:
        return jsonify({'id': result.id, 'test_case_id': result.test_case_id, 'tester_id': result.tester_id,
                       'status': str(result.status), 'executed_at': str(result.executed_at), 'notes': result.notes})
    return jsonify({'error': 'Test result not found'}), 404

# ============ STATISTICS ENDPOINTS ============

@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = get_db()
    users_count = db.query(User).count()
    testers_count = db.query(Tester).count()
    plans_count = db.query(TestPlan).count()
    cases_count = db.query(TestCase).count()
    steps_count = db.query(TestStep).count()
    results_count = db.query(TestResult).count()
    
    results_by_status = {}
    for result in db.query(TestResult.status).distinct():
        count = db.query(TestResult).filter(TestResult.status == result[0]).count()
        results_by_status[str(result[0])] = count
    
    db.close()
    
    return jsonify({
        'users_count': users_count,
        'testers_count': testers_count,
        'test_plans_count': plans_count,
        'test_cases_count': cases_count,
        'test_steps_count': steps_count,
        'test_results_count': results_count,
        'test_results_by_status': results_by_status
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Lab 2 OSMAK API is running'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
