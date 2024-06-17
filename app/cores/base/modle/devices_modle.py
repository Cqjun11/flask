from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flask_test'
db = SQLAlchemy(app)

class devices_list(db.Model):
    __tablename__ = 'devices_list'
    id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, nullable=False)
    device_did = db.Column(db.String(120), nullable=False)
    update_version = db.Column(db.String(120))
    demote_version = db.Column(db.String(120))
    count = db.Column(db.Integer, nullable=False)
    suc_num = db.Column(db.Integer)

    @classmethod
    def add_device(cls, productId, device_did, update_version, demote_version, count):
        if productId and device_did and update_version and demote_version and count:
            new_device = devices_list(productId=productId, device_did=device_did, update_version=update_version, demote_version=demote_version, count=count)
            with app.app_context():
                try:
                    db.session.add(new_device)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
        else:
            print("填写数据不能为空")
            return False

    @classmethod
    def update_suc_num(cls, device_did, suc_num):
        data = devices_list.query.filter_by(device_did=device_did)
        for item in data:
            if item.suc_num < item.count:
                item.suc_num = suc_num
        with app.app_context():
            db.session.commit()

    @classmethod
    def query_all_device(cls):
        with app.app_context():
            query = devices_list.query.all()
        return query

    @classmethod
    def query_device(cls, device_did):
        with app.app_context():
            query = devices_list.query.filter_by(device_did=device_did)
        return query
    @classmethod
    def delete_device(cls, device_did):
        with app.app_context():
            query = devices_list.query.filter_by(device_did=device_did)
            if query:
                query.delete()
                db.session.commit()

class devices_ota_data(db.Model):
    __tablename__ = 'device_ota_data'
    device_did = db.Column(db.String(120), nullable=False, primary_key=True)
    filesize = db.Column(db.String(120), nullable=False)
    versionName = db.Column(db.String(120), nullable=False)
    file_url = db.Column(db.String(120), nullable=False)
    md5 = db.Column(db.String(120), nullable=False)
    sha256 = db.Column(db.String(120))
    version = db.Column(db.Integer, nullable=False)

    @classmethod
    def add_ota_data(cls, device_did, filesize, versionName, file_url, md5, sha256, version):
        with app.app_context():
            try:
                if device_did and filesize and versionName and file_url and version and sha256:
                    device_data = devices_ota_data(device_did=device_did, filesize=filesize, versionName=versionName, file_url=file_url, md5=md5, sha256=sha256, version=version)
                    db.session.add(device_data)
                    db.session.commit()
            except Exception as e:
                db.session.rollback()
    @classmethod
    def query_data(cls):
        with app.app_context():
            query = devices_ota_data.query.all()
        return query

    @classmethod
    def query_data_by_device_did(cls, device_did, version):
        with app.app_context():
            query = devices_ota_data.query.filter_by(device_did=device_did, version=version)
        return query


