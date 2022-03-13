# Kindle Subway Display
Displays subway arrival times on a Kindle Touch


<img width="400" alt="Without frame" src="https://user-images.githubusercontent.com/6628497/158081248-ed2de740-1d91-4238-b835-28ccdffb461d.jpg"> <img width="400" alt="With frame" src="https://user-images.githubusercontent.com/6628497/158081268-eeabc0e9-fbc7-44aa-93c8-01c449148b56.jpg">


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

