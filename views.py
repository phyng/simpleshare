# -*- coding: utf-8 -*- #

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from flask import *
import control
import os
import StringIO
import markdown
import cStringIO, codecs


#Config
global DOMIAN
DOMIAN = 'http://share.phyng.com'


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files['file[0]']
        #存储到数据库并返回uid
        filename = files.filename
        files.save('files.temp')
        files = open('files.temp', 'rb')
        uid = control.SaveToDB(files, filename)
        files.close()
        os.remove('files.temp')
        return str(uid)

    return render_template('index.html', title = 'Simple Share')

@app.route('/f/<int:uid>', methods=['GET'])
def files(uid):
    (uid, files, filename, filetype) = control.ReadDB(uid)

    typedict = {
        'jpg':'image/jpeg',
        'jpeg':'image/jpeg',
        'png':'image/png',
        'bmp':'image/bmp',
        'svg':'image/svg',

        'pdf':'application/pdf',
        'doc':'application/msword',
        'docx':'application/msword',
        'ppt':'application/mspowerpoint',
        'pptx':'application/mspowerpoint',
        'xls':'application/excel',
        'xlsx':'application/excel',

        'flv':'application/x-shockwave-flash',
        'swf':'application/x-shockwave-flash',
        }

    strIO = StringIO.StringIO()
    strIO.write(files)
    strIO.seek(0)
    try:
        return send_file(strIO, attachment_filename=filename, mimetype = typedict[filetype])
    except KeyError:
        return send_file(strIO, attachment_filename=filename, as_attachment=True)

@app.route('/<int:uid>', methods=['GET'])
def page(uid):

    try:
        (uid, files, filename, filetype) = control.ReadDB(uid)
        strIO = StringIO.StringIO()
        strIO.write(files)
        strIO.seek(0)
    except:
        return 'simple 404'

    if filetype in ['png', 'jpg', 'jpeg', 'gif', 'svg', 'bmp']:
        return render_template('photo.html', title = filename, uid = uid)

    elif filetype in ['mp4', 'mp3', 'ogg', 'webm']:
        return render_template('video.html', title = filename, uid = uid)

    elif filetype in ['flv', 'swf']:
        return render_template('flash.html', title = filename, uid = uid)

    elif filetype in ['md', 'txt']:
        try:
            content = Markup(markdown.markdown(strIO.read(), extensions = ['meta']))
            return render_template('md.html', title = filename, content = content)
        except UnicodeDecodeError:
            error = 'UnicodeDecodeError'
            return render_template('md.html', title = filename, error = error)

        

    elif filetype in ['c', 'bat', 'py', 'sh', 'sql', 'bash', 'java', 'vb', 'pm', 'h', 'cpp', 'bas']:
        newstr = '~~~~{.code}\n' + strIO.read() + '\n\n~~~~\n'
        try:
            content = Markup(markdown.markdown(newstr, extensions = ['fenced_code']))
            return render_template('code.html', title = filename, content = content)
        except UnicodeDecodeError:
            error = 'UnicodeDecodeError'
            return render_template('code.html', title = filename, error = error)

    elif filetype =='pdf':
        return render_template('pdf.html', title = filename, uid = uid)

    elif filetype in ['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx']:
        url = DOMIAN + '/f/' +str(uid)
        return render_template('docs.html', title = filename, url = url)

    else:
        return render_template('other.html', title = filename, uid = uid)

if __name__ == '__main__':
    app.debug = True
    app.run(port = 5000)