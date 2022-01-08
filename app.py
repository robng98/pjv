import os, datetime
from sys import path
from flask import Flask, render_template, request, redirect, flash, url_for, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'secret'

BASE_PATH =  '/uploads'
abs_path = os.path.abspath(BASE_PATH)
ALLOWED_EXT = {'txt', 'pdf'}

def allowed_files(filename: str) -> bool :
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def vamover(file):
    for line in file:
        flash(line)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files.get('file')

        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and allowed_files(file.filename):

            #FUNCAO ONDE FICARA TODOS OS SCRIPTS DE POS-PROCESSAMENTO
            script(file)

            # filename = secure_filename(file.filename)
            # file.save(os.path.join('C:/Users/beton/Downloads/ProjetoFlask/uploads', filename))
            return redirect(url_for('download'))

    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():

    date = datetime.datetime.now()

    name = 'Diagnostico_' + date.strftime('%Y_%m_%d_%H_%M_%S') + '.txt'

    return send_file('uploads/temp.txt', mimetype='text', attachment_filename=name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)




def script(file):
    with open('uploads/temp.txt', 'w+') as dest:
            for line in file:
                line_dcd = line.decode('UTF-8')
                line_dcd = line_dcd.replace('$ADC$,', '')
                line_dcd = line_dcd.replace(',', ', ')
                line_dcd = line_dcd.replace('#', ' ')
                line_dcd = line_dcd.replace(',', ' ')
                line_dcd = line_dcd.split()
                # print(line_dcd)
                line_num = [int(val) for val in line_dcd]
                cont = 0

                for val in line_num:
                    cont = cont + val
                
                cont_str = str(cont) + '\n'  
                dest.write(cont_str)
    flash('File uploaded successfully')
    
