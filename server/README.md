rm output.png output2.png image-with-border.png
gcloud builds submit --tag gcr.io/subwaydisplay/helloworld
gcloud run deploy --image gcr.io/subwaydisplay/helloworld --platform managed