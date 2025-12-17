# Variables d'Environnement

Ce fichier liste toutes les variables d'environnement nécessaires pour le projet.

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```bash
# ============================================
# Configuration de la Base de Données
# ============================================
POSTGRES_DB=bankdb
POSTGRES_USER=bankuser
POSTGRES_PASSWORD=changeme_secure_password

# ============================================
# Configuration Elasticsearch
# ============================================
ELASTIC_PASSWORD=changeme_elastic_password

# ============================================
# Configuration Kibana
# ============================================
KIBANA_SYSTEM_PASSWORD=changeme_kibana_system_password
KIBANA_ENCRYPTION_KEY=changeme_32_char_encryption_key_here
KIBANA_SECURITY_KEY=changeme_32_char_security_key_here
KIBANA_REPORTING_KEY=changeme_32_char_reporting_key_here

# ============================================
# Configuration Elastic APM
# ============================================
ELASTIC_APM_SERVER_URL=http://apm-server:8200
APM_SECRET_TOKEN=changeme_apm_secret_token
ELASTIC_APM_SERVICE_NAME=bank-flask-app

# ============================================
# Configuration Flask Application
# ============================================
FLASK_SECRET_KEY=changeme_flask_secret_key_min_32_chars
APP_ENV=dev
LOG_LEVEL=INFO
```

## Génération de Clés Sécurisées

Pour générer des clés sécurisées, vous pouvez utiliser :

```bash
# Générer une clé aléatoire de 32 caractères
openssl rand -hex 32

# Ou avec Python
python -c "import secrets; print(secrets.token_hex(32))"
```

## Important

⚠️ **Ne commitez jamais le fichier `.env` dans Git !** Il contient des informations sensibles.

