# train_python

## Image Uploader Application
課題：画像アップローダーアプリケーションを作成します。選択したフロントエンドライブラリを使用し、APIを作成します。
- 画像をドラッグアンドドロップしてアップロードできる 
- フォルダから画像を選択できる
- アップロード時にローダーが表示される 
- 画像をアップロードすると、画像を表示してコピーできる 
- クリップボードにコピーすることを選択できる
  
# note
## プロジェクト
mysite/   プロジェクトのコンテナ。名前は Django にとって重要ではありません。任意の名前に変更できます。
    manage.py  Django プロジェクトに対する様々な操作を行うためのコマンドラインユーティリティ
    mysite/  このプロジェクトの実際の Python パッケージ。
        __init__.py　このディレクトリが Python パッケージであることを Python に知らせるための空のファイル。
        settings.py　Django プロジェクトの設定ファイル
        urls.py　Django プロジェクトの URL 宣言、いうなれば Django サイトにおける「目次」に相当
        asgi.py　プロジェクトを提供する ASGI 互換 Web サーバーのエントリポイント。
        wsgi.py　プロジェクトをサーブするためのWSGI互換Webサーバーとのエントリーポイント
## アプリケーション
application/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py