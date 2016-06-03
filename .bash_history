ls
docker images
docker rmi animation_maker_5
docker rmi -f animation_maker_5
docker ps
docker stop 5a011d415880
docker rmi -f $(docker images -q)
docker images
docker ps
docker kill
docker rm $(docker ps -a -q)
docker rm -f $(docker ps -a -q)
docker ps
ls
cd nexrad/
ls
cd input_files/
ls
sudo rm *
ls
cd ..
cd output_plots/
ls
sudo rm *
cd ..
cd animation_html/
ls
rm *
sudo rm *
cd ..
ls
rm animation_maker.pyc
ls
cd ..
ls
cd docker_images/
ls
ls animation_maker/
ls jupyter_dood/
ls plot_maker/
cd
cat /dev/null > ~/.bash_history
