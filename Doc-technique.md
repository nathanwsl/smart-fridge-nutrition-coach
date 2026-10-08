# 📖 Documentation Technique

Si vous voulez fouiller dans le moteur du projet et comprendre comment tout s'articule, voici une vue d'ensemble de notre architecture et de notre logique métier.

## 1. Organisation du Code (Backend)

Nous avons opté pour une structure modulaire classique avec FastAPI, pour bien séparer les responsabilités :

* backend/app/main.py : Le point d'entrée de l'application. C'est ici qu'on initialise FastAPI et qu'on sert notre fichier HTML statique.
* backend/app/routers/ : Nos "contrôleurs". On y a découpé nos routes de l'API par domaine (auth, fridge, profile, recipes).
* backend/app/schemas/ : Nos modèles Pydantic. Ils sont cruciaux pour valider et nettoyer les données qui entrent et qui sortent de notre API.
* backend/app/security/ : La mécanique des tokens JWT et le hachage des mots de passe.
* backend/app/services/ : Les "cerveaux" de l'app. C'est ici que se trouve toute la logique métier complexe (calculs métaboliques, appels asynchrones aux APIs, traduction des ingrédients).
* backend/app/static/ : Notre frontend (index.html), servi directement par le backend.

## 2. Base de Données (Supabase)

L'application tourne avec deux tables très simples sur Supabase :

* Table "users" : Gère l'authentification. Elle contient un "username" (Clé primaire, unique) et un "hashed_password".
* Table "fridge_items" : Gère l'inventaire des utilisateurs. Elle contient un "id", le nom de l'ingrédient, et une clé étrangère "username" pour lier l'ingrédient à son propriétaire.

## 3. Le Pipeline Nutritionnel (Le cœur du réacteur)

Le fichier le plus important du projet est "services/nutrition_pipeline.py". Voici ce qu'il se passe exactement quand un utilisateur demande des suggestions de recettes :

1. Extraction : On récupère d'abord tous les ingrédients présents dans le frigo de l'utilisateur.
2. Recherche de recettes : On lance des requêtes simultanées à TheMealDB (via filter.php) pour chaque ingrédient.
3. Dédoublonnage : On regroupe les résultats et on élimine les recettes en double.
4. Normalisation des données : Pour les recettes retenues, on utilise un modèle Pydantic très pratique ("RawMealDBRecipe") qui transforme les 20 clés d'ingrédients mal formatées de TheMealDB en une belle liste Python propre. On passe ensuite ces ingrédients dans notre traducteur UK vers US.
5. Enrichissement nutritionnel asynchrone : On lance un "asyncio.gather()" pour interroger l'USDA sur *tous* les ingrédients de la recette en même temps.
6. Agrégation : On fait la somme finale (Kcal, Protéines, Glucides, Lipides) et on renvoie le tout au Frontend.

À noter : Nous avons mis en place un système de tolérance aux pannes. Si l'API de l'USDA ne répond pas assez vite ou ne connait pas un ingrédient, l'application ne plante pas. L'ingrédient est simplement classé dans une liste "d'ingrédients non reconnus" affichée à l'utilisateur.

## 4. Sécurité

L'API ne stocke absolument aucun mot de passe en clair. À l'inscription, le mot de passe est haché via "bcrypt" (librairie passlib).
Lorsqu'un utilisateur se connecte, nous générons un JSON Web Token (JWT) signé avec la clé secrète du serveur. 
Toutes les routes sensibles (comme l'ajout d'ingrédients ou la génération de suggestions) sont protégées par le middleware "get_current_user", qui vérifie systématiquement la validité et la date d'expiration de ce token.
