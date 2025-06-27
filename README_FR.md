# AIMD - Générateur de README par Intelligence Artificielle

**AIMD** est un puissant outil en ligne de commande qui génère automatiquement des fichiers README.md professionnels pour vos projets en utilisant l’IA Gemini de Google. Il suffit d’indiquer le dossier de votre projet et la documentation complète est créée en quelques secondes !

## 🚀 Installation rapide

### Prérequis

- Python 3.6 ou supérieur
- Clé API Google AI Studio ([Obtenez-la ici](https://aistudio.google.com/app/apikey))
- Connexion Internet

### Windows
```cmd
git clone https://github.com/babe051/aimd.git
cd aimd
# Exécuter en tant qu’administrateur
setup-windows.bat
```

### Linux/macOS
```bash
git clone https://github.com/babe051/aimd.git
cd aimd
chmod +x setup-unix.sh
sudo ./setup-unix.sh
```

## 📖 Utilisation

Après installation, utilisez `aimd` depuis n’importe quel dossier :

```bash
# Générer un README pour le dossier courant
aimd .

# Générer un README pour un projet spécifique
aimd /chemin/vers/projet

# Exemple sous Windows
aimd C:\Users\username\projects\myapp

# Ignorer certains fichiers/dossiers
aimd . -i node_modules "*.log" temp/

# Nom de fichier personnalisé et limite de fichiers
aimd . --output DOCUMENTATION.md --max-files 100

# Plusieurs motifs d’exclusion
aimd . -i "*.pyc" "__pycache__/" ".env*" "logs/"

# Générer la documentation en arabe
aimd . --ar

# Générer la documentation en français
aimd . --fr
```


## 🛠️ Options de commande

| Option         | Description                                      | Exemple                   |
|----------------|--------------------------------------------------|---------------------------|
| `path`         | Dossier du projet à analyser                     | `aimd /projects/webapp`   |
| `--output`     | Nom du fichier de sortie (par défaut: README.md) | `--output DOCS.md`        |
| `--max-files`  | Nombre maximal de fichiers à traiter (50 par défaut) | `--max-files 100`     |
| `-i, --ignore` | Fichiers/dossiers supplémentaires à ignorer      | `-i logs/ "*.tmp"`        |
| `--ar`         | Générer la documentation en arabe                | `--ar`                    |
| `--fr`         | Générer la documentation en français             | `--fr`                    |

---

## ⚙️ Fonctionnalités

- 🤖 **Propulsé par l’IA** : Utilise Gemini de Google pour une documentation intelligente
- 📂 **Analyse intelligente** : Détecte automatiquement la structure du projet et la stack technique
- 🚫 **Filtrage intelligent** : Respecte le `.gitignore` et les motifs d’exclusion personnalisés
- 🎯 **Multi-plateforme** : Fonctionne sous Windows, Linux et macOS
- ⚡ **Traitement rapide** : Barres de progression et gestion efficace des fichiers
- 🎨 **Sortie professionnelle** : Markdown prêt pour GitHub avec emojis et structure claire

## 📁 Ce qui est analysé

AIMD analyse intelligemment votre projet :

✅ **Inclus :**
- Fichiers source (`.py`, `.js`, `.html`, `.css`, etc.)
- Fichiers de configuration (`package.json`, `requirements.txt`, etc.)
- Fichiers de documentation
- Structure du projet et dépendances

❌ **Ignoré automatiquement :**
- Dossier `.git/`
- Dossier `node_modules/`
- Dossier `__pycache__/`
- Fichiers binaires et images
- Fichiers volumineux (>5 Mo)
- Fichiers correspondant au `.gitignore`

## 📊 Exemple de sortie

```bash
$ aimd .
🚀 Démarrage de AIMD - Générateur de README par IA
📂 Chemin cible : /home/user/monprojet
📄 Fichier de sortie : /home/user/monprojet/README.md (dans le dossier cible)
--------------------------------------------------
🔍 Analyse de : /home/user/monprojet...
📄 Le README sera enregistré dans : /home/user/monprojet/README.md
📂 Traitement des fichiers |████████████| 25/50 [00:02<00:01]
🎉 README généré avec succès !
✅ README.md généré avec succès à /home/user/monprojet/README.md
--------------------------------------------------
🎉 Terminé ! Votre README.md a été généré avec succès.
📁 Emplacement : /home/user/monprojet/README.md
```

## 🗂️ Structure des fichiers d’installation

### Windows
```
C:\Windows\System32\aimd\
├── aimd.py          # Script principal
├── generator.py     # Logique de génération
├── utils.py         # Utilitaires
└── aimd.bat         # Script de commande local

C:\Windows\System32\
└── aimd.bat         # Commande globale (appelle le script local)
```

### Linux/macOS
```
/usr/local/lib/aimd/
├── aimd.py          # Script principal
├── generator.py     # Logique de génération
└── utils.py         # Utilitaires

/usr/local/bin/
└── aimd             # Script de commande global
```

## 🗑️ Désinstallation

### Windows
```cmd
# Exécuter en tant qu’administrateur
uninstall-windows.bat
```

### Linux/macOS
```bash
sudo ./uninstall-unix.sh
```

### Désinstallation manuelle
**Windows :**
```cmd
del "C:\Windows\System32\aimd.bat"
rmdir /s "C:\Windows\System32\aimd"
```

**Linux/macOS :**
```bash
sudo rm /usr/local/bin/aimd
sudo rm -rf /usr/local/lib/aimd
```

## 🔧 Dépannage

### Problèmes courants

**"Permission denied" lors de l’installation**
- **Windows** : Exécutez l’installation en tant qu’administrateur
- **Linux/Mac** : Utilisez `sudo ./setup-unix.sh`

**"Command not found: aimd"**
- Vérifiez que le script d’installation s’est terminé correctement
- Essayez d’ouvrir un nouveau terminal
- Vérifiez la présence des fichiers dans les dossiers d’installation

**"No readable files found"**
- Assurez-vous que le dossier cible contient du code source
- Vérifiez que vos motifs d’exclusion ne sont pas trop restrictifs
- Essayez d’augmenter la limite `--max-files`

**"Failed to connect to Google AI Studio"**
- Vérifiez votre connexion Internet
- Vérifiez que votre clé API est valide et active
- Assurez-vous que la clé API dispose des autorisations nécessaires

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le dépôt
2. Créez une branche de fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Commitez vos modifications (`git commit -m 'Add amazing feature'`)
4. Poussez la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT – voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🛡️ Sécurité

- **Sécurité des clés API** : Ne jamais inclure de clés API dans le code source
- **Variables d’environnement** : Utilisez des variables d’environnement pour les données sensibles
- **Permissions des fichiers** : Les scripts d’installation gèrent correctement les permissions
- **Installation sécurisée** : Les fichiers sont placés dans les dossiers système standards

## 🔄 Historique des versions

- **v1.0.0** : Première version avec support multi-plateforme
- Génération de README entièrement par IA
- Filtrage intelligent des fichiers et support du gitignore
- Barres de progression et retour visuel animé
- Installation de la commande globale

---
## 👥 Contributeurs

- [<img src="https://github.com/babe051.png" width="32" height="32" style="border-radius:50%"/>](https://github.com/babe051)  
  **Mohamed Val** – [@babe051](https://github.com/babe051)

- [<img src="https://github.com/Zeini-23025.png" width="32" height="32" style="border-radius:50%"/>](https://github.com/Zeini-23025)  
  **Zeini Cheikh** – [@Zeini-23025](https://github.com/Zeini-23025)

**Fait avec ❤️ pour les développeurs qui aiment la bonne documentation ! 🚀📝**