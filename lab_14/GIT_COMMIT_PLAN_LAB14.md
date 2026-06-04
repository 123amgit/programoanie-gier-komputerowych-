# Proponowane commity dla Lab 14

Wymaganie laboratorium mówi o refaktoryzacji z commitami per kategorię. Po wypakowaniu ZIP-a do repozytorium wykonaj najlepiej takie commity:

```bash
git add lab14/scenes/boss.tscn lab14/scripts/boss.gd lab14/main.tscn lab14/scripts/main_scene.gd
git commit -m "Lab14: add boss FSM and two hitboxes"

git add lab14/scenes/explosion.tscn lab14/scripts/explosion.gd
git commit -m "Refactor category: signals and particle death effect"

git add lab14/scripts/boss.gd
git commit -m "Refactor category: replace magic numbers with constants and exports"

git add lab14/scripts/boss.gd lab14/scripts/main_scene.gd
git commit -m "Refactor category: split long boss methods into state helpers"

git add lab14/README_LAB14.md lab14/PEER_REVIEW_ISSUE_TEMPLATE.md lab14/GIT_COMMIT_PLAN_LAB14.md
git commit -m "Add lab14 documentation and peer review template"
```

Jeżeli repozytorium ma już foldery `lab09`-`lab13`, po prostu dodaj folder `lab14` obok nich.
