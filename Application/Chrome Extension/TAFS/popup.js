document.addEventListener('DOMContentLoaded', function() {
    var checkboxes = document.querySelectorAll('input[name="category"]');

    checkboxes.forEach(function(checkbox) {
        // 초기 상태 불러오기
        chrome.storage.local.get(checkbox.value, function(result) {
            checkbox.checked = result[checkbox.value] || false;
        });

        // 상태 변경 감지
        checkbox.addEventListener('change', function() {
            var storageObject = {};
            storageObject[checkbox.value] = checkbox.checked;
            chrome.storage.local.set(storageObject);
        });
    });
});