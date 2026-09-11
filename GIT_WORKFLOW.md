# Workflow Git — Travail en duo

L'objectif : un historique de commits propre et régulier, sans écraser le travail
de l'autre. Voici la méthode la plus simple et la plus sûre pour un projet de 30h.

## 1. Mise en place initiale (une seule fois)

**Personne A** (celle qui a le dépôt GitHub) :
```bash
git init
git add .
git commit -m "chore: initialisation de l'architecture du projet"
git branch -M main
git remote add origin <url_de_votre_repo_github>
git push -u origin main
```

**Personne B** :
```bash
git clone <url_de_votre_repo_github>
cd smart-fridge-nutrition-coach
```

## 2. Branche par fonctionnalité

Ne jamais coder directement sur `main`. Pour chaque tâche/séquence, on crée une branche :

```bash
git checkout main
git pull origin main
git checkout -b feature/moteur-metabolique
```

Convention de nommage : `feature/nom-court`, `fix/nom-du-bug`.

## 3. Committer régulièrement

Des petits commits fréquents et clairs, pas un seul gros commit à la fin.

```bash
git add app/services/nutrition_engine.py
git commit -m "feat: implémente le calcul du BMR (Mifflin-St Jeor)"
```

Convention de messages (recommandée) :
- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `refactor:` réorganisation sans changement de comportement
- `docs:` documentation
- `test:` ajout/modif de tests

## 4. Pousser sa branche et ouvrir une Pull Request

```bash
git push -u origin feature/moteur-metabolique
```

Puis sur GitHub : ouvrir une **Pull Request** vers `main`, et demander à votre
binôme de la relire avant de merger. Ça évite les conflits silencieux et ça
laisse une trace claire de qui a fait quoi.

## 5. Récupérer le travail de l'autre

Avant de commencer une nouvelle branche, toujours se resynchroniser :

```bash
git checkout main
git pull origin main
```

## 6. En cas de conflit

1. `git status` pour voir les fichiers en conflit.
2. Ouvrir les fichiers, chercher les marqueurs `<<<<<<<`, `=======`, `>>>>>>>`.
3. Choisir/fusionner le bon code, supprimer les marqueurs.
4. `git add <fichier>` puis `git commit`.

## Répartition suggérée (exemple)

| Séquence | Suggestion |
|---|---|
| 1. Moteur métabolique | Personne A |
| 2. Pipeline async (TheMealDB + USDA) | Personne B (la plus technique, à faire à deux idéalement) |
| 3. Auth JWT | Personne A |
| 4. UI Tailwind/Jinja2 + résilience | Personne B |

Même en vous répartissant les séquences, relisez le code de l'autre via les
Pull Requests : c'est ça qui compte pour la note et pour que chacun comprenne
l'ensemble du projet.
