#!/usr/bin/env bash

echo "Starting CMS services..."
cd /root/cms

# Database & Admin account initialization
if [ ! -f "init.lock" ]; then
   echo "DB needs initialization..."
   python3 scripts/cmsInitDB
   # Create/Update admin account
   python3 cmscontrib/AddAdmin.py $(python3 scripts/getconf.py admin_user) -p  $(python3 scripts/getconf.py admin_password)
   touch "init.lock"
else
   echo "DB was already initialized..."
fi

# Start Admin & Logging Service
python3 scripts/cmsLogService 0   | tee -a /var/log/cms/logservice &
python3 scripts/cmsAdminWebServer | tee -a /var/log/cms/adminserver &
sleep 4

# Import all required contest data
find /root/cms-data/ -type f -name '.itime*' -delete
python3 cmscontrib/ImportUser.py --all -L italy_yaml /root/cms-data/
contest_out=$(python3 cmscontrib/ImportContest.py -i -u -U -L italy_yaml /root/cms-data/)
contest_id=($(echo $contest_out | sed -nr 's/.*\(new contest id: ([0-9]+)\)\.$/\1/p'))

# Install python packages which are needed for the assignments
if [ -f "/root/cms-data/requirements.txt" ]; then
  echo "Python package requirements for assignments found. Installing..."
  pip3 install -r /root/cms-data/requirements.txt
else
  echo "No Python package requirements found for assignments."
fi

# Run Contest, Scoring & Evaluation Services to setup grading environment
python3 scripts/cmsContestWebServer -c $contest_id  | tee -a /var/log/cms/contestserver &
python3 scripts/cmsScoringService -c $contest_id    | tee -a /var/log/cms/scoringservice &
python3 scripts/cmsEvaluationService -c $contest_id | tee -a /var/log/cms/evaluationservice &

# Initialize worker nodes (number of workers are obtained from cms-config/cms.conf)
worker=$(python3 scripts/getconf.py number_of_workers)
for i in $(seq 1 $worker); do
  python3 scripts/cmsWorker $i | tee -a /var/log/cms/worker$i &
done

wait
