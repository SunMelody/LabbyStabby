import os
from flask import Flask
from flask import request
from flask import json
from flask import send_file
from flask import send_from_directory

app = Flask(__name__)

#переход в корень
def RootWay():
    try:
        os.chdir('./root')
    except FileNotFoundError:
        while os.path.basename(os.getcwd()) != 'root':
            os.chdir('..')

#создание папки по имени
def FolderAdd(name):
    os.mkdir(name)

#удаление папки
def DelEmptyFolder(name):
    try:
        os.rmdir(name)
    except OSError:
        print('There is empty folder')

#скачивание файла
def FileGet(name):
    return send_from_directory(os.path.join(app.instance_path, ''), name)

#описание пути к файлу/папке
def PathList():
    list = [];
    for name in os.listdir():
        Path = './' + name
        if os.path.isfile(Path):
            type = 'file'
        else:
            type = 'folder'
        obj = {'name': name, 'type': type}
        list.append(obj)
    return json.dumps(list, ensure_ascii=False);

@app.route('/')
@app.route('/index/')
@app.route('/root/')
#работа с папками 
def index():
    fold = request.args.get('folder', 0, int)
    file = request.args.get('file', 0, int)
    name = request.args.get('name', None, str)
    goToRoot()
    if (fold == 1) & (name != None):
        FolderAdd(name)
    elif (fold == 2) & (name != None):
        DelEmptyFolder(name)
    if (file == 1) & (name != None):
        FileGet(name)
    return PathList()

@app.route('/root/<path:path>')
def dir(path):
    fold = request.args.get('folder', 0, int)
    file = request.args.get('file', 0, int)
    name = request.args.get('name', None, str)
    if (file == 1) & (name != None):
        send_file('./root/'+path+'/'+name, as_attachment=True)
    RootWay()
    os.chdir('./'+path)
    if (fold == 1) & (name != None):
        FolderAdd(name)
    elif (fold == 2) & (name != None):
        DelEmptyFolder(name)
    if (file == 1) & (name != None):
        FileGet(name)
    return PathList()

if __name__ == '__main__':
    app.run()
