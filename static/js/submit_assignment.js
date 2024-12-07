document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.getElementById('submit-btn');
    const fileInput = document.getElementById('fileInput');
    const assignmentName = submitBtn.getAttribute('data-aname');

    // 点击按钮触发文件选择
    submitBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // 文件选择后直接上传
    fileInput.addEventListener('change', async () => {
        if (!fileInput.files.length) return;

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        try {
            submitBtn.texContent = '上传中...';
            submitBtn.disabled = true;

            const response = await fetch(`/submit_assignment/${courseName}/${assignmentName}`, {
                method:'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                alert('文件上传成功！');
                window.location.reload();
            } else {
                alert('上传失败：' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('上传失败，请重试');
        } finally {
            // 重置按钮状态和文件输入
            selectFileBtn.textContent = '点击选择文件';
            selectFileBtn.disabled = false;
            fileInput.value = '';
        }
    });
});