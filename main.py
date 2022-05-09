import sys, os
from flask import Flask  
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from flask import Flask, request, Response, jsonify, render_template
from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
import json

app = Flask(__name__, template_folder='template') #creating the Flask class object 
app.config["BUNDLE_ERRORS"] = True 
api = Api(app) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' 

db = SQLAlchemy(app)
ma = Marshmallow(app)

class user(db.Model):
    id = db.Column("user_id", db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=None)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        # model = user
        id = fields.Integer()
        name = fields.Str()
        email = fields.Str()
        phone = fields.Integer()
        created_date = fields.DateTime()
        modified_at = fields.DateTime()
        load_instance = True
        include_fk = True

user_schema = UserSchema(many = True)

db.create_all()

class UserGet(Resource):
    def get(self):
        data_dict = []
        APIdata = user.query.all()
        # APIdata = user.get_all()
        # output = user_schema.dumps(APIdata)

        for x in APIdata:
            temp = {}
            if x.modified_at == None:
                x.modified_at = x.modified_at
            else:
                x.modified_at = x.modified_at.isoformat()         
            temp["id"] = x.id
            temp["name"] = x.name
            temp["email"] = x.email
            temp["phone"] = x.phone
            temp["created_date"] = x.created_date.isoformat()
            temp["modified_at"] = x.modified_at
            # output = UserSchema().dump(x)
            # data_dict = UserSchema.dump(temp)
            data_dict.append(temp)
        # output = user_schema.dump(data_dict)
        # print(user_schema.validate(temp))
        print(APIdata)
        return {"data":data_dict}

class UserPost(Resource):
    def post(self):
        # ids = request.args.get("id", type=int)
        # name = request.args.get("name", type=str)
        # email = request.args.get("email", type=str)
        # phone = request.args.get("phone", type=int)
        ids = request.json['id']
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']

        user_data = user(id=ids,name=name,email=email,phone=phone)
        db.session.add(user_data)
        db.session.commit()
        # temp = UserSchema().dump(user_data)
        # data=user_schema.dump(user_data)
        # # print(UserSchema().jsonify(user_data))
        # print(user_schema().load(user_data))
        # return UserSchema().jsonify(user_data)
        # return {"message": "DATA CREATED"}
        if user_data.modified_at == None:
            user_data.modified_at = user_data.modified_at
        else:
            user_data.modified_at = user_data.modified_at.isoformat()

        return {"DATA":{"id":user_data.id, 
                        "name":user_data.name,
                        "email":user_data.email,
                        "phone":user_data.phone,
                        "created_date":user_data.created_date.isoformat(),
                        "modified_at":user_data.modified_at
                        }}

class Userput(Resource):
    def put(self, objectdata):
        userd = user.query.get_or_404(int(objectdata))
        args = request.get_json()
        userd.name = request.json['name']
        userd.email = request.json['email']
        userd.phone = request.json['phone']
        userd.created_date = userd.created_date
        userd.modified_at = datetime.utcnow()

        db.session.add(userd)
        db.session.commit()
        
        return {"DATA":{"id":userd.id,
                "name":userd.name,
                "email":userd.email,
                "phone": userd.phone,
                "created_data": userd.created_date.isoformat(),
                "modified_at": userd.modified_at.isoformat()
                }}

class Userdel(Resource):
    def delete(self, objectdata):
        print(objectdata)
        userd = user.query.get_or_404(int(objectdata))
        db.session.delete(userd)

        db.session.commit()
        return {"message": "DATA DELETED"}


class viewdata(Resource):
    def get(self):
        users = user.query
        return Response(response=render_template('data.html', title='User Data', users=users))


api.add_resource(UserGet, '/getdata')
api.add_resource(UserPost, '/saveddata')
api.add_resource(Userput, '/putdata/<int:objectdata>')
api.add_resource(Userdel, '/deldata/<int:objectdata>')
api.add_resource(viewdata, '/admin/users')

if __name__ =='__main__':  
    port = int(os.environ.get('PORT', 4001))
    # app.run(host='0.0.0.0', port=sys.argv[1], debug = True)
    app.run(host='0.0.0.0', port=port, debug = True)