#!/bin/sh

FULL_REFRESH_INTERVAL_MINUTES=10
DOWNLOADED_IMAGE_FILE_NAME=image.png
IMAGE_URL=http://storage.googleapis.com/subwaykindledisplay/image.png

download_successful=1

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
  # Remove the file if it exists
  [ -f $DOWNLOADED_IMAGE_FILE_NAME ] && rm $DOWNLOADED_IMAGE_FILE_NAME

  # The key is used to prevent caching
  current_timestamp=$(date '+%s')
  #curl -H 'Cache-Control: no-cache' $IMAGE_URL?key=$current_timestamp > $DOWNLOADED_IMAGE_FILE_NAME

  if curl -H 'Cache-Control: no-cache' $IMAGE_URL?key=$current_timestamp > $DOWNLOADED_IMAGE_FILE_NAME
    then download_successful=1
    else download_successful=0
  fi
}

partially_refresh_screen() {
  eips -g $DOWNLOADED_IMAGE_FILE_NAME
}

# -f causes a full image refresh
# -g indicates the image is a jpg/png. -b for bitmap images
fully_refresh_screen() {
  eips -f -g $DOWNLOADED_IMAGE_FILE_NAME
}

enable_wifi() {
  lipc-set-prop com.lab126.cmd wirelessEnable 1
}

disable_wifi() {
  lipc-set-prop com.lab126.cmd wirelessEnable 0
}

cd "$(dirname "$0")" || exit
enable_screensaver
#disable_screensaver

enable_wifi
sleep 15
download_image
disable_wifi

#if $download_successful
#  then disable_screensaver
#  else enable_screensaver
#fi

# Display the image
current_minute=$(date +"%M")
if [ $((current_minute%$FULL_REFRESH_INTERVAL_MINUTES)) -eq 0 ];
then
    fully_refresh_screen
else
    partially_refresh_screen
fi

#sleep 20
#download_image
#partially_refresh_screen
