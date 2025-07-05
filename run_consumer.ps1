# Scripts para ejecutar el consumer integrado

# Consumer integrado - Consume mensajes y los envía a AWS
Write-Host "🚀 Ejecutando Consumer Integrado con AWS..." -ForegroundColor Green
Write-Host "Este script consumirá mensajes de Confluent Cloud y los enviará a AWS" -ForegroundColor Yellow
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Cyan
python consumers/integrated_consumer.py
