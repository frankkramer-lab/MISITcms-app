#!/usr/bin/env bash

echo "Starting CMS services..."
cd /root/cms

#PGPASSWORD=$POSTGRES_PASSWORD psql -d $POSTGRES_DB -h cms-db -U $POSTGRES_USER -c "SELECT EXIST (SELECT COUNT(name) FROM admins);"
if [ ! -f "init.lock" ]; then
   echo "DB needs initialization..."
   python3 scripts/cmsInitDB
   # Create/Update admin account
   python3 cmscontrib/AddAdmin.py $(python3 scripts/getconf.py admin_user) -p  $(python3 scripts/getconf.py admin_password)
   touch "init.lock"
else
   echo "DB was already initialized..."
fi

# Start Logging Service
python3 scripts/cmsLogService 0   | tee -a /var/log/cms/logservice &
python3 scripts/cmsAdminWebServer | tee -a /var/log/cms/adminserver &

sleep 4

# Install all course packages for all courses
find /root/cms-data/ -type f -name '.itime*' -delete
python3 cmscontrib/ImportUser.py --all -L italy_yaml /root/cms-data/
contest_out=$(python3 cmscontrib/ImportContest.py -i -u -U -L italy_yaml /root/cms-data/)
contest_id=($(echo $contest_out | sed -nr 's/.*\(new contest id: ([0-9]+)\)\.$/\1/p'))
pip3 install -r /root/cms-data/requirements.txt

python3 scripts/cmsContestWebServer -c $contest_id  | tee -a /var/log/cms/contestserver &
python3 scripts/cmsScoringService -c $contest_id    | tee -a /var/log/cms/scoringservice &
python3 scripts/cmsEvaluationService -c $contest_id | tee -a /var/log/cms/evaluationservice &
# worker=$(python3 scripts/getconf.py admin_user)
worker=3
for i in $(seq 1 $worker); do
  python3 scripts/cmsWorker $i | tee -a /var/log/cms/worker$i &
done

wait
