$exclude = @(".venv", "template.zip", "dist", "__pycache__", ".git")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "template.zip" -Force
Write-Host "Gerado: $((Resolve-Path template.zip).Path)"
