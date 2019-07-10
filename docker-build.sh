#!/bin/bash
# Builds docker image for GDC within the repo using the commit as the tag

# Overwriting .deps dir
pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}

docker_build () {
    command docker build \
        --build-arg http_proxy=$http_proxy \
        --build-arg https_proxy=$https_proxy \
        --build-arg no_proxy=$no_proxy \
        --rm \
        "$@"
}

# tag
quay="quay.io/ncigdc/gdc-sanger-somatic-tool"
version=$(git log --first-parent --max-count=1 --format=format:%H)
imagetag="${quay}:${version}"

echo "Building tag: $imagetag"
docker_build -t $imagetag .
