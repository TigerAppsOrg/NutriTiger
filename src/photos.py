#----------------------------------------------------------------------
# Contributors:
# Oyu Enkhbold
#
# To support personal nutrition information
#----------------------------------------------------------------------
from bson.objectid import ObjectId
from PIL import Image
import io
from bson.binary import Binary
import os
import cloudinary.uploader
import cloudinary.api
import dotenv

dotenv.load_dotenv()
cloudinary.config(
    cloud_name=os.getenv("cloud_name"), 
    api_key=os.getenv("api_key"), 
    api_secret=os.getenv("api_secret")
)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic'}
    new_filename = filename
    format = new_filename.rsplit('.', 1)[1].lower()

    if format == 'jpg':
        format = 'jpeg'
    if format == 'heic':
        new_filename.replace(".heic", ".jpg")
        format = 'jpeg'
    # os.rename(file, new_filename)
    return '.' in filename and format in ALLOWED_EXTENSIONS, format.upper()

def allowed_size(photo):
    max_size = 10 * 1024 * 1024  # 10 MB in bytes

    # Check the size of the photo
    photo.seek(0, 2)  # Move the read cursor to the end of the file
    file_size = photo.tell()  # Get the position of the cursor—this is the file's size in bytes
    photo.seek(0)  # Reset the cursor to the start of the file

    return file_size <= max_size

# def delete_one_photo(public_id):
#     dotenv.load_dotenv()
#     cloudinary.config(
#         cloud_name=os.getenv("cloud_name"), 
#         api_key=os.getenv("api_key"), 
#         api_secret=os.getenv("api_secret")
#     )
#     try:
#         response = cloudinary.uploader.destroy(public_id)
#         return response  # This will return the result of the delete operation
#     except Exception as e:
#         return {'status': 'error', 'message': str(e)}

# def delete_many_photos(public_ids):
#     dotenv.load_dotenv()
#     cloudinary.config(
#         cloud_name=os.getenv("cloud_name"), 
#         api_key=os.getenv("api_key"), 
#         api_secret=os.getenv("api_secret")
#     )
#     print("inside delete_many_photos:")
#     print(public_ids)
#     try:
#         # Ensure that the 'public_ids' parameter name is used correctly
#         response = cloudinary.api.delete_resources(public_ids=public_ids)
#         print("success in delete_many_photos")
#         return True
#     except Exception as e:
#         print("fails in delete_many_photos")
#         print(f"An error occurred: {str(e)}")
#         # Handle the response in case of an exception
#         # return {"status": "error", "message": str(e)}
#         return False


    



