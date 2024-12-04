$pythonProgramPath = cmd /c "where python" '2>&1'
echo $pythonProgramPath
$pythonScriptPath = "C:\Users\berend.wilkens\PycharmProjects\canvas_dashboard\test.py"
$pythonOutput = & $pythonProgramPath $pythonScriptPath
echo $pythonOutput
Get-Date; Start-Sleep -Seconds 5; Get-Date
