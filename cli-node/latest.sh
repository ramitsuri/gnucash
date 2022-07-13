project=$(pwd)
cd /home/pi/Downloads/expenses || exit
git pull
flatpak run --command=gnucash-cli org.gnucash.GnuCash --report run --name="Annual-2022" --output-file=$project/public/annual.html /home/pi/Downloads/expenses/v1.0.gnucash
flatpak run --command=gnucash-cli org.gnucash.GnuCash --report run --name="Monthly-2022" --output-file=$project/public/monthly.html /home/pi/Downloads/expenses/v1.0.gnucash