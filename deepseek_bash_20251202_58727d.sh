# בדוק סטטוס
curl http://A2-MONITORING-IP:3000

# בדוק GPU
ssh root@VASTAI-INSTANCE-IP "nvidia-smi"

# בדוק SIREG
ssh root@VASTAI-INSTANCE-IP "cat /etc/sireg_ip.txt"