cd criticlist
./download.sh
python process.py > ../todownload.txt
cd ../criticdownloads
./download.sh
