(Get-Item `
(Get-ItemProperty `
'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe').`
'(Default)').`
VersionInfo.`
ProductVersion
