# Clubes Project

## Configuración del Entorno Virtual

### Requisitos Previos
- Python 3.12.9 o superior
- pip (incluido con Python)

### Pasos para Activar el Entorno Virtual

1. **Activar el entorno virtual**:
   - En Windows Command Prompt (cmd):
     ```
     clubes_env\Scripts\activate.bat
     ```
   - En Windows PowerShell:
     ```
     .\clubes_env\Scripts\Activate.ps1
     ```

2. **Verificar la activación**:
   ```
   python -V
   pip -V
   ```
   Deberías ver que Python y pip están siendo ejecutados desde el directorio del entorno virtual.

3. **Instalar dependencias** (cuando existan):
   ```
   pip install -r requirements.txt
   ```

4. **Desactivar el entorno virtual**:
   ```
   deactivate
   ```

### Notas Importantes
- Siempre activa el entorno virtual antes de trabajar en el proyecto
- Cuando instales nuevas dependencias, actualiza requirements.txt:
  ```
  pip freeze > requirements.txt
