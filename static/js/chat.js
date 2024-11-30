
document.addEventListener('DOMContentLoaded', function() {
    const chatToggle = document.getElementById('chatToggle');
    const chatPanel = document.getElementById('chatPanel');
    const dragHandle = document.getElementById('dragHandle');
    let isDragging = false;
    let startX;
    let startWidth;

    // 切换面板显示/隐藏
    chatToggle.addEventListener('click', function() {
        chatPanel.classList.toggle('open');
        const width = chatPanel.offsetWidth;
        if (chatPanel.classList.contains('open')) {
            chatPanel.style.right = '0';
        } else {
            chatPanel.style.right = `-${width}px`;
        }
    });

    // 拖拽调整宽度
    dragHandle.addEventListener('mousedown', function(e) {
        isDragging = true;
        startX = e.clientX;
        startWidth = parseInt(getComputedStyle(chatPanel).width, 10);
        
        document.body.classList.add('dragging');
    });

    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;

        const deltaX = startX - e.clientX;
        let newWidth = startWidth + deltaX;

        // 限制最小和最大宽度
        const maxWidth = window.innerWidth * 0.67;
        newWidth = Math.max(280, Math.min(maxWidth, newWidth));
        
        chatPanel.style.width = `${newWidth}px`;
        chatPanel.style.right = chatPanel.classList.contains('open') ? '0' : `-${newWidth}px`;
    });

    document.addEventListener('mouseup', function() {
        if (isDragging) {
            isDragging = false;
            document.body.classList.remove('dragging');
        }
    });

    // 保存宽度到本地存储
    window.addEventListener('beforeunload', function() {
        const width = chatPanel.style.width;
        if (width) {
            localStorage.setItem('chatPanelWidth', width);
        }
    });

    // 恢复上次保存的宽度
    const savedWidth = localStorage.getItem('chatPanelWidth');
    if (savedWidth) {
        chatPanel.style.width = savedWidth;
        chatPanel.style.right = chatPanel.classList.contains('open') ? '0' : `-${savedWidth}`;
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const chatContent = document.getElementById('chatContent');
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendMessage');

    function loadChatHistory() {
        const chatHistory = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        chatHistory.forEach(msg => {
            appendMessage(msg.content, msg.type, false);
        });
        // 滚动到最新消息
        chatContent.scrollTop = chatContent.scrollHeight;
    }

    // 保存消息到 localStorage
    function saveChatHistory(message, type) {
        const chatHistory = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        chatHistory.push({
            content: message,
            type: type,
            timestamp: new Date().getTime()
        });
        // 可以限制历史记录数量，比如只保留最近50条
        if (chatHistory.length > 50) {
            chatHistory.shift();
        }
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    }

    // 修改 appendMessage 函数
    function appendMessage(message, type, save = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        messageDiv.textContent = message;
        chatContent.appendChild(messageDiv);
        
        // 滚动到最新消息
        chatContent.scrollTop = chatContent.scrollHeight;
        
        // 保存到本地存储
        if (save) {
            saveChatHistory(message, type);
        }
    }
    // 发送消息的函数
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        
        try {
            const response = await fetch('/chatBOT', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (response.ok) {
                const data = await response.json();
                // 处理成功响应
                appendMessage(message, 'user');
                appendMessage(data.message, 'bot');
                chatInput.value = ''; // 清空输入框
            } else if (response.status === 401 || response.redirected) {
                window.location.href = '/index';
            } else {
                appendMessage('消息发送失败,请重试', 'bot')
            }
        } catch (error) {
            console.error('Error:', error);
            if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                window.location.href = '/index';
            } else {
                appendMessage('发送失败，请重试', 'bot');
            }
        }
    }

    // 点击发送按钮
    sendButton.addEventListener('click', sendMessage);

    // 监听回车键
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) { // 按下回车但不按Shift
            e.preventDefault(); // 阻止默认的换行行为
            sendMessage();
        }
    });

    function addClearButton() {
        const clearButton = document.createElement('button');
        // 使用 Material Icons 的删除图标替代文本
        clearButton.innerHTML = '<span class="material-icons">cleaning_services</span>';
        clearButton.className = 'clear-chat-btn';
        clearButton.onclick = function() {
            localStorage.removeItem('chatHistory');
            chatContent.innerHTML = '<h4 style="border-bottom: 1px solid #e0e0e0; padding-bottom: 10px; margin-bottom: 15px;">CHAT</h4>';
        };
        chatContent.parentElement.insertBefore(clearButton, chatContent);
    }

    loadChatHistory();
    addClearButton();
});