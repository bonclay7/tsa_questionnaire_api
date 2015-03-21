from flask.ext.restful.utils.cors import crossdomain
from models.publication import Publication

__author__ = 'grk'
from flask import request, abort
from flask.ext.restful import Resource, reqparse, fields, marshal_with
from resources import mongo, swagger, SUPER_USER, authorize, get_id
from models.quiz import creation_parser, Quiz, QuizStats, patch_parser, put_parser
from models.user import User, post_parser, user_fields
from models.contact import Contact
import hashlib
from datetime import datetime
import smtplib
from email.mime.text import MIMEText


class PublicationServices(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Content-Type", type=str, location='headers', required=True,
                                 help="Content Type must be application/json")
        self.parser.add_argument("Authorization", type=str, location='headers', required=True,
                                 help="Authorization header missing")


    def post(self, quiz_id, contact_group=None):
        session = authorize(request.headers["Authorization"])

        if contact_group is None: contact_group = "default"

        contacts = self.get_contacts(contact_group, session.get("user").get("login"))

        if contacts is None:
            return {"message": "no contact to send"}, 400

        criteria = {"createdBy": session.get('user').get('login'), "_id": int(quiz_id)}
        quiz = Quiz.quiz_from_dict(mongo.db.quiz.find_one_or_404(criteria))

        for contact in contacts:
            c = Contact.contact_from_dict(contact)
            p = Publication()
            p._id = get_id("publication")
            p.creationDate = datetime.now()
            p.hash = hashlib.sha256("%d.%s" % (p._id, str(p.creationDate))).hexdigest()
            p.by = session.get('user').get('login')
            p.quiz = quiz
            p.to =  c
            mongo.db.publications.insert(p.format())
            self.send_email(quiz.title, p.hash, c.email, c.language)

        return {"message": "quiz %s published to %d contacts" % (quiz.title, len(contacts))}, 200




    def get_contacts(self, group_name, owner):
        res = mongo.db.contacts_groups.find_one({"name": group_name, "owner": owner})
        if not (res is None):
            return res.get("contacts")
        return None



    def send_email(self, quiz_title, pub_hash, to, lang):
        me = "sio.autismgroup@gmail.com"
        url = "http://127.0.0.1:8080/participation/%s/" % pub_hash

        msg = MIMEText("You have been invited to participate to a survey at %s" % url)
        msg["Subject"] = "Survey - %s" % quiz_title
        msg["From"] = me
        msg["To"] = to

        s = smtplib.SMTP('smtp.gmail.com:587')
        s.starttls()
        #s = smtplib.SMTP('aspmx.l.google.com:25')
        s.login(me, "4DQGyP3JponyD")
        s.sendmail(me, [to], msg.as_string())
        s.quit()