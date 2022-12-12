To create the image:
`docker image build -t deploy_hm:scratch .`

To run the container:
`docker run --rm -v "$(pwd)"/outputs:/app/outputs -it deploy_hm:scratch 2021 04`