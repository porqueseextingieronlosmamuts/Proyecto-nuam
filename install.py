#!/usr/bin/env python
"""
Script de instalación rápida para el proyecto NUAM
Ejecutar: python install.py
"""

import subprocess
import sys
import os

def install_dependencies():
    """Instala todas las dependencias del proyecto"""
    
    print("=" * 80)
    print("🚀 INSTALACIÓN DE DEPENDENCIAS - PROYECTO NUAM")
    print("=" * 80)
    print()
    
    # Verificar que pip esté disponible
    try:
        import pip
    except ImportError:
        print("❌ ERROR: pip no está instalado")
        print("Por favor, instala pip primero")
        sys.exit(1)
    
    # Leer requirements.txt
    if not os.path.exists('requirements.txt'):
        print("❌ ERROR: No se encontró requirements.txt")
        sys.exit(1)
    
    print("📦 Instalando dependencias desde requirements.txt...")
    print()
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt"
        ])
        
        print()
        print("=" * 80)
        print("✅ ¡INSTALACIÓN COMPLETADA!")
        print("=" * 80)
        print()
        print("📋 PRÓXIMOS PASOS:")
        print()
        print("1. Configurar archivo .env:")
        print("   copy .env.example .env")
        print()
        print("2. Ejecutar migraciones:")
        print("   python manage.py migrate")
        print("   python manage.py migrate cuentas")
        print()
        print("3. Crear superuser (opcional):")
        print("   python manage.py createsuperuser")
        print()
        print("4. Iniciar servidor:")
        print("   python manage.py runserver")
        print()
        print("5. Abrir navegador:")
        print("   http://localhost:8000")
        print()
        print("=" * 80)
        
    except subprocess.CalledProcessError as e:
        print()
        print("❌ ERROR durante la instalación:")
        print(str(e))
        sys.exit(1)

def verify_installation():
    """Verifica que las dependencias críticas estén instaladas"""
    
    print()
    print("🔍 Verificando instalación...")
    print()
    
    critical_packages = {
        'django': 'Django Framework',
        'pyotp': 'OTP Generation (MFA)',
        'qrcode': 'QR Code Generation (MFA)',
        'PIL': 'Pillow (Image Processing)',
        'openpyxl': 'Excel File Handling',
        'dotenv': 'Environment Variables',
    }
    
    all_ok = True
    
    for package, description in critical_packages.items():
        try:
            __import__(package)
            print(f"✅ {description:40} - OK")
        except ImportError:
            print(f"❌ {description:40} - MISSING")
            all_ok = False
    
    print()
    
    if all_ok:
        print("✅ Todas las dependencias críticas están instaladas")
    else:
        print("⚠️  Algunas dependencias falta instalar")
        print("Ejecuta: pip install -r requirements.txt")
    
    print()

if __name__ == "__main__":
    install_dependencies()
    verify_installation()
