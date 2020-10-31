# SubwayDisplay
Displays subway arrival times on a Kindle Touch

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

