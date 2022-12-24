from re import S
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import json

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:pass@localHost:5432/Dummy2"
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

    def __init__(self, name, email, stream_id):
        self.name = name
        self.email = email
        self.stream_id = stream_id


class Candidate(db.Model):
    __tablename__ = 'candidate'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    mobile = db.Column(db.BigInteger)
    entry_type = db.Column(db.String(50))
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id'))
    stream_id = db.Column(db.Integer, db.ForeignKey(
        'stream.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    candidate_status = db.relationship(
        'RoundStatus', backref='candidatestatus', lazy=True)

    def __init__(self, name, email, mobile, project_id, stream_id, entry_type, status_id):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.project_id = project_id
        self.stream_id = stream_id
        self.entry_type = entry_type
        self.status_id = status_id


class PanelPool(db.Model):
    __tablename__ = 'panelpool'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    panelmember_id = db.Column(db.Integer, db.ForeignKey(
        'panelmember.id'))

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


class RoundStatus(db.Model):
    __tablename__ = 'roundstatus'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    round_num = db.Column(db.Integer)
    round_name = db.Column(db.String(20))
    panel_id = db.Column(db.Integer, db.ForeignKey('panelmember.id'))
    status = db.Column(db.String(20))
    rating = db.Column(db.Integer)
    remarks = db.Column(db.String(2000))

    def __init__(self, candidate_id, round_num, round_name, panel_id, status, rating, remarks):
        self.candidate_id = candidate_id
        self.round_num = round_num
        self.round_name = round_name
        self.panel_id = panel_id
        self.status = status
        self.rating = rating
        self.remarks = remarks


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, name) -> None:
        self.name = name


class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'Description')


class StreamSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


class PanelMemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'stream_id')


class PanelMemberStreamSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'stream_id', 'stream_name')


class CandidateSchema(ma.Schema):
    class Meta:
        feilds = ('id', 'name', 'email', 'mobile',
                  'entry_type', 'project_id', 'stream_id')


class RoundStatusSchema(ma.Schema):
    class Meta:
        fields = ('id', 'candidate_id', 'round_num', 'round_name',
                  'panel_id', 'status', 'rating', 'remarks')


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

stream_schema = StreamSchema()
streams_schema = StreamSchema(many=True)

panelmember_schema = PanelMemberSchema()
panelmembers_schema = PanelMemberSchema(many=True)

panelmember_stream_schema = PanelMemberStreamSchema()
panelmembers_stream_schema = PanelMemberStreamSchema(many=True)


candidate_schema = CandidateSchema()
candidates_schema = CandidateSchema(many=True)

roundstatus_schema = RoundStatusSchema()
roundstatusall_schema = RoundStatusSchema(many=True)


# Creating a project or get all projects


@app.route('/api/project', methods=['GET', 'POST'])
def projects():
    if request.method == "POST":
        name = request.json['name']
        Description = request.json['Description']
        new_project = Project(name, Description)

        db.session.add(new_project)
        db.session.commit()
        return project_schema.jsonify(new_project)

    else:
        all_projects = Project.query.all()
        result = projects_schema.dump(all_projects)
        return jsonify(result)


# Get single project
@app.route('/api/project/<id>', methods=['GET'])
def get_project(id):
    project = Project.query.get(id)
    return project_schema.jsonify(project)

# Update project


@app.route('/api/project/<id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get(id)
    name = request.json['name']
    description = request.json['description']
    project.name = name
    project.description = description
    db.session.commit()
    return project_schema.jsonify(project)

# Delete Project


@app.route('/api/project/<id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    return project_schema.jsonify(project)


# Creating a project or get all streams
@app.route('/api/stream', methods=['GET', 'POST'])
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
@app.route('/api/stream/<id>', methods=['GET'])
def get_stream(id):
    stream = Stream.query.get(id)
    return stream_schema.jsonify(stream)

# Update stream


@app.route('/api/stream/<id>', methods=['PUT'])
def update_stream(id):
    stream = Stream.query.get(id)
    name = request.json['name']
    description = request.json['description']
    stream.name = name
    stream.description = description
    db.session.commit()
    return stream_schema.jsonify(stream)

# Delete stream


@app.route('/api/stream/<id>', methods=['DELETE'])
def delete_stream(id):
    stream = Stream.query.get(id)
    db.session.delete(stream)
    db.session.commit()
    return stream_schema.jsonify(stream)


# Creating a panelmember or get all panelmembers
@app.route('/api/panelmember', methods=['GET', 'POST'])
def panelmembers():
    if request.method == "POST":
        name = request.json['name']
        email = request.json['email']
        stream_id = request.json['stream_id']
        new_panelmember = PanelMember(name, email, stream_id)

        db.session.add(new_panelmember)
        db.session.commit()
        return panelmember_schema.jsonify(new_panelmember)

    else:
        all_panels = db.session.query(PanelMember.id, PanelMember.name, PanelMember.email, Stream.id, Stream.name).outerjoin(
            Stream, PanelMember.stream_id == Stream.id).all()
        keys = ['id', 'name', 'email', 'stream_id', 'stream_name']
        if all_panels == None:
            return "No panels avalible in list"
        data = [dict(zip(keys, panel)) for panel in all_panels]
        json_data = json.dumps(data, indent=2)
        db.session.commit()
        return json_data


# Get single panelmember
@app.route('/api/panelmember/<id>', methods=['GET'])
def get_panelmember(id):
    all_panel = db.session.query(PanelMember.id, PanelMember.name, PanelMember.email, Stream.id, Stream.name).outerjoin(
        Stream, PanelMember.stream_id == Stream.id).filter(PanelMember.id == id).first()
    keys = ['id', 'name', 'email', 'stream_id', 'stream_name']
    if all_panel == None:
        return "No panels avalible in list"
    data = dict(zip(keys, all_panel))
    json_data = json.dumps(data, indent=2)
    db.session.commit()
    return json_data


# Update panelmember
@app.route('/api/panelmember/<id>', methods=['PUT'])
def update_panelmember(id):
    panelmember = PanelMember.query.get(id)
    name = request.json['name']
    email = request.json['email']
    panelmember.name = name
    panelmember.email = email
    db.session.commit()
    return panelmember_schema.jsonify(panelmember)

# Delete panelmember


@app.route('/api/panelmember/<id>', methods=['DELETE'])
def delete_panelmember(id):
    panelmember = PanelMember.query.get(id)
    db.session.delete(panelmember)
    db.session.commit()
    return panelmember_schema.jsonify(panelmember)


# Creating a candidate or get all candidate
@app.route('/api/candidate', methods=['GET', 'POST'])
def candidate():
    if request.method == "POST":
        name = request.json['name']
        email = request.json['email']
        mobile = request.json['mobile']
        entry_type = request.json['entry_type']
        project_id = request.json['project_id']
        stream_id = request.json['stream_id']
        status_id = request.json['status_id']
        new_candidate = Candidate(
            name, email, mobile, project_id, stream_id, entry_type, status_id)

        db.session.add(new_candidate)
        db.session.commit()
        return candidate_schema.jsonify(new_candidate)

    else:
        all_candidates = db.session.query(Candidate.id, Candidate.name, Candidate.email, Candidate.mobile, Candidate.entry_type, Project.id, Project.name,
                                          Stream.id, Stream.name, Status.name).outerjoin(Project, Candidate.project_id == Project.id).outerjoin(Stream, Candidate.stream_id == Stream.id).outerjoin(Status, Candidate.status_id == Status.id).all()
        print(all_candidates)
        keys = ['id', 'name', 'email', 'mobile', 'entry_type',
                'project_id', 'project_name', 'stream_id', 'stream_name', 'status_name']
        if all_candidates == None:
            return "No candidates avalible in list"
        data = [dict(zip(keys, candidate)) for candidate in all_candidates]
        json_data = json.dumps(data, indent=9)
        db.session.commit()
        return json_data

# Get single candidate


@app.route('/api/candidate/<id>', methods=['GET'])
def get_candidate(id):
    candidate = db.session.query(Candidate.id, Candidate.name, Candidate.email, Candidate.mobile, Candidate.entry_type, Project.id, Project.name,
                                 Stream.id, Stream.name, Status.name).outerjoin(Project, Candidate.project_id == Project.id).outerjoin(Stream, Candidate.stream_id == Stream.id).outerjoin(Status, Candidate.status_id == Status.id).filter(Candidate.id == id).first()
    keys = ['id', 'name', 'email', 'mobile', 'entry_type',
            'project_id', 'project_name', 'stream_id', 'stream_name', 'status_name']
    if candidate == None:
        return "Candidate not found"
    data = dict(zip(keys, candidate))
    json_data = json.dumps(data, indent=9)
    db.session.commit()
    return json_data

# Update candidate


@app.route('/api/candidate/<id>', methods=['PUT'])
def update_candidate(id):
    candidate = Candidate.query.get(id)
    name = request.json['name']
    email = request.json['email']
    mobile = request.json['mobile']
    entry_type = request.json['entry_type']
    project_id = request.json['project_id']
    stream_id = request.json['stream_id']
    status_id = request.json['status_id']
    candidate.name = name
    candidate.email = email
    candidate.mobile = mobile
    candidate.entry_type = entry_type
    candidate.project_id = project_id
    candidate.stream_id = stream_id
    candidate.status_id = status_id
    db.session.commit()
    return candidate_schema.jsonify(candidate)

# Delete candidate


@app.route('/api/candidate/<id>', methods=['DELETE'])
def delete_candidate(id):
    candidate = Candidate.query.get(id)
    db.session.delete(candidate)
    db.session.commit()
    return candidate_schema.jsonify(candidate)

# Round Status
# Creating a round or get all round


@app.route('/api/project/status', methods=['GET'])
@app.route('/api/candidate/status', methods=['GET'])
@app.route('/api/roundstatus', methods=['GET', 'POST'])
def roundstatus():
    if request.method == "POST":
        candidate_id = request.json['candidate_id']
        round_num = request.json['round_num']
        round_name = request.json['round_name']
        panel_id = request.json['panel_id']
        status = request.json['status']
        rating = request.json['rating']
        remarks = request.json['remarks']
        new_round = RoundStatus(candidate_id, round_num,
                                round_name, panel_id, status, rating, remarks)
        db.session.add(new_round)
        db.session.commit()
        return roundstatus_schema.jsonify(new_round)

    else:
        all_rounds = db.session.query(RoundStatus.id, Candidate.id, Candidate.name, RoundStatus.round_num, RoundStatus.round_name, PanelMember.id, PanelMember.name, Project.id, Project.name, Stream.id, Stream.name, RoundStatus.status, RoundStatus.rating, RoundStatus.remarks).outerjoin(
            Candidate, RoundStatus.candidate_id == Candidate.id).outerjoin(PanelMember, RoundStatus.panel_id == PanelMember.id).outerjoin(Project, Candidate.project_id == Project.id).outerjoin(Stream, Candidate.stream_id == Stream.id).all()

        keys = ['id', 'Candidate_id', 'Candidate_name', 'Round_number', 'Round_name', 'Panel_id',
                'Panel_member_name', 'project_id', 'project_name', 'stream_id', 'stream_name', 'status', 'rating', 'remarks']
        if all_rounds == None:
            return "No rounds avalible in list"
        data = [dict(zip(keys, round)) for round in all_rounds]
        json_data = json.dumps(data, indent=9)
        db.session.commit()
        return json_data


# Get single round
@app.route('/api/roundstatus/<id>', methods=['GET'])
def get_roundstatus(id):
    rounds = db.session.query(RoundStatus.id, Candidate.id, Candidate.name, RoundStatus.round_num, RoundStatus.round_name, PanelMember.id, PanelMember.name, Project.id, Project.name, Stream.id, Stream.name, RoundStatus.status, RoundStatus.rating, RoundStatus.remarks).outerjoin(
        Candidate, RoundStatus.candidate_id == Candidate.id).outerjoin(PanelMember, RoundStatus.panel_id == PanelMember.id).outerjoin(Project, Candidate.project_id == Project.id).outerjoin(Stream, Candidate.stream_id == Stream.id).filter(RoundStatus.id == id).first()
    keys = ['id', 'Candidate_id', 'Candidate_name', 'Round_number', 'Round_name', 'Panel_id',
            'Panel_member_name', 'project_id', 'project_name', 'stream_id', 'stream_name', 'status', 'rating', 'remarks']
    if rounds == None:
        return "round not found"
    data = [dict(zip(keys, rounds))]
    json_data = json.dumps(data, indent=9)
    db.session.commit()
    return json_data

# Update round


@app.route('/api/roundstatus/<id>', methods=['PUT'])
def update_roundstatus(id):
    round = RoundStatus.query.get(id)
    candidate_id = request.json['candidate_id']
    round_num = request.json['round_num']
    round_name = request.json['round_name']
    panel_id = request.json['panel_id']
    status = request.json['status']
    rating = request.json['rating']
    remarks = request.json['remarks']

    round.candidate_id = candidate_id
    round.round_num = round_num
    round.round_name = round_name
    round.panel_id = panel_id
    round.status = status
    round.rating = rating
    round.remarks = remarks
    db.session.commit()
    return roundstatus_schema.jsonify(round)

# Delete Rounds


@app.route('/api/roundstatus/<id>', methods=['DELETE'])
def delete_rounds(id):
    round = RoundStatus.query.get(id)
    db.session.delete(round)
    db.session.commit()
    return roundstatus_schema.jsonify(candidate)


# Extra Api endpoints
# Get single candidate status
@app.route('/api/candidate/<id>/status', methods=['GET'])
def get_candidatestatus(id):
    candidate_status = db.session.query(RoundStatus.id, Candidate.id, Candidate.name, RoundStatus.round_num, RoundStatus.round_name, PanelMember.id, PanelMember.name, Project.id, Project.name, Stream.id, Stream.name, RoundStatus.status, RoundStatus.rating, RoundStatus.remarks).outerjoin(
        Candidate, RoundStatus.candidate_id == Candidate.id).outerjoin(PanelMember, RoundStatus.panel_id == PanelMember.id).outerjoin(Project, Candidate.project_id == Project.id).outerjoin(Stream, Candidate.stream_id == Stream.id).filter(Candidate.id == id).all()
    keys = ['id', 'Candidate_id', 'Candidate_name', 'Round_number', 'Round_name', 'Panel_id',
            'Panel_member_name', 'project_id', 'project_name', 'stream_id', 'stream_name', 'status', 'rating', 'remarks']
    if candidate_status == None:
        return "No Interview Found"
    data = [dict(zip(keys, status)) for status in candidate_status]
    json_data = json.dumps(data, indent=9)
    db.session.commit()
    return json_data

# get panel member status


@app.route('/api/panelmember/status', methods=['GET'])
def get_panels_status():
    panel_status = db.session.query(RoundStatus.id, PanelMember.id, PanelMember.name, RoundStatus.round_num, RoundStatus.round_name, Candidate.id, Candidate.name, Project.id, Project.name, Stream.id, Stream.name, RoundStatus.status, RoundStatus.rating, RoundStatus.remarks).outerjoin(
        Candidate, RoundStatus.candidate_id == Candidate.id).outerjoin(PanelMember, RoundStatus.panel_id == PanelMember.id).outerjoin(Project, Candidate.project_id == Project.id).outerjoin(Stream, Candidate.stream_id == Stream.id).all()
    keys = ['id', 'Panel_member_id', 'Panel_member_name', 'Round_number', 'Round_name', 'Candidate_id',
            'Candidate_name', 'project_id', 'project_name', 'stream_id', 'stream_name', 'status', 'rating', 'remarks']
    if panel_status == None:
        return "round not found"
    data = [dict(zip(keys, status)) for status in panel_status]
    json_data = json.dumps(data, indent=9)
    db.session.commit()
    return json_data

# Get single panel status


@app.route('/api/panelmember/<id>/status', methods=['GET'])
def get_panel_status(id):
    panel_status = db.session.query(RoundStatus.id, PanelMember.id, PanelMember.name, RoundStatus.round_num, RoundStatus.round_name, Candidate.id, Candidate.name, Project.id, Project.name, Stream.id, Stream.name, RoundStatus.status, RoundStatus.rating, RoundStatus.remarks).outerjoin(
        Candidate, RoundStatus.candidate_id == Candidate.id).outerjoin(PanelMember, RoundStatus.panel_id == PanelMember.id).outerjoin(Project, Candidate.project_id == Project.id).outerjoin(Stream, Candidate.stream_id == Stream.id).filter(PanelMember.id == id).all()
    keys = ['id', 'Panel_member_id', 'Panel_member_name', 'Round_number', 'Round_name', 'Candidate_id',
            'Candidate_name', 'project_id', 'project_name', 'stream_id', 'stream_name', 'status', 'rating', 'remarks']
    if panel_status == None:
        return "No Interview Found"
    data = [dict(zip(keys, status)) for status in panel_status]
    json_data = json.dumps(data, indent=9)
    db.session.commit()
    return json_data

# Get project status


@app.route('/api/project/<id>/status', methods=['GET'])
def get_project_status(id):
    project_status = db.session.query(RoundStatus.id, Project.id, Project.name, RoundStatus.round_num, RoundStatus.round_name, Candidate.id, Candidate.name, PanelMember.id, PanelMember.name, Stream.id, Stream.name, RoundStatus.status, RoundStatus.rating, RoundStatus.remarks).outerjoin(
        Candidate, RoundStatus.candidate_id == Candidate.id).outerjoin(PanelMember, RoundStatus.panel_id == PanelMember.id).outerjoin(Project, Candidate.project_id == Project.id).outerjoin(Stream, Candidate.stream_id == Stream.id).filter(Project.id == id).all()
    keys = ['id', 'project_id', 'project_name', 'Round_number', 'Round_name', 'Candidate_id',
            'Candidate_name', 'Panel_member_id', 'Panel_member_name', 'stream_id', 'stream_name', 'status', 'rating', 'remarks']
    if project_status == None:
        return "No Interview Found"
    data = [dict(zip(keys, status)) for status in project_status]
    json_data = json.dumps(data)
    db.session.commit()
    return json_data

# Get project Candidates


@app.route('/api/project/<id>/candidate', methods=['GET'])
def get_project_candidate(id):
    project_candidate = db.session.query(Candidate.id, Candidate.name, Candidate.entry_type, Project.id, Project.name, Status.name).outerjoin(
        Project, Candidate.project_id == Project.id).outerjoin(
        Status, Candidate.status_id == Status.id).filter(Project.id == id).all()
    keys = ['Candidate_id', 'Candidate_name',
            'entry_type', 'project_id', 'project_name', 'status_name']
    if project_candidate == None:
        return "No Candidate Found"
    data = [dict(zip(keys, status)) for status in project_candidate]
    json_data = json.dumps(data)
    db.session.commit()
    return json_data


# Get project Panel Members
@app.route('/api/project/panalmember', methods=['GET'])
def get_project_panels():
    project_panels = db.session.query(RoundStatus.id, RoundStatus.round_name, Project.id, Project.name, PanelMember.id, PanelMember.name).outerjoin(Candidate, RoundStatus.candidate_id == Candidate.id).outerjoin(
        PanelMember, RoundStatus.panel_id == PanelMember.id).outerjoin(Project, Candidate.project_id == Project.id).all()
    keys = ['round_id', 'round_name', 'project_id', 'project_name',
            'Panel_member_id', 'Panel_member_name']
    if project_panels == None:
        return "No PanelMembers Found"
    data = [dict(zip(keys, status)) for status in project_panels]
    json_data = json.dumps(data)
    db.session.commit()
    return json_data

# Get single project Panel Members


@app.route('/api/project/<id>/panalmember', methods=['GET'])
def get_project_panel(id):
    project_panels = db.session.query(RoundStatus.id, RoundStatus.round_name, Project.id, Project.name, PanelMember.id, PanelMember.name).outerjoin(Candidate, RoundStatus.candidate_id == Candidate.id).outerjoin(
        PanelMember, RoundStatus.panel_id == PanelMember.id).outerjoin(Project, Candidate.project_id == Project.id).filter(Project.id == id).all()
    keys = ['round_id', 'round_name', 'project_id', 'project_name',
            'Panel_member_id', 'Panel_member_name']
    if project_panels == None:
        return "No PanelMembers Found"
    data = [dict(zip(keys, status)) for status in project_panels]
    json_data = json.dumps(data)
    db.session.commit()
    return json_data

# Get  project streams


@app.route('/api/project/stream', methods=['GET'])
def get_project_streams():
    project_panels = db.session.query(RoundStatus.id, RoundStatus.round_name, Project.id, Project.name, Stream.id, Stream.name).outerjoin(Candidate, RoundStatus.candidate_id == Candidate.id).outerjoin(
        Project, Candidate.project_id == Project.id).outerjoin(Stream, Candidate.stream_id == Stream.id).all()
    keys = ['round_id', 'round_name', 'project_id', 'project_name',
            'Stream_id', 'Stream_name']
    if project_panels == None:
        return "No Streams Found"
    data = [dict(zip(keys, status)) for status in project_panels]
    json_data = json.dumps(data)
    db.session.commit()
    return json_data

# Get  single project streams


@app.route('/api/project/<id>/stream', methods=['GET'])
def get_project_stream(id):
    project_panels = db.session.query(RoundStatus.id, RoundStatus.round_name, Project.id, Project.name, Stream.id, Stream.name).outerjoin(Candidate, RoundStatus.candidate_id == Candidate.id).outerjoin(
        Project, Candidate.project_id == Project.id).outerjoin(Stream, Candidate.stream_id == Stream.id).filter(Project.id == id).all()
    keys = ['round_id', 'round_name', 'project_id', 'project_name',
            'Stream_id', 'Stream_name']
    if project_panels == None:
        return "No Streams Found"
    data = [dict(zip(keys, status)) for status in project_panels]
    json_data = json.dumps(data, indent=4, separators=(',', ': '))
    db.session.commit()
    return json_data


@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Interview Managment'})


if __name__ == '__main__':
    app.run(debug=True)
