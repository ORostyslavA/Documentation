from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flasgger import Swagger
from functools import wraps
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from dal.database import SessionLocal
from dal.models import User, Tester, TestPlan, TestCase, TestStep, TestResult
from bll.implementations import UserService, TesterService, TestPlanService, TestCaseService, TestStepService, TestResultService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Lab 2 OSMAK API",
        "description": "Three-tier application API with JWT authentication",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    }
})

# Initialize database session
def get_db():
    return SessionLocal()

# Initialize services
def get_testcase_service():
    db = get_db()
    from dal.implementations import TestCaseRepository, TestPlanRepository
    testcase_repo = TestCaseRepository(db)
    testplan_repo = TestPlanRepository(db)
    return TestCaseService(testcase_repo), TestPlanService(testplan_repo), db

def get_tester_service():
    db = get_db()
    from dal.implementations import TesterRepository
    tester_repo = TesterRepository(db)
    return TesterService(tester_repo), db

def get_testplan_service():
    db = get_db()
    from dal.implementations import TestPlanRepository
    testplan_repo = TestPlanRepository(db)
    return TestPlanService(testplan_repo), db

# ============ JWT TOKEN GENERATION ============

def generate_token(username: str, expires_in: int = 3600) -> str:
    """Generate JWT token"""
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# ============ DECORATOR FOR PROTECTED ROUTES ============

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid Authorization header format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        
        payload = verify_token(token)
        if payload is None:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return f(payload, *args, **kwargs)
    return decorated

# Initialize database session
def get_db():
    return SessionLocal()

# ============ USER ENDPOINTS ============

@app.route('/api/users', methods=['GET'])
@token_required
def get_users(payload):
    """
    Get all users (requires JWT token)
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of all users
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              name:
                type: string
              email:
                type: string
      401:
        description: Unauthorized - missing or invalid token
    """
    db = get_db()
    users = db.query(User).all()
    db.close()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(payload, user_id):
    """
    Get user by ID (requires JWT token)
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: User found
        schema:
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
      401:
        description: Unauthorized
      404:
        description: User not found
    """
    db = get_db()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user:
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
    return jsonify({'error': 'User not found'}), 404

# ============ TESTER ENDPOINTS ============

@app.route('/api/testers', methods=['GET'])
@token_required
def get_testers(payload):
    """
    Get all testers (requires JWT token)
    ---
    tags:
      - Testers
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of all testers
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              user_id:
                type: integer
              experience_years:
                type: integer
      401:
        description: Unauthorized
    """
    db = get_db()
    testers = db.query(Tester).all()
    db.close()
    return jsonify([{'id': t.id, 'user_id': t.user_id, 'experience_years': t.experience_years} for t in testers])

@app.route('/api/testers/<int:tester_id>', methods=['GET'])
@token_required
def get_tester(payload, tester_id):
    """
    Get tester by ID (requires JWT token)
    ---
    tags:
      - Testers
    security:
      - BearerAuth: []
    parameters:
      - name: tester_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tester found
        schema:
          properties:
            id:
              type: integer
            user_id:
              type: integer
            experience_years:
              type: integer
      401:
        description: Unauthorized
      404:
        description: Tester not found
    """
    db = get_db()
    tester = db.query(Tester).filter(Tester.id == tester_id).first()
    db.close()
    if tester:
        return jsonify({'id': tester.id, 'user_id': tester.user_id, 'experience_years': tester.experience_years})
    return jsonify({'error': 'Tester not found'}), 404

# ============ TEST PLAN ENDPOINTS ============

@app.route('/api/test-plans', methods=['GET'])
@token_required
def get_test_plans(payload):
    """
    Get all test plans (requires JWT token)
    ---
    tags:
      - Test Plans
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of all test plans
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              name:
                type: string
              description:
                type: string
              created_at:
                type: string
      401:
        description: Unauthorized
    """
    db = get_db()
    plans = db.query(TestPlan).all()
    db.close()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description, 'created_at': str(p.created_at)} for p in plans])

@app.route('/api/test-plans/<int:plan_id>', methods=['GET'])
@token_required
def get_test_plan(payload, plan_id):
    """
    Get test plan by ID (requires JWT token)
    ---
    tags:
      - Test Plans
    security:
      - BearerAuth: []
    parameters:
      - name: plan_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Test plan found
      401:
        description: Unauthorized
      404:
        description: Test plan not found
    """
    db = get_db()
    plan = db.query(TestPlan).filter(TestPlan.id == plan_id).first()
    db.close()
    if plan:
        return jsonify({'id': plan.id, 'name': plan.name, 'description': plan.description, 'created_at': str(plan.created_at)})
    return jsonify({'error': 'Test plan not found'}), 404

# ============ TEST CASE ENDPOINTS ============

@app.route('/api/test-cases', methods=['GET'])
@token_required
def get_test_cases(payload):
    """
    Get all test cases (requires JWT token)
    ---
    tags:
      - Test Cases
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of all test cases
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              test_plan_id:
                type: integer
              name:
                type: string
              description:
                type: string
      401:
        description: Unauthorized
    """
    db = get_db()
    cases = db.query(TestCase).all()
    db.close()
    return jsonify([{'id': c.id, 'test_plan_id': c.test_plan_id, 'name': c.name, 'description': c.description} for c in cases])

@app.route('/api/test-cases/<int:case_id>', methods=['GET'])
@token_required
def get_test_case(payload, case_id):
    """
    Get test case by ID (requires JWT token)
    ---
    tags:
      - Test Cases
    security:
      - BearerAuth: []
    parameters:
      - name: case_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Test case found
      401:
        description: Unauthorized
      404:
        description: Test case not found
    """
    db = get_db()
    case = db.query(TestCase).filter(TestCase.id == case_id).first()
    db.close()
    if case:
        return jsonify({'id': case.id, 'test_plan_id': case.test_plan_id, 'name': case.name, 'description': case.description})
    return jsonify({'error': 'Test case not found'}), 404

# ============ TEST STEP ENDPOINTS ============

@app.route('/api/test-steps', methods=['GET'])
@token_required
def get_test_steps(payload):
    """
    Get all test steps (requires JWT token)
    ---
    tags:
      - Test Steps
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of all test steps
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              test_case_id:
                type: integer
              step_number:
                type: integer
              description:
                type: string
              expected_result:
                type: string
      401:
        description: Unauthorized
    """
    db = get_db()
    steps = db.query(TestStep).all()
    db.close()
    return jsonify([{'id': s.id, 'test_case_id': s.test_case_id, 'step_number': s.step_number, 
                     'description': s.description, 'expected_result': s.expected_result} for s in steps])

@app.route('/api/test-steps/<int:step_id>', methods=['GET'])
@token_required
def get_test_step(payload, step_id):
    """
    Get test step by ID (requires JWT token)
    ---
    tags:
      - Test Steps
    security:
      - BearerAuth: []
    parameters:
      - name: step_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Test step found
      401:
        description: Unauthorized
      404:
        description: Test step not found
    """
    db = get_db()
    step = db.query(TestStep).filter(TestStep.id == step_id).first()
    db.close()
    if step:
        return jsonify({'id': step.id, 'test_case_id': step.test_case_id, 'step_number': step.step_number,
                       'description': step.description, 'expected_result': step.expected_result})
    return jsonify({'error': 'Test step not found'}), 404

# ============ TEST RESULT ENDPOINTS ============

@app.route('/api/test-results', methods=['GET'])
@token_required
def get_test_results(payload):
    """
    Get all test results (requires JWT token)
    ---
    tags:
      - Test Results
    security:
      - BearerAuth: []
    parameters:
      - name: limit
        in: query
        type: integer
        default: 20
        description: Number of results
      - name: offset
        in: query
        type: integer
        default: 0
        description: Offset
    responses:
      200:
        description: List of test results
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              test_case_id:
                type: integer
              tester_id:
                type: integer
              status:
                type: string
              executed_at:
                type: string
              notes:
                type: string
      401:
        description: Unauthorized
    """
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
    db = get_db()
    results = db.query(TestResult).limit(limit).offset(offset).all()
    db.close()
    return jsonify([{'id': r.id, 'test_case_id': r.test_case_id, 'tester_id': r.tester_id, 
                     'status': str(r.status), 'executed_at': str(r.executed_at), 'notes': r.notes} for r in results])

@app.route('/api/test-results/<int:result_id>', methods=['GET'])
@token_required
def get_test_result(payload, result_id):
    """
    Get test result by ID (requires JWT token)
    ---
    tags:
      - Test Results
    security:
      - BearerAuth: []
    parameters:
      - name: result_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Test result found
      401:
        description: Unauthorized
      404:
        description: Test result not found
    """
    db = get_db()
    result = db.query(TestResult).filter(TestResult.id == result_id).first()
    db.close()
    if result:
        return jsonify({'id': result.id, 'test_case_id': result.test_case_id, 'tester_id': result.tester_id,
                       'status': str(result.status), 'executed_at': str(result.executed_at), 'notes': result.notes})
    return jsonify({'error': 'Test result not found'}), 404

# ============ STATISTICS ENDPOINTS ============

@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats(payload):
    """
    Get statistics about the database (requires JWT token)
    ---
    tags:
      - Statistics
    security:
      - BearerAuth: []
    responses:
      200:
        description: Database statistics
        schema:
          properties:
            users_count:
              type: integer
            testers_count:
              type: integer
            test_plans_count:
              type: integer
            test_cases_count:
              type: integer
            test_steps_count:
              type: integer
            test_results_count:
              type: integer
            test_results_by_status:
              type: object
      401:
        description: Unauthorized
    """
    db = get_db()
    users_count = db.query(User).count()
    testers_count = db.query(Tester).count()
    plans_count = db.query(TestPlan).count()
    cases_count = db.query(TestCase).count()
    steps_count = db.query(TestStep).count()
    results_count = db.query(TestResult).count()
    
    # Count by status
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
    """
    Health check
    ---
    tags:
      - Health
    responses:
      200:
        description: API is healthy
    """
    return jsonify({'status': 'healthy', 'message': 'Lab 2 OSMAK API is running'})

# ============ AUTHENTICATION ENDPOINT ============

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Get JWT token (for testing use any username/password)
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            username:
              type: string
              example: testuser
            password:
              type: string
              example: password123
    responses:
      200:
        description: Token generated successfully
        schema:
          properties:
            token:
              type: string
            expires_in:
              type: integer
      400:
        description: Missing username or password
    """
    data = request.get_json()
    
    if not data or not data.get('username'):
        return jsonify({'error': 'Username is required'}), 400
    
    username = data.get('username')
    token = generate_token(username)
    
    return jsonify({
        'token': token,
        'expires_in': 3600,
        'message': f'Token generated for user: {username}'
    }), 200

# ============ MVC ROUTES ============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testplans')
def testplans_list():
    db = get_db()
    testplans = db.query(TestPlan).options(joinedload(TestPlan.test_cases)).all()
    db.close()
    return render_template('testplan_list.html', testplans=testplans)

@app.route('/testers')
def testers_list():
    db = get_db()
    testers = db.query(Tester).options(joinedload(Tester.user), joinedload(Tester.test_results)).all()
    db.close()
    return render_template('tester_list.html', testers=testers)

@app.route('/testcases')
def testcases_list():
    db = get_db()
    testcases = db.query(TestCase).options(joinedload(TestCase.test_plan), joinedload(TestCase.test_steps), joinedload(TestCase.test_results)).all()
    db.close()
    return render_template('testcase_list.html', testcases=testcases)

@app.route('/testcases/<int:testcase_id>')
def testcase_detail(testcase_id):
    db = get_db()
    testcase = db.query(TestCase).options(joinedload(TestCase.test_plan), joinedload(TestCase.test_steps), joinedload(TestCase.test_results).joinedload(TestResult.tester).joinedload(Tester.user)).filter(TestCase.id == testcase_id).first()
    db.close()
    if not testcase:
        return "Test case not found", 404
    return render_template('testcase_detail.html', testcase=testcase)

@app.route('/testcases/new', methods=['GET', 'POST'])
def testcase_create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        test_plan_id = request.form['test_plan_id']
        
        db = get_db()
        testcase = TestCase(name=name, description=description, test_plan_id=test_plan_id)
        db.add(testcase)
        db.commit()
        db.close()
        return redirect(url_for('testcases_list'))
    
    db = get_db()
    test_plans = db.query(TestPlan).all()
    db.close()
    return render_template('testcase_form.html', test_plans=test_plans)

@app.route('/testcases/<int:testcase_id>/edit', methods=['GET', 'POST'])
def testcase_edit(testcase_id):
    db = get_db()
    testcase = db.query(TestCase).filter(TestCase.id == testcase_id).first()
    if not testcase:
        db.close()
        return "Test case not found", 404
    
    if request.method == 'POST':
        testcase.name = request.form['name']
        testcase.description = request.form.get('description')
        testcase.test_plan_id = request.form['test_plan_id']
        db.commit()
        db.close()
        return redirect(url_for('testcase_detail', testcase_id=testcase_id))
    
    test_plans = db.query(TestPlan).all()
    db.close()
    return render_template('testcase_form.html', testcase=testcase, test_plans=test_plans)

@app.route('/testcases/<int:testcase_id>/delete', methods=['POST'])
def testcase_delete(testcase_id):
    db = get_db()
    testcase = db.query(TestCase).options(joinedload(TestCase.test_steps), joinedload(TestCase.test_results)).filter(TestCase.id == testcase_id).first()
    if testcase:
        db.delete(testcase)
        db.commit()
    db.close()
    return redirect(url_for('testcases_list'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
