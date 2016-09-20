[Files]
Source: C:\Documents and Settings\Anonymous User\Desktop\veoh\dist\veoh_downloader_gui.exe; DestDir: {app}; Flags: 32bit
Source: C:\Documents and Settings\Anonymous User\Desktop\veoh\dist\w9xpopen.exe; DestDir: {app}; OnlyBelowVersion: 4.90.3000,0
Source: C:\Documents and Settings\Anonymous User\Desktop\veoh\dist\MSVCR71.dll; DestDir: {sys}; Flags: onlyifdoesntexist
[Registry]
Root: HKCR; SubKey: veoh; ValueType: string; ValueName: ; ValueData: URL:veoh Protocol
Root: HKCR; SubKey: veoh; ValueType: string; ValueName: URL Protocol; ValueData: 
Root: HKCR; SubKey: veoh\shell\open\command; ValueType: string; ValueData: "\""{app}\veohdownloader.exe\"" \""%1\"""
[UninstallDelete]
Name: {app}\veoh_downloader_gui.exe; Type: filesandordirs
Name: {app}\w9xpopen.exe; Type: filesandordirs
[Setup]
AppCopyright=2009 David Konsumer
AppName=Veoh Downloader
AppVerName=1.13
DefaultDirName={pf}\Veoh Downloader
