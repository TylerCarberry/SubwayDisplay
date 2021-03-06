#!/bin/sh

disable_screensaver() {
  stop framework
  lipc-set-prop -i com.lab126.powerd preventScreenSaver 1
  lipc-set-prop com.lab126.pillow disableEnablePillow disable
}

enable_screensaver() {
  start framework
  lipc-set-prop -i com.lab126.powerd preventScreenSaver 0
  lipc-set-prop com.lab126.pillow disableEnablePillow enable
}

# Download the image from the server
# The kindle is missing SSL libraries and curl only works with http, not https
download_image() {
  file_name=$1
  url=$2

  remove_file_if_exists "$file_name"

  # The key is used to prevent caching
  current_timestamp=$(date '+%s')
  curl -H 'Cache-Control: no-cache' $url?key=$current_timestamp > "$file_name"
}

remove_file_if_exists() {
  file_name=$1
  [ -f "$file_name" ] && rm "$file_name"
}

update_this_file() {
  temp_file_name=/mnt/us/subway/temp_refresh_display.sh
  actual_file_name=/mnt/us/subway/refresh_display.sh
  minimum_file_size_bytes=1000

  remove_file_if_exists $temp_file_name

  current_timestamp=$(date '+%s')
  curl -H 'Cache-Control: no-cache' http://storage.googleapis.com/subwaykindledisplay/refresh_display.sh?key=$current_timestamp > $temp_file_name

  if [ -f "$temp_file_name" ]; then
    actualsize=$(wc -c < "$temp_file_name")
    if [ $actualsize -ge $minimum_file_size_bytes ]; then
      remove_file_if_exists $actual_file_name
      mv $temp_file_name $actual_file_name
    fi

  fi
}

update_no_wifi_logo() {
  temp_file_name=/mnt/us/subway/temp_no_wifi.png
  actual_file_name=/mnt/us/subway/no_wifi.png
  minimum_file_size_bytes=1000

  remove_file_if_exists $temp_file_name

  current_timestamp=$(date '+%s')
  curl -H 'Cache-Control: no-cache' http://storage.googleapis.com/subwaykindledisplay/no_wifi.png?key=$current_timestamp > $temp_file_name

  if [ -f "$temp_file_name" ]; then
    actualsize=$(wc -c < "$temp_file_name")
    if [ $actualsize -ge $minimum_file_size_bytes ]; then
      remove_file_if_exists $actual_file_name
      mv $temp_file_name $actual_file_name
    fi
  fi
}

partially_refresh_screen() {
  file_name=$1
  minimum_file_size_bytes=1000

  actualsize=$(wc -c < "$file_name")
  # If the file is large enough
  if [ $actualsize -ge $minimum_file_size_bytes ]; then
    eips -g $file_name
  else
    eips -g no_wifi.png
  fi
}

# -f causes a full image refresh
# -g indicates the image is a jpg/png. -b for bitmap images
fully_refresh_screen() {
  file_name=$1
  minimum_file_size_bytes=1000

  actualsize=$(wc -c < "$file_name")
  # If the file is large enough
  if [ $actualsize -ge $minimum_file_size_bytes ]; then
    eips -f -g $file_name
  else
    eips -f -g no_wifi.png
  fi
}

enable_wifi() {
  lipc-set-prop com.lab126.cmd wirelessEnable 1
}

disable_wifi() {
  lipc-set-prop com.lab126.cmd wirelessEnable 0
}

# Reboot the device every day at 4 AM
currenttime=$(date +%H:%M)

cd "$(dirname "$0")" || exit
#enable_screensaver
disable_screensaver

enable_wifi

# Give the server time to generate the images and for the wifi to connect
# It usually takes 20 seconds
sleep 30

download_image image0.png http://storage.googleapis.com/subwaykindledisplay/image0.png
download_image image1.png http://storage.googleapis.com/subwaykindledisplay/image1.png
download_image image2.png http://storage.googleapis.com/subwaykindledisplay/image2.png
download_image image3.png http://storage.googleapis.com/subwaykindledisplay/image3.png
download_image image4.png http://storage.googleapis.com/subwaykindledisplay/image4.png
update_this_file
update_no_wifi_logo
#disable_wifi

fully_refresh_screen image0.png
sleep 60
partially_refresh_screen image1.png
sleep 60
partially_refresh_screen image2.png
sleep 60
partially_refresh_screen image3.png
sleep 60
partially_refresh_screen image4.png

if [ "$currenttime" = "04:00" ]; then
  reboot
fi
