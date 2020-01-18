#!/bin/sh
#https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git
git remote -v update

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    git pull --rebase
    docker cp requirements.txt app:/app
    docker exec -d app pip install -r requirements.txt
    docker restart app
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
    echo "Production use release branch. No push is allowed!"
else
    echo "Diverged"
fi


