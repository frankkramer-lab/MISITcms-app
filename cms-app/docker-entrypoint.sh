#!/usr/bin/env bash

echo "Starting CMS services..."
cd /root/cms

# Database & Admin account initialization
# Check whether the table 'admins' exists to detect empty db
PGPASSWORD=$POSTGRES_PASSWORD psql -d $POSTGRES_DB -h cms-db -U $POSTGRES_USER -c "SELECT count(table_name) from information_schema.tables where table_name = 'admins'" | grep 0 >> /dev/null 2>&1
if [ $? -eq 0 ]; then
   echo "DB needs initialization..."
   python3 scripts/cmsInitDB 2>&1 | tee -a /var/log/cms/initdb
   # Create/Update admin account
   python3 cmscontrib/AddAdmin.py $(jq -r '.["admin_user"]' ./config/cms.conf ) -p  $(jq -r '.["admin_password"]' ./config/cms.conf ) 2>&1 | tee -a /var/log/cms/addadmin
else
   echo "DB was already initialized..."
fi

# Start Admin & Logging Service
python3 scripts/cmsLogService 0 2>&1 | tee -a /var/log/cms/logservice &
python3 scripts/cmsAdminWebServer 2>&1 | tee -a /var/log/cms/adminserver &
sleep 4

# Import all required contest data
find /root/cms-data/ -type f -name '.itime*' -delete
python3 cmscontrib/ImportUser.py --all -L italy_yaml /root/cms-data/ 2>&1 | tee -a /var/log/cms/userimport
contest_out=$(python3 cmscontrib/ImportContest.py -i -u -U -L italy_yaml /root/cms-data/)
contest_id=($(echo $contest_out | sed -nr 's/.*\(new contest id: ([0-9]+)\)\.$/\1/p'))

# Install python packages which are needed for the assignments
if [ -f "/root/cms-data/requirements.txt" ]; then
  echo "Python package requirements for assignments found. Installing..."
  python3.8 -m pip install -r /root/cms-data/requirements.txt --target=/usr/local/lib/python3.8/dist-packages/
else
  echo "No Python package requirements found for assignments."
fi

# Run Contest, Scoring & Evaluation Services to setup grading environment
python3 scripts/cmsContestWebServer -c $contest_id 2>&1 | tee -a /var/log/cms/contestserver &
python3 scripts/cmsScoringService -c $contest_id 2>&1 | tee -a /var/log/cms/scoringservice &
python3 scripts/cmsEvaluationService -c $contest_id 2>&1 | tee -a /var/log/cms/evaluationservice &

# Initialize worker nodes (number of workers are obtained from cms-config/cms.conf)
worker=$(jq -r '.["number_of_workers"]' ./config/cms.conf )
for i in $(seq 1 $worker); do
  python3 scripts/cmsWorker $i 2>&1 | tee -a /var/log/cms/worker$i &
done

wait
