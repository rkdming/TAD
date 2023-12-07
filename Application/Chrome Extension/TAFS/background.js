// background.js

function getYouTubeVideoID(url) {
  const youtubeRegex = /(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:shorts\/|watch\?v=|embed\/))([^&=%\?]{11})/;
  const matches = youtubeRegex.exec(url);
  if (matches) {
    return matches[1];
  }
  return null;
}

let popupOpen = false;
let pausedTabId = null;




chrome.webNavigation.onCompleted.addListener(function (details) {
  console.log('youtube page');
  const videoID = getYouTubeVideoID(details.url);

  chrome.storage.local.get(['FI', 'FL', 'VI', 'CC', 'CR'], function (result) {

    // 선택된 카테고리들을 배열로 변환
    var selectedCategories = Object.keys(result).filter(key => result[key]);

    // if 문 추가해야 됨. selectedCategroies.length != 0 일 때 서버에 요청 보내기
    if (selectedCategories.length != 0) {
      // 서버에 요청
      if (videoID) {
        fetch('http://localhost:8080/extension2.php', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: 'videoID=' + encodeURIComponent(videoID) + '&categories=' + encodeURIComponent(JSON.stringify(selectedCategories))
        })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            console.log(data);

            data.forEach(item => {
              const title = item.title;
              const category = item.category;

              // title과 category 저장 -> warning.js 에서 출력
              chrome.storage.local.set({ 'videoTitle': title, 'videoCategory': category });
              console.log('Title:', title, 'Category:', category);
            });

            console.log('check and puase video');
            chrome.tabs.sendMessage(details.tabId, { action: 'checkAndPauseVideo' }); // 비디오 일시정지 요청 보내기
          })
          .catch(error => {
            console.error('Fetch error:', error);
          });
      }
    }


  });

});


chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  // 다른 탭에서 log 남기는 거 출력
  if (request.type === 'log') {
    //console.log('Log from', sender.tab ? 'Tab:' + sender.tab.id : 'Extension', '-', request.message);
    console.log(request.message);
  }
  
  if (request.action === 'videoPaused') {
    console.log('videoPaused');
    setTimeout(function () {
      if (!popupOpen) {
        popupOpen = true;
        pausedTabId = sender.tab.id;

        // 경고 창 생성
        chrome.windows.create({
          url: chrome.runtime.getURL('warningWindow.html'),
          type: 'popup',
          focused: true,
          top: 100,
          left: 750,
          width: 700,
          height: 900,
        }, function (createdWindow) {
          chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
            if (request.action === 'resumeClicked') {
              console.log('resumeClicked');
              popupOpen = false;
              chrome.tabs.sendMessage(pausedTabId, { action: 'resumeVideo' });
            } else if (request.action === 'skipClicked') {
              console.log('skipClicked');
              popupOpen = false;
              chrome.tabs.sendMessage(pausedTabId, { action: 'skipVideo' });
            }
          });
          chrome.windows.onRemoved.addListener(function (windowId) {
            console.log('destory window');
            popupOpen = false;
          });
        })
      }
    }, 500);

  }
  sendResponse({});
});
