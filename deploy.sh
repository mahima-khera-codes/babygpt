rm -rf gunicorn-nf--access.log.*
rm -rf gunicorn-nf--error.log.*
git pull origin dev_branch
source ../myenv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart hr-staging-notify
