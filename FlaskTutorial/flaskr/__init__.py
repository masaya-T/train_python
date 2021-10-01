import os

from flask import Flask


def create_app(test_config=None):
    '''
    _name__は、現在のPythonモジュールの名前です。
    アプリは、いくつかのパスを設定するためにアプリがどこにあるかを知る必要があり、__ name__はそれを伝えるための便利な方法です。 
    instance_relative_config = Trueは、構成ファイルがインスタンスフォルダーに関連していることをアプリに通知します。
    インスタンスフォルダはflaskrパッケージの外部にあり、構成シークレットやデータベースファイルなど、バージョン管理にコミットしてはならないローカルデータを保持できます。
    '''
    # create and configure the app.
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
