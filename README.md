# vk_viewer
 This app provides additional features to VK's interface (e.g. sorting by date, likes, reposts, etc.) 
 
 # Building and running docker container
 docker image build -t docker_vk_viewer .
 docker run --name docker_vk_viewer_container -p 5000:5000 docker_vk_viewer
