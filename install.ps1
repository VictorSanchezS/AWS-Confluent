# Scripts de inicio rápido

# Instalar dependencias
Write-Host "📦 Instalando dependencias de Python..." -ForegroundColor Green
pip install -r requirements.txt

# Verificar instalación
Write-Host "`n✅ Verificando instalación..." -ForegroundColor Green
python -c "import kafka, boto3, dotenv; print('Todas las dependencias instaladas correctamente')"

Write-Host "`n🎉 ¡Instalación completada!" -ForegroundColor Green
Write-Host "💡 Próximos pasos:" -ForegroundColor Yellow
Write-Host "   1. Copia config/.env.example a config/.env"
Write-Host "   2. Completa las credenciales en config/.env"
Write-Host "   3. Ejecuta: python producers/basic_producer.py"
Write-Host "   4. En otra terminal: python consumers/integrated_consumer.py"
