document.addEventListener('DOMContentLoaded', function() {
    const joinButtons = document.querySelectorAll('.join-btn');
    
    joinButtons.forEach(button => {
        button.addEventListener('click', function() {
            const courseName = this.getAttribute('data-course');
            const teacherName = this.getAttribute('data-teacher');
            
            fetch('/courses_square', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    course: courseName,
                    teacher: teacherName
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('申请成功！');
                    this.disabled = true;
                    this.textContent = '已申请';
                } else {
                    alert(data.message || '申请失败，请重试');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('申请失败，请重试');
            });
        });
    });
});