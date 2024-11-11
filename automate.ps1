$pythonProgramPath = "C:\Program Files\Python312\python.exe"

echo $pythonProgramPath
echo $pythonScriptPath = "C:\Users\berend.wilkens\PycharmProjects\canvas_dashboard\generate_results.py"
echo $pythonScriptPath
echo $pythonOutput = & $pythonProgramPath $pythonScriptPath
echo $pythonOutput
Start-Sleep -Seconds 10
$pythonScriptPath = "C:\Users\berend.wilkens\PycharmProjects\canvas_dashboard\generate_dashboard.py"
echo $pythonScriptPath
$pythonOutput = & $pythonProgramPath $pythonScriptPath
echo $pythonOutput

echo $pythonScriptPath = "C:\Users\berend.wilkens\PycharmProjects\canvas_dashboard\generate_plotly.py"
echo $pythonScriptPath
echo $pythonOutput = & $pythonProgramPath $pythonScriptPath
echo $pythonOutput

echo $pythonScriptPath = "C:\Users\berend.wilkens\PycharmProjects\canvas_dashboard\generate_portfolio.py"
echo $pythonScriptPath
echo $pythonOutput = & $pythonProgramPath $pythonScriptPath
echo $pythonOutput

Start-Sleep -Seconds 10
