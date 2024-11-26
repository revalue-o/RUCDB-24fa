window.addEventListener('scroll', function () {
    const headerBar = document.querySelector('.header-bar');
    const chatPanel = document.getElementById('chatPanel');
    const chatToggleContainer = document.querySelector('.chat-toggle-container');

    if (window.scrollY > 50) {  // 滚动超过50px时
        headerBar.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';  // 半透明黑色背景
        headerBar.style.backdropFilter = 'blur(5px)';  // 毛玻璃效果

        chatToggleContainer.style.top = '64px';
    } else {  // 回到顶部时
        headerBar.style.backgroundColor = 'transparent';
        headerBar.style.backdropFilter = 'none';

        chatToggleContainer.style.top = '160px';
    }
});