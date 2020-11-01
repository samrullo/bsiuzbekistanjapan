import os
from application import db
from application.post_weight.models import PostWeightContent
from flask import current_app, session
import logging
import boto3
from botocore.exceptions import ClientError
import tinify
from application import images
from threading import Thread
from application import create_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class S3Uploader:
    def __init__(self):
        self.name = "s3uploader"

    def save_file(self, filename):
        """
        save file in the local folder
        """
        saved_filename = images.save(filename)
        optimized_filename = 'optimized_' + saved_filename
        tinify.key = current_app.config['TINIFY_API_KEY']
        logging.info(
            f"Will try tinify.from_file {os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], saved_filename)}")
        source = tinify.from_file(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], saved_filename))
        resized = source.resize(method='fit', width=current_app.config['PHOTO_WIDTH'],
                                height=current_app.config['PHOTO_HEIGHT'])
        resized.to_file(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], optimized_filename))

        # remove original file
        os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], saved_filename))
        return optimized_filename

    def upload_file(self, file_name, bucket_name, object_name=None):
        """
        uploads the file to s3 bucket
        """
        if not object_name:
            object_name = file_name
        s3_client = boto3.client('s3', aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
                                 aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])
        try:
            response = s3_client.upload_file(file_name, bucket_name, object_name, ExtraArgs={'ACL': 'public-read'})
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_file_async_target_func(self, app, file_name, bucket_name, object_name=None):
        """
        uploads the file to s3 bucket
        """
        with app.app_context():
            if not object_name:
                object_name = file_name
            s3_client = boto3.client('s3', aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
                                     aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])
            try:
                response = s3_client.upload_file(file_name, bucket_name, object_name, ExtraArgs={'ACL': 'public-read'})
            except ClientError as e:
                logging.error(e)
                return False

    def upload_file_async(self, file_name, bucket_name, object_name=None):
        new_app = create_app(os.environ['FLASK_ENV'])
        thr = Thread(target=self.upload_file_async_target_func,
                     args=[new_app, file_name, bucket_name, object_name])
        thr.start()
        return thr

    def upload_photo_to_s3_bucket(self, file_field_data, new_filename, s3_folder):
        img_filename = self.save_file(file_field_data)
        new_img_filename = "_".join(new_filename.lower().split())
        s3_object_name = f"{current_app.config['BUCKET_FOLDER']}/{s3_folder}/{new_img_filename}"
        if self.upload_file(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], img_filename),
                            current_app.config['BUCKET_NAME'], s3_object_name):
            photo_url = f"{current_app.config['BUCKET_URL']}/{s3_object_name}"

            # remove file in local
            os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], img_filename))
            return photo_url
        else:
            logging.error(f"Something went wrong when uploading {file_field_data} to s3 bucket")

    def upload_photo_to_s3_bucket_asynch_target_func(self, app, file_field_data, new_filename, s3_folder,
                                                     post_weight_content):
        with app.app_context():
            img_filename = self.save_file(file_field_data)
            new_img_filename = "_".join(new_filename.lower().split())
            s3_object_name = f"{current_app.config['BUCKET_FOLDER']}/{s3_folder}/{new_img_filename}"
            if self.upload_file(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], img_filename),
                                current_app.config['BUCKET_NAME'], s3_object_name):
                photo_url = f"{current_app.config['BUCKET_URL']}/{s3_object_name}"

                # remove file in local
                os.remove(os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], img_filename))
                post_weight_content.content_image_url = photo_url

                # get db session from session factory
                session_factory = sessionmaker(db.engine)
                Session = scoped_session(session_factory)
                db_session = Session()
                db_session.add(post_weight_content)
                db_session.commit()
            else:
                logging.error(f"Something went wrong when uploading {file_field_data} to s3 bucket")

    def upload_photo_to_s3_asynch(self, file_field_data, new_filename, s3_folder, post_weight_content):
        new_app = create_app(os.environ['FLASK_ENV'])
        thr = Thread(target=self.upload_photo_to_s3_bucket_asynch_target_func,
                     args=[new_app, file_field_data, new_filename, s3_folder, post_weight_content])
        thr.start()
        return thr
