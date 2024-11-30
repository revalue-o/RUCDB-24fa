document.getElementById('announcement-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const content = form.querySelector('textarea').value;
    
    try {
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `content=${encodeURIComponent(content)}`
        });
        
        if (response.ok) {
            alert('公告发布成功！');
        } else {
            alert('发布失败，请重试');
        }
    } catch (err) {
        console.error('Error:', err);
        alert('发布失败，请重试');
    }
});