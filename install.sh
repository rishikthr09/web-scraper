rm -f ./scraper.cron
touch ./scraper.cron

echo '# run script every 5 minutes' >> ./scraper.cron
echo '*/10 * * * *   '$USER'  python '$PWD'/scraper.py' >> ./scraper.cron
echo '# run script after system (re)boot' >> ./scraper.cron
echo '@reboot       '$USER'  python '$PWD'/scraper.py' >> ./scraper.cron

sudo mv ./scraper.cron /etc/cron.d/scraper.cron
