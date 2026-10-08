# 🥦 Smart Fridge & Nutrition Coach

Bienvenue sur **Smart Fridge & Nutrition Coach**, une application web conçue pour transformer la gestion de votre frigo en un véritable assistant nutritionnel. 

L'objectif de ce projet est d'aller au-delà de la simple suggestion de recettes : l'application calcule les véritables valeurs nutritionnelles de vos plats en croisant les données de plusieurs APIs en temps réel de manière asynchrone.

## ✨ Fonctionnalités Principales

* Profil & Besoins Métaboliques : Calcul automatique de votre métabolisme de base (BMR) et de votre dépense énergétique (TDEE) selon la formule de Mifflin-St Jeor.
* Frigo Virtuel : Une interface fluide pour gérer votre inventaire d'ingrédients au quotidien.
* Générateur de Recettes : Suggestions de plats réalisables avec ce que vous avez sous la main, propulsées par TheMealDB.
* Analyse Nutritionnelle Avancée : L'application croise dynamiquement les ingrédients de chaque recette avec la base de données de l'USDA pour calculer vos macros exactes (Kcal, Protéines, Glucides, Lipides).
* Sécurité : Système de comptes sécurisé avec authentification par JWT et hachage des mots de passe.

## 🛠️ Stack Technique

Ce projet a été conçu pour être léger, rapide et axé sur les performances backend :
* Backend : Python 3.10+, FastAPI (pour sa gestion native de l'asynchrone), Pydantic
* Base de données : Supabase (PostgreSQL)
* Frontend : Vanilla HTML/CSS/JS (Interface type Single Page Application)
* APIs Tierces : TheMealDB, USDA FoodData Central

## 🚀 Installation & Lancement en local

Pour tester le projet sur votre machine, suivez ces étapes :

1. Cloner le projet :
    git clone <url-du-repo>
    cd smart-fridge-nutrition-coach

2. Préparer l'environnement virtuel :
    python -m venv venv
    source venv/bin/activate  (ou venv\Scripts\activate sur Windows)
    pip install -r backend/requirements.txt

3. Configurer les variables d'environnement :
    Le projet utilise des variables d'environnement pour gérer les accès sécurisés aux APIs et à la base de données.
    Renommez simplement le fichier ".env.example" fourni à la racine en ".env", et complétez-le avec vos propres clés.

4. Démarrer le serveur :
    cd backend
    uvicorn app.main:app --reload

🎉 L'application est maintenant accessible sur http://localhost:8000 !
