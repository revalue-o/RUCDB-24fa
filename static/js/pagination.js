document.addEventListener('DOMContentLoaded', function() {
    let currentPage = 1;
    const pageSize = 10; // 每页显示数量
    const contentItems = document.querySelectorAll('.content-item');
    const totalPages = Math.ceil(contentItems.length / pageSize);

    // 初始化页面
    updatePage();

    // 更新页面显示
    function updatePage() {
        // 计算当前页的开始和结束索引
        const startIndex = (currentPage - 1) * pageSize;
        const endIndex = Math.min(startIndex + pageSize, contentItems.length);

        // 隐藏所有内容
        contentItems.forEach(item => {
            item.style.display = 'none';
        });

        // 显示当前页的内容
        for(let i = startIndex; i < endIndex; i++) {
            contentItems[i].style.display = 'block';
        }

        // 更新页码信息
        document.getElementById('page-info').textContent = `${currentPage} / ${totalPages}`;

        // 更新按钮状态
        document.getElementById('prev-btn').disabled = currentPage === 1;
        document.getElementById('next-btn').disabled = currentPage === totalPages;
    }

    // 上一页
    window.previousPage = function() {
        if (currentPage > 1) {
            currentPage--;
            updatePage();
        }
    }

    // 下一页
    window.nextPage = function() {
        if (currentPage < totalPages) {
            currentPage++;
            updatePage();
        }
    }
});