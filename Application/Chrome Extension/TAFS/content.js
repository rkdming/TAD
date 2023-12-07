// content.js

chrome.runtime.onMessage.addListener(async function (request, sender, sendResponse) {
    if (request.action === 'checkAndPauseVideo') { //동영상 일시 정지
      chrome.runtime.sendMessage({type: "log", message: "con : pause video"});
      const videoElements = document.getElementsByTagName('video');
      for (let i = 0; i < videoElements.length; i++) {
        try {
          videoElements[i].pause();
        } catch (e) {
        }
      }
      chrome.runtime.sendMessage({ action: 'videoPaused' });
    } else if (request.action === 'resumeVideo') {
      chrome.runtime.sendMessage({type: "log", message: "con : resume video"});
      const videoElements = document.getElementsByTagName('video');
      for (let i = 0; i < videoElements.length; i++) {
        try {
          videoElements[i].play();
        } catch (e) {
        }
      }
    } else if (request.action === 'skipVideo') {
      chrome.runtime.sendMessage({type: "log", message: "con : skip video"});
      if (window.location.href.includes('youtube.com/shorts')) {
        chrome.runtime.sendMessage({type: "log", message: "skip video - reload shorts"});
        window.location.href = 'https://www.youtube.com/shorts';
      } else {
        chrome.runtime.sendMessage({type: "log", message: "skip video - next video"});
        const nextButton = document.querySelector('.ytp-next-button');
        if (nextButton) {
          nextButton.click();
        }
      }
    }
  
    sendResponse({});
  });