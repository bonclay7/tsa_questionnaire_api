# -*- coding:utf-8 -*-
from flask.ext.restful import Resource, reqparse, abort
from flask import request
from models.contact import Contact, post_parser
from models.session import Session
from resources import authorize, swagger, mongo, get_id
from datetime import datetime

class ContactsServices(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Content-Type", type=str, location='headers', required=True,
                                 help="Content Type must be application/json")
        self.parser.add_argument("Authorization", type=str, location='headers', required=True,
                                 help="Authorization header missing")

    def post(self, group_name=None):
        session = authorize(request.headers["Authorization"])
        print session

        contacts = post_parser.parse_args().get("contacts")
        if contacts is None:
            abort(403)

        if group_name is None: group_name = "default"

        new_contacts = 0
        existing_contact = 0
        for contact in contacts:
            print contact
            contact = Contact.contact_from_dict(contact)
            existing = mongo.db.contacts.find_one({"email": contact.email})

            if existing is None:
                contact._id = get_id("contacts")
                contact.creationDate = datetime.now()
                contact.createdBy = session.get("user").get("login")
                if contact.language is None:
                    contact.language = "fr"

                mongo.db.contacts.insert(contact.format())

                self.update_group(group_name, contact.createdBy, contact)

                new_contacts += 1
            else:
                existing_contact += 1
                contact = Contact.contact_from_dict(existing)
                self.update_group(group_name, contact.createdBy, contact)



        return {"inserted": new_contacts, "existing": existing_contact}, 200

    def update_group(self, group_name, owner, contact):
        res = mongo.db.contacts_groups.update({"name": group_name, "owner": owner}, {"$push": {"contacts": contact.format()}})

        if not res.get("updatedExisting"):
            mongo.db.contacts_groups.insert({"name": group_name, "owner": owner, "creationDate": datetime.now(), "contacts": []})
            self.update_group(group_name, owner, contact)


    def get(self, contact_id=None):
        authorize(request.headers["Authorization"])

        if contact_id is None:
            return self.get_all_contacts()
        else:
            return self.get_a_contact(contact_id)



    def get_all_contacts(self):
        contacts = []
        for c in mongo.db.contacts.find():
            contacts.append(Contact.contact_from_dict(c).format())

        return contacts, 200

    def get_a_contact(self, contact_id):
        c = mongo.db.contacts.find_one_or_404({"_id": contact_id})
        return c.contact_from_dict(c).format(), 200


    def delete(self, contact_id):
        authorize(request.headers["Authorization"])

        existing = mongo.db.contacts.find_one_or_404({"_id": contact_id})

        c_delete = existing.contact_from_dict(existing)
        c_delete.deleteDate = datetime.now()

        delete_id = mongo.db.contacts_deleted.insert(c_delete.format_for_delete())

        mongo.db.contacts.remove({"_id": contact_id})

        print "deleted : ", delete_id

        return {"message": "deleted"}, 200




class ContactsGroupsServices(Resource):
    pass