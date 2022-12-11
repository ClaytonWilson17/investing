docker image build -t investing .
docker run --rm -it -v $(pwd):/usr/app/src investing