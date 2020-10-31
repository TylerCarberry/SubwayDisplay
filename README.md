# Kindle Subway Display
Displays subway arrival times on a Kindle Touch


<img width="450" alt="Example screenshot" src="https://user-images.githubusercontent.com/6628497/97786594-03011380-1b83-11eb-8dd2-4eaa0f7516c0.png">     - - - -    <img width="450" alt="Example covid overnight" src="https://user-images.githubusercontent.com/6628497/97786660-799e1100-1b83-11eb-91fc-083481a92e99.png">



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

