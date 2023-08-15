from flask import send_file, request
from gevent import pywsgi
from flask import Flask
import io
import sys
import os
import time
import zipfile
sys.path.append('..')
 
app = Flask(__name__)

def file2zip(zip_file_name: str, file_names: list):
    """ 将多个文件夹中文件压缩存储为zip
    
    :param zip_file_name:   /root/Document/test.zip
    :param file_names:      ['/root/user/doc/test.txt', ...]
    :return: 
    """
    # 读取写入方式 ZipFile requires mode 'r', 'w', 'x', or 'a'
    # 压缩方式  ZIP_STORED： 存储； ZIP_DEFLATED： 压缩存储
    with zipfile.ZipFile(zip_file_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for fn in file_names:
            parent_path, name = os.path.split(fn)
            
            # zipfile 内置提供的将文件压缩存储在.zip文件中， arcname即zip文件中存入文件的名称
            # 给予的归档名为 arcname (默认情况下将与 filename 一致，但是不带驱动器盘符并会移除开头的路径分隔符)
            zf.write(fn, arcname=name)
            
            # 等价于以下两行代码
            # 切换目录， 直接将文件写入。不切换目录，则会在压缩文件中创建文件的整个路径
            # os.chdir(parent_path)
            # zf.write(name)

@app.route("/api/test", methods=["POST"])
def test():
    value = request.form['key']
    return value
 
 
@app.route("/api/upload", methods=["POST"])
def upload():
    """接受前端传送过来的文件"""
    file_obj = request.files.get("file")
    # print(file_obj)
    if file_obj is None:
        return "文件上传为空"
 
    # 直接使用文件上传对象保存
    time_str = time.strftime("%Y%m%d_%H%M%S")
    # print(time_str)
    path = os.getcwd() + '/files/' + time_str + file_obj.filename
    print(path)
    # input(999)
    file_obj.save(path)
    return "文件上传成功\n"
 
 
@app.route('/api/download')
def download():
    """
    简单的文件服务器
    提供文件下载服务
    浏览器下载：示例：文件1.TXT的下载链接：http://127.0.0.1:10011/download?file_name=1.txt
    linux下载：示例：文件1.TXT的下载链接：curl -# -o 1.txt http://127.0.0.1:10011/download?file_name=1.txt
    :return:
    """
    file_name = request.args.get('file_name')
    path = os.getcwd() + '/files/%s' % file_name
    return send_file(path)
 
 
if __name__ == "__main__":
    print('启动成功，端口10011')
    server = pywsgi.WSGIServer(('0.0.0.0', 10011), app)
    server.serve_forever()