pip install -r requirements.txt
pip install --upgrade --force-reinstall whls/PyOpenGL-3.1.7-cp310-cp310-win_amd64.whl
pip install nuitka
pip install pyinstaller
::pyinstaller --onefile --add-data="%LocalAppData%\Programs\Python\Python310\Lib\site-packages\openal\*;." --add-data="%LocalAppData%\Programs\Python\Python310\Lib\site-packages\glfw\*;." __main__.py
python -m nuitka --include-plugin-directory=%LocalAppData%\Programs\Python\Python310\Lib\site-packages\openal --include-plugin-directory=%LocalAppData%\Programs\Python\Python310\Lib\site-packages\glfw __main__.py