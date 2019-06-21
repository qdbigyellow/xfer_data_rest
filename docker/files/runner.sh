#! /bin/sh

: ${REPO:="git@github.com:qdbigyellow/xfer_data_rest.git"}
: ${CI_BRANCH:="master"}
export CI_BRANCH
# We want to run on the branch "release" (not "master"), because then we deploy code that has been tested.

export REST_USER="rest_user"
# REST_PASSWD set via Docker run/compose

echo "Installing SSH Certificate"
mkdir -p -m 700 ${HOME}/.ssh
cp -a /secrets/ssh/config ${HOME}/.ssh
cp -a /secrets/ssh/id_rsa ${HOME}/.ssh

git clone "${REPO}"
git checkout "${CI_BRANCH}"

# Existing Python path
export PYTHONPATH=$(python3 -m site | grep /usr/lib | sed -e "s/,//" -e "s/[' ]//g" | tr '\n' ':')
# Our additions
export PYTHONPATH="${PYTHONPATH}:$(pwd)/build/site-packages/linux:$(pwd)/build/lib:$(pwd)/build"

while true; do
  # Fetch latest check out script
  git pull

  # run scheduled 
  python3 "$@" --check-git
done

#eof
