// warningWindow.js



function changeCat(DBcategory) {
  var dic = {}
  dic['FI'] = 'fire';
  dic['FL'] = 'flooding';
  dic['VI'] = 'violence';
  dic['CC'] = 'car crash';

  var cat = dic[DBcategory];

  return cat;
}

document.addEventListener('DOMContentLoaded', function () {

  chrome.runtime.sendMessage({ type: "log", message: "warn : DomLoaded" });

  // 사용자가 선택한 카테고리 가져오기
  chrome.storage.local.get(['videoTitle', 'videoCategory'], function (data) {
    if (data.videoTitle && data.videoCategory) {
      console.log('from wwjs Title:', data.videoTitle, 'Category:', data.videoCategory);
      cat = changeCat(data.videoCategory);

      // html 경고 메시지 변경
      var msg = 'This Video(' + data.videoTitle + ') contains ' + cat;
      document.getElementById('warning').textContent = msg;

    }
  });


  var resumeButton = document.getElementById('resumeButton');
  if (resumeButton) {
    resumeButton.addEventListener('click', function () {
      chrome.runtime.sendMessage({ type: "log", message: "warn : resume video" });
      chrome.runtime.sendMessage({ action: 'resumeClicked' });

      // windlow.close에 delay
      setTimeout(function() {
        window.close();
      }, 100);
    });
  }

  var skipButton = document.getElementById('skipButton');
  if (skipButton) {
    skipButton.addEventListener('click', function () {
      chrome.runtime.sendMessage({ type: "log", message: "warn : skip video" });
      chrome.runtime.sendMessage({ action: 'skipClicked' });

      setTimeout(function() {
        window.close();
      }, 100);
    });
  }
});
