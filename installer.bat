pip install -r requirements.txt
pip install pyinstaller

pyinstaller __main__.py --onefile --icon=valheim_sync.ico --name=valheim-sync --add-data valheim_sync.ico:. --add-data .env:.

move %cd%\dist\valheim-sync.exe %cd%\
rmdir %cd%\dist

:: copied from https://superuser.com/questions/392061/how-to-make-a-shortcut-from-cmd
@echo off
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%HOMEDRIVE%%HOMEPATH%\Desktop\valheim-sync.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo scriptDir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\") - 1) >> CreateShortcut.vbs
echo oLink.TargetPath = scriptDir + "\valheim-sync.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = scriptDir >> CreateShortcut.vbs
echo oLink.IconLocation = scriptDir + "\valheim_sync.ico, 0" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
CreateShortcut.vbs
del CreateShortcut.vbs
