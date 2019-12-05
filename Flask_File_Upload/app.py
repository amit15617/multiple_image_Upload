from flask import Flask, redirect, render_template, request, session, url_for
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class, UploadNotAllowed
import os
from flask import flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkeygoeshere'

dropzone = Dropzone(app)
# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*, .pdf, .txt, .csv'
# app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'text/csv, image/*'

app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

# Uploads settings
# app.config['UPLOADED_FILES_DEST'] = 'static/uploadstorage'
#*****************
# app.config['UPLOADED_FILES_DEST'] = os.getcwd() + '/uploads'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
# files = UploadSet('files', ('csv',))

# configure_uploads(app, files)

#*************************************
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
#*****************************************
patch_request_class(app)  # set maximum file size, default is 16MB


@app.route('/', methods=['GET', 'POST'])
def index():
    print('check1')
    print(IMAGES)
    # set session for image results
    if "file_urls" not in session:
        print('check2')
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']
    # handle image upload from Dropzone
    
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename    
            )
            # append image urls
            file_urls.append(photos.url(filename))
            
        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request    
    return render_template('index.html')


@app.route('/results')
def results():
    
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    session.pop('file_urls', None)
    
    return render_template('results.html', file_urls=file_urls)


if __name__ == '__main__':
    app.run(debug=True,
            port=5000)


# @app.route('/datauploads', methods=['GET', 'POST'])
# def datauploads():
#     if request.method == 'POST' and 'csv_data' in request.files:
#         try:
#             filename = csv_file.save(request.files['csv_data'])
#             return render_template('results.html', filename=filename)
#         except UploadNotAllowed:
#             flash('Only CSV files can be uploaded, please correct', 'error')

#     return render_template('index.html')