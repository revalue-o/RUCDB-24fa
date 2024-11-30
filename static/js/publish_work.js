document.getElementById('homework-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    try {
        const response = await fetch(`/course/${courseName}/publish_work`, {
            method: 'POST',
            body: formData  // FormData不需要设置Content-Type，浏览器会自动设置
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            alert('作业发布成功！');
            this.reset();
        } else {
            alert(result.message || '发布失败，请重试');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('发布失败，请稍后重试');
    }
});


