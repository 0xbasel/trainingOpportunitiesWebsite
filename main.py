from flask import Flask, request, redirect, render_template, url_for


class Student:
    def __init__(self, username: str, password: str, name: str, gpa: float, major: str, location_preference: str):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__gpa = gpa
        self.__major = major
        self.__location_preference = location_preference

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def name(self):
        return self.__name

    @property
    def gpa(self):
        return self.__gpa

    @property
    def major(self):
        return self.__major

    @property
    def location_preference(self):
        return self.__location_preference


class Company:
    def __init__(self, username: str, password: str, name: str, major: str):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__major = major

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def name(self):
        return self.__name

    @property
    def major(self):
        return self.__major


class Post:
    def __init__(self, minimum_gpa: float, location: str, description: str, apply_link: str):
        self.__minimum_gpa = minimum_gpa
        self.__location = location
        self.__description = description
        self.__apply_link = apply_link

    @property
    def minimum_gpa(self):
        return self.__minimum_gpa

    @property
    def location(self):
        return self.__location

    @property
    def description(self):
        return self.__description

    @property
    def apply_link(self):
        return self.__apply_link


class System:
    def __init__(self):
        self.__posts = []
        self.__students = []
        self.__companies = []

    @property
    def posts(self):
        return self.__posts

    @property
    def students(self):
        return self.__students

    @property
    def companies(self):
        return self.__companies

    def add_post(self, post: Post):
        self.__posts.append(post)

    def add_student(self, student: Student):
        self.__students.append(student)

    def add_company(self, company: Company):
        self.__companies.append(company)

    def is_username_taken(self, username):
        for student in self.__students:
            if student.username == username:
                return True
        for company in self.__companies:
            if company.username == username:
                return True
        return False

    def authenticate_student(self, username, password):
        for student in self.__students:
            if student.username == username and student.password == password:
                return True
        return False

    def authenticate_company(self, username, password):
        for company in self.__companies:
            if company.username == username and company.password == password:
                return True
        return False


app = Flask(__name__)
system = System()

# Mock posts for demonstration purposes
post1 = Post(minimum_gpa=4.5, location="Medina", description="Software Engineer Internship",
             apply_link="https://example.com")
post2 = Post(minimum_gpa=4.0, location="Riyadh", description="Data Analyst Internship",
             apply_link="https://example.com")
system.add_post(post1)
system.add_post(post2)


@app.get('/')
def index():
    return render_template('index.html', posts=system.posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        name = request.form['name']
        major = request.form['major']

        if system.is_username_taken(username):
            return render_template('register.html', is_username_taken=system.is_username_taken(username))

        if user_type == 'student':
            gpa = float(request.form['gpa'])
            location_preference = request.form['location_preference']
            system.add_student(Student(username, password, name, gpa, major, location_preference))
        else:
            system.add_company(Company(username, password, name, major))

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        if user_type == 'student' and system.authenticate_student(username, password):
            return redirect(url_for('student_dashboard', username=username))
        elif user_type == 'company' and system.authenticate_company(username, password):
            return redirect(url_for('company_dashboard', username=username))
        else:
            return render_template('login.html', authenticate='failed')

    return render_template('login.html')


@app.get('/student_dashboard/<username>')
def student_dashboard(username: str):
    student = None
    for s in system.students:
        if s.username == username:
            student = s
            break

    filtered_posts = [post for post in system.posts if student.location_preference.lower() == post.location.lower() and student.gpa >= post.minimum_gpa]
    return render_template('student_dashboard.html', student=student, posts=filtered_posts)


@app.get('/company_dashboard/<username>')
def company_dashboard(username: str):
    company = None
    for c in system.companies:
        if c.username == username:
            company = c
            break

    return render_template('company_dashboard.html', company=company)


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        minimum_gpa = float(request.form['minimum_gpa'])
        location = request.form['location']
        description = request.form['description']
        apply_link = request.form['apply_link']
        system.add_post(Post(minimum_gpa=minimum_gpa, location=location, description=description, apply_link=apply_link))

        return redirect(url_for('index'))

    return render_template('create_post.html')


if __name__ == "__main__":
    app.run(debug=True)
