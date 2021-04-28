mkdir tmp
cp ./*.sh ./tmp
cp ./*.py ./tmp
sudo docker build -t nlutils:ai-server
rm -rf tmp