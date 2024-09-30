pip install -r requirements.txt
pip install --upgrade --force-reinstall whls/PyOpenGL-3.1.7-cp310-cp310-win_amd64.whl
pip install nuitka
python -m nuitka  --output-filename="jesters_bakery" --windows-icon-from-ico=.\jesters_bakery.ico --windows-console-mode=disable --include-plugin-directory=%LocalAppData%\Programs\Python\Python310\Lib\site-packages\openal --include-plugin-directory=%LocalAppData%\Programs\Python\Python310\Lib\site-packages\glfw __main__.py

:: copied from https://superuser.com/questions/392061/how-to-make-a-shortcut-from-cmd
@echo off
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%HOMEDRIVE%%HOMEPATH%\Desktop\jesters_bakery.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo scriptDir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\") - 1) >> CreateShortcut.vbs
echo oLink.TargetPath = scriptDir + "\jesters_bakery.exe" >> CreateShortcut.vbs
echo oLink.IconLocation = scriptDir + "\jesters_bakery.ico, 0" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
CreateShortcut.vbs
del CreateShortcut.vbs