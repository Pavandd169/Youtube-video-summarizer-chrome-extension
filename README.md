# Youtube-video-summarizer-chrome-extension

## How to Use - Follow the 2 steps

1. Backend (required)
docker pull pavandd1/youtube-video-summarizer-chrome-extension
docker run -p 8000:8000 pavandd1/youtube-video-summarizer-chrome-extension

2. 
a. Open chrome://extensions
b. Enable Developer Mode
c. Click "Load unpacked"
d. Select the `extension/` folder


### PROJECT DETAILS

## Purpose 

This is a chrome extension which creates a summary and key points of a video in youtube on the webpage. The purpose of the project is to save time reading the summary before watching any long video to understand what is majorly focusedin the video

## Constraints
1. Supports only english captions containing videos - (also supports for videos having auto generated captions)
2. The length of the video for getting a reliable summary could be at maximum 1-2 hrs

## How it works
The captions are fetched through API and fed into Qwen2.5-1.5B LLM into chunks which creates a summary and key points all in the local environment. 

## Next version - v2.0
1. Intgrating gpt 4o model using API for faster and reliable results
2. Reducing the processing time for longer videos
