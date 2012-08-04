from screenchop import config

ALLOWED_EXTENSIONS = set(config.ALLOWED_FILE_TYPES)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
