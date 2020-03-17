#!/usr/bin/env bash

echo "Starting CMS services..."
cd /root/cms
python3 scripts/cmsInitDB

# Create/Update admin account
python3 cmscontrib/AddAdmin.py $(python3 config/getconf.py admin_user) -p  $(python3 config/getconf.py admin_password)

# Install all course packages for all courses
for c_dir in /root/cms-data/*/ ; do
    pip3 install -r ${c_dir}requirements.txt
done

# Start Logging Service
python3 scripts/cmsLogService 0   | tee -a /var/log/cms/logservice &
python3 scripts/cmsAdminWebServer | tee -a /var/log/cms/adminserver &

sleep 4

declare -a contest_ids=()

# Install all course packages for all courses
for c_dir in /root/cms-data/* ; do
    if [ -d "$c_dir" ]; then
        find $c_dir -type f -name '.itime*' -delete
        python3 cmscontrib/ImportUser.py --all -L italy_yaml ${c_dir}
        contest_out=$(python3 cmscontrib/ImportContest.py -i -u -U -L italy_yaml ${c_dir})
        contest_ids+=($(echo $contest_out | sed -nr 's/.*\(new contest id: ([0-9]+)\)\.$/\1/p'))
    fi
done

for id in "${contest_ids[@]}" ; do
    python3 scripts/cmsContestWebServer -c $id  | tee -a /var/log/cms/contestserver &
    python3 scripts/cmsScoringService -c $id    | tee -a /var/log/cms/scoringservice &
    python3 scripts/cmsEvaluationService -c $id | tee -a /var/log/cms/evaluationservice &    
done

wait
