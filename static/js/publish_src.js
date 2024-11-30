document.addEventListener('DOMContentLoaded', function() {
    const selectFileBtn = document.getElementById('selectFileBtn');
    const fileInput = document.getElementById('fileInput');

    // 点击按钮触发文件选择
    selectFileBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // 文件选择后直接上传
    fileInput.addEventListener('change', async () => {
        if (!fileInput.files.length) return;

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        try {
            selectFileBtn.textContent = '上传中...';
            selectFileBtn.disabled = true;

            const response = await fetch(`/upload_file/${courseName}/src`, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                alert('文件上传成功！');
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