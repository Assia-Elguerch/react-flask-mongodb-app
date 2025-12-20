from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
import os
import hvac
import sys

app = Flask(__name__)

# CONFIGURATION VAULT
VAULT_ADDR = os.environ.get('VAULT_ADDR', 'http://vault:8200')
VAULT_TOKEN = os.environ.get('VAULT_TOKEN', 'myroot')

print("Initialisation de la connexion à Vault...")
print(f"  Vault URL: {VAULT_ADDR}")


def get_secret_from_vault(path):

    try:
        # Créer un client Vault
        client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
        
        # Vérifier l'authentification
        if not client.is_authenticated():
            print("Erreur: Impossible de s'authentifier à Vault")
            return None
        
        print(f"Authentification Vault réussie")
        
        # Récupérer le secret (KV v2)
        secret = client.secrets.kv.v2.read_secret_version(path=path)
        
        if secret and 'data' in secret and 'data' in secret['data']:
            print(f"Secret '{path}' récupéré depuis Vault")
            return secret['data']['data']
        else:
            print(f" Secret '{path}' non trouvé dans Vault")
            return None
            
    except Exception as e:
        print(f" Erreur lors de la récupération du secret depuis Vault: {e}")
        return None



# RÉCUPÉRATION DES SECRETS MONGODB

print("\n Récupération des credentials MongoDB depuis Vault...")

mongodb_secrets = get_secret_from_vault('mongodb')

if mongodb_secrets:
    print(" Secrets MongoDB récupérés depuis Vault avec succès!")
    
    mongodb_host = mongodb_secrets.get('host', 'localhost')
    mongodb_username = mongodb_secrets.get('username', '')
    mongodb_password = mongodb_secrets.get('password', '')
    mongodb_database = mongodb_secrets.get('database', 'flaskdb')
    USING_VAULT = True
    
else:
    print(" Impossible de récupérer les secrets depuis Vault")
    print("   Utilisation des variables d'environnement par défaut...")
    
    mongodb_host = os.environ.get('MONGODB_HOST', 'localhost')
    mongodb_username = os.environ.get('MONGODB_USERNAME', '')
    mongodb_password = os.environ.get('MONGODB_PASSWORD', '')
    mongodb_database = os.environ.get('MONGODB_DATABASE', 'flaskdb')
    
    
    # Indicateur que Vault n'est pas utilisé
    USING_VAULT = False



# CONFIGURATION MONGODB

try:
    app.config['MONGO_URI'] = f'mongodb://{mongodb_username}:{mongodb_password}@{mongodb_host}:27017/{mongodb_database}?authSource=admin'
    mongo = PyMongo(app)
    print("Configuration MongoDB terminée\n")
except Exception as e:
    print(f" Erreur lors de la configuration MongoDB: {e}")
    sys.exit(1)

# Configuration CORS
CORS(app)


# ROUTES API


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint de santé pour vérifier le statut de l'application
    """
    try:
        # Tester la connexion MongoDB
        mongo.db.command('ping')
        db_status = " Connected"
    except Exception as e:
        db_status = f" Error: {str(e)}"
    
    return jsonify({
        'status': 'healthy',
        'vault': ' Connected' if USING_VAULT else '  Not using Vault',
        'database': db_status,
        'mongodb_host': mongodb_host,
        'mongodb_database': mongodb_database,
        'security': 'Token-based with Vault' if USING_VAULT else 'Environment variables'
    })


@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    """
    Récupère toutes les tâches
    """
    try:
        tasks = mongo.db.tasks
        result = []

        for field in tasks.find():
            result.append({
                '_id': str(field['_id']), 
                'title': field['title']
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/task', methods=['POST'])
def add_task():
    """
    Ajoute une nouvelle tâche
    """
    try:
        tasks = mongo.db.tasks 
        title = request.get_json()['title']

        # Utiliser insert_one au lieu de insert (déprecié)
        task_id = tasks.insert_one({'title': title}).inserted_id
        new_task = tasks.find_one({'_id': task_id})

        result = {'title': new_task['title']}

        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/task/<id>', methods=['PUT'])
def update_task(id):
    """
    Modifie une tâche existante
    """
    try:
        tasks = mongo.db.tasks 
        title = request.get_json()['title']

        tasks.find_one_and_update(
            {'_id': ObjectId(id)}, 
            {"$set": {"title": title}}, 
            upsert=False
        )
        new_task = tasks.find_one({'_id': ObjectId(id)})

        if new_task:
            result = {'title': new_task['title']}
            return jsonify({"result": result})
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/task/<id>', methods=['DELETE'])
def delete_task(id):
    """
    Supprime une tâche
    """
    try:
        tasks = mongo.db.tasks 
        response = tasks.delete_one({'_id': ObjectId(id)})

        if response.deleted_count == 1:
            result = {'message': 'record deleted'}
        else: 
            result = {'message': 'no record found'}
        
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# POINT D'ENTRÉE
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Flask API démarrée avec succès!")
    print(f"   Vault: {' Enabled' if USING_VAULT else ' Disabled'}")
    print(f"   MongoDB: {mongodb_host}:{mongodb_database}")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0')