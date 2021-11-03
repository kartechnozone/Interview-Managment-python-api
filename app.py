from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:pass@localHost:5432/Dummy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    Description = db.Column(db.String(2000))
    candidate = db.relationship(
        'Candidate', backref='project', lazy=True)
    projectstream = db.relationship(
        'ProjectStream', backref='project', lazy=True)

    def __init__(self, name, Description):
        self.name = name
        self.Description = Description


class Stream(db.Model):
    __tablename__ = 'stream'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(2000))
    candidate = db.relationship('Candidate', backref='candidate', lazy=True)
    panelmember = db.relationship(
        'PanelMember', backref='panelmember', lazy=True)
    projectstream = db.relationship(
        'ProjectStream', backref='projectstream', lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description
        # self.candidate = candidate
        # self.panelmember = panelmember
        # self.projectstream = projectstream


class PanelMember(db.Model):
    __tablename__ = 'panelmember'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    panelpool = db.relationship('PanelPool', backref='panelpool', lazy=True)
    round_status = db.relationship(
        'RoundStatus', backref='roundstatus', lazy=True)
    stream_id = db.Column(db.Integer, db.ForeignKey(
        'stream.id'))

    def __init__(self, name, email, stream_id, panelpool, round_status):
        self.name = name
        self.email = email
        self.stream_id = stream_id
        self.panelpool = panelpool
        self.round_status = round_status


class Candidate(db.Model):
    __tablename__ = 'candidate'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    mobile = db.Column(db.Integer)
    entry_type = db.Column(db.String(50))
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id'))
    stream_id = db.Column(db.Integer, db.ForeignKey(
        'stream.id'))

    def __init__(self, name, email, mobile, project_id, stream_id, entry_type):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.project_id = project_id
        self.stream_id = stream_id
        self.entry_type = entry_type


class PanelPool(db.Model):
    __tablename__ = 'panelpool'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    panelmember_id = db.Column(db.Integer, db.ForeignKey(
        'panelmember.id'))
    stream_id = db.Column(db.Integer, db.ForeignKey(
        'stream.id'))

    def __init__(self, name, stream_id, panelmember_id):
        self.name = name
        self.panelmember_id = panelmember_id
        self.stream_id = stream_id


class ProjectStream(db.Model):
    __tablename__ = 'projectstream'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id'))
    stream_id = db.Column(db.Integer, db.ForeignKey(
        'stream.id'))
    required_people = db.Column(db.Integer)

    def __init__(self, name, stream_id, project_id, required_people):
        self.name = name
        self.project_id = project_id
        self.stream_id = stream_id
        self.required_people = required_people


class CandidateStatus(db.Model):
    __tablename__ = 'candidatestatus'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projectstream.id'))
    roundstatus_id = db.Column(db.Integer, db.ForeignKey('roundstatus.id'))
    finalstatus = db.Column(db.String(30))
    hr_remarks = db.Column(db.String(200))

    def __init__(self, id, candidate_id, project_id, roundstatus_id, finalstatus, hr_remarks):
        self.id = id
        self.candidate_id = candidate_id
        self.project_id = project_id
        self.roundstatus_id = roundstatus_id
        self.finalstatus = finalstatus
        self.hr_remarks = hr_remarks


class RoundStatus(db.Model):
    __tablename__ = 'roundstatus'
    id = db.Column(db.Integer, primary_key=True)
    round_num = db.Column(db.Integer)
    round_name = db.Column(db.String(20))
    panel_id = db.Column(db.Integer, db.ForeignKey('panelmember.id'))
    status = db.Column(db.String(20))
    rating = db.Column(db.Integer)
    remarks = db.Column(db.Integer)

    def __init__(self, id, round_num, round_name, panel_id, status, rating, remarks):
        self.id = id
        self.round_num = round_num
        self.round_name = round_name
        self.panel_id = panel_id
        self.status = status
        self.rating = rating
        self.remarks = remarks


class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


class StreamSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


class PanelMemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

stream_schema = StreamSchema()
streams_schema = StreamSchema(many=True)

panelmember_schema = PanelMemberSchema()
panelmembers_schema = PanelMemberSchema(many=True)


# Creating a project or get all projects
@app.route('/project', methods=['GET', 'POST'])
def projects():
    if request.method == "POST":
        name = request.json['name']
        description = request.json['description']
        new_project = Project(name, description)

        db.session.add(new_project)
        db.session.commit()
        return project_schema.jsonify(new_project)

    else:
        all_projects = Project.query.all()
        result = projects_schema.dump(all_projects)
        return jsonify(result)


# Get single project
@app.route('/project/<id>', methods=['GET'])
def get_project(id):
    project = Project.query.get(id)
    return project_schema.jsonify(project)

# Update project


@app.route('/project/<id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get(id)
    name = request.json['name']
    description = request.json['description']
    project.name = name
    project.description = description
    db.session.commit()
    return project_schema.jsonify(project)

# Delete Project


@app.route('/project/<id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    return project_schema.jsonify(project)


# Creating a project or get all streams
@app.route('/stream', methods=['GET', 'POST'])
def streams():
    if request.method == "POST":
        name = request.json['name']
        description = request.json['description']
        new_stream = Stream(name, description)

        db.session.add(new_stream)
        db.session.commit()
        return stream_schema.jsonify(new_stream)

    else:
        all_streams = Stream.query.all()
        result = streams_schema.dump(all_streams)
        return jsonify(result)


# Get single stream
@app.route('/stream/<id>', methods=['GET'])
def get_stream(id):
    stream = Stream.query.get(id)
    return stream_schema.jsonify(stream)

# Update stream


@app.route('/stream/<id>', methods=['PUT'])
def update_stream(id):
    stream = Stream.query.get(id)
    name = request.json['name']
    description = request.json['description']
    stream.name = name
    stream.description = description
    db.session.commit()
    return stream_schema.jsonify(stream)

# Delete stream


@app.route('/stream/<id>', methods=['DELETE'])
def delete_stream(id):
    stream = Stream.query.get(id)
    db.session.delete(stream)
    db.session.commit()
    return stream_schema.jsonify(stream)


# Creating a panelmember or get all panelmembers
@app.route('/panelmember', methods=['GET', 'POST'])
def panelmembers():
    if request.method == "POST":
        name = request.json['name']
        email = request.json['email']
        new_panelmember = PanelMember(name, email)

        db.session.add(new_panelmember)
        db.session.commit()
        return panelmember_schema.jsonify(new_panelmember)

    else:
        all_streams = PanelMember.query.all()
        result = panelmembers_schema.dump(all_streams)
        return jsonify(result)


# Get single panelmember
@app.route('/panelmember/<id>', methods=['GET'])
def get_panelmember(id):
    panelmember = PanelMember.query.get(id)
    return panelmember_schema.jsonify(panelmember)


# Update panelmember
@app.route('/panelmember/<id>', methods=['PUT'])
def update_panelmember(id):
    panelmember = PanelMember.query.get(id)
    name = request.json['name']
    email = request.json['email']
    panelmember.name = name
    panelmember.email = email
    db.session.commit()
    return panelmember_schema.jsonify(panelmember)

# Delete panelmember


@app.route('/panelmember/<id>', methods=['DELETE'])
def delete_panelmember(id):
    panelmember = PanelMember.query.get(id)
    db.session.delete(panelmember)
    db.session.commit()
    return panelmember_schema.jsonify(panelmember)


@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})


if __name__ == '__main__':
    app.run(debug=True)
