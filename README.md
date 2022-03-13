# Kindle Subway Display
Displays subway arrival times on a Kindle Touch


<img width="400" alt="Without frame" src="https://user-images.githubusercontent.com/6628497/158081248-ed2de740-1d91-4238-b835-28ccdffb461d.jpg"> <img width="400" alt="With frame" src="https://user-images.githubusercontent.com/6628497/158081563-1438675a-34e7-43cb-b7b3-100979e586f7.jpg">

Setting up the Kindle
- Follow the instructions from https://youtu.be/Oel08SDFyIY


Add this line to crontab
```
*/1  * * * * /mnt/us/subway/refresh_display.sh      
```

Useful commands

- Connect to the kindle  
`ssh root@192.168.15.244`

- Enable read/write file system  
`mntroot rw`

- Edit crontab  
`nano /etc/crontab/root`

