import os
import random

from classes.data_manager import DataManager
from .upload_manager import UploadManager
from .exceptions import OutOfFreeNamesError, PictureFormatNotSupportedError, PictureNotUploadedError

from flask import Blueprint, current_app
from flask import Blueprint, request, render_template, current_app

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')



#def get_free_filename(folder, file_type):

  #  attemps = 0
 #   RANGE_OF_IMAGE_NUMBERS = 100
 #   LIMIT_OF_ATTEMPS = 1000

 #   while True:
  #      pic_name = str(random.randint(0, RANGE_OF_IMAGE_NUMBERS))
  #      filename_to_save = f"{pic_name}.{file_type}"
    #    os_path = os.path.join(folder, filename_to_save)
   #     is_filename_occupied = os.path.exists(os_path)

  #      if not is_filename_occupied:
   #         return filename_to_save

  #      attemps += 1

  #      if attemps > LIMIT_OF_ATTEMPS:
 #           raise OutOfFreeNamesError("No free names to save image")

#def is_file_type_valid(file_type):

#    if file_type in ["jpg", "jpeg", "gif", "png", "webp", "tiff"]:
 #       return True
#    return False


@loader_blueprint.route('/post', methods=['GET'])
def page_form():
    return render_template('post_form.html')

@loader_blueprint.route('/post', methods=['POST'])
def page_create_posts():


    path = current_app.config.get("POST_PATH")
    data_manager = DataManager(path)
    upload_manager = UploadManager()

#получаем данные
    picture = request.files.get('picture', None)
    content = request.values.get('content', '')

#сохраняем картинку с помощью менеджера загрузки
    filename_saved = upload_manager.save_with_random_name(picture)
#получаем путь
    web_path = f"/uploads/images/{filename_saved}"

    #создаем данные для записи в файл

    post = {"pic": web_path, "content": content}
#добавляем данные в файл
    data_manager.add(post)

    return render_template('post_uploaded.html', pic=web_path, content=content)

@loader_blueprint.errorhandler(OutOfFreeNamesError)
def error_out_of_free_names(e):
    return "Закончились свободные имена для згрузки картинок. Обратитесь в тех поддержку."

@loader_blueprint.errorhandler(PictureFormatNotSupportedError)
def error_format_not_supported(e):
    return "Формат картинки не поддерживается. Выберите другой."

@loader_blueprint.errorhandler(PictureNotUploadedError)
def error_format_not_supported(e):
    return "Не удалось загрузить картинку"