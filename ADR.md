# 🏗️ Nos choix d'architecture (ADR)

Vu qu'on avait qu'une trentaine d'heures pour boucler ce projet fil rouge, on a dû trancher dans le vif sur pas mal d'aspects techniques. Voici pourquoi on a fait ces choix.

## 1. Pourquoi FastAPI ? (L'enfer des requêtes)
Le plus gros défi du projet, c'était de calculer les macros d'une recette complète. Pour une recette de 10 ingrédients, il fallait faire 1 requête à TheMealDB + 10 requêtes à l'USDA. Si on faisait ça de manière classique (synchrone), le temps de chargement aurait été horrible. 
Notre solution : On a pris FastAPI avec la bibliothèque "httpx". Grâce à sa gestion native de l'asynchrone, on lance toutes les requêtes USDA en parallèle. Résultat : on a gagné un temps fou sur l'affichage des suggestions.

## 2. Supabase au lieu d'une BDD locale
On avait besoin d'une vraie base de données relationnelle (pour lier les utilisateurs à leur frigo), mais on ne voulait pas perdre des heures à configurer Docker ou un serveur PostgreSQL local, surtout pour bosser efficacement à deux. 
Notre solution : On est partis sur Supabase. C'est très rapide à brancher via leur client REST, et ça fait parfaitement le job. Par contre, on a géré la logique d'authentification (les JWT et le hashage des mots de passe) nous-mêmes côté backend pour bien maîtriser le flux et apprendre comment ça marche sous le capot.

## 3. Le dictionnaire de traduction "UK to US"
Celui-là, on ne l'avait pas vu venir. TheMealDB est britannique, donc il nous sortait des ingrédients comme "aubergine" ou "prawns". Sauf que l'USDA est américain, et lui ne comprend que "eggplant" et "shrimp". Ça bloquait la moitié de nos correspondances nutritionnelles.
Notre solution : On a créé un petit fichier de traduction qui intercepte et traduit les noms des ingrédients avant d'interroger l'USDA. Simple, un peu manuel, mais 100% efficace par rapport à l'intégration d'une API de traduction qui aurait inutilement ralenti l'application.

## 4. Le Frontend en Vanilla JS
Vu que le temps était compté, on a préféré se concentrer sur la vraie difficulté du projet : la complexité algorithmique du Backend (le pipeline de données et les requêtes asynchrones).
Notre solution : Pas de React, pas de Vue.js. On a fait une interface avec du JavaScript pur (Vanilla JS) et du CSS. Ajouter un framework front aurait alourdi le projet pour pas grand-chose. Le Vanilla fait très bien le boulot et donne un vrai effet d'application fluide sans aucun rechargement de page.
