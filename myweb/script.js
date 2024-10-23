document.getElementById('header').addEventListener('click', function(e) {
    for (let i = 0; i < 10; i++) {
        createStar(e.pageX, e.pageY);
    }
});

function createStar(x, y) {
    const star = document.createElement('div');
    star.className = 'star';
    document.body.appendChild(star);

    // 随机大小
    const size = Math.random() * 15 + 5 + 'px';
    star.style.width = size;
    star.style.height = size;

    // 随机颜色
    const color = `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.8)`;
    star.style.backgroundColor = color;

    // 设置位置
    star.style.left = x + 'px';
    star.style.top = y + 'px';

    // 动画效果
    setTimeout(() => {
        star.style.transform = `translate(${(Math.random() - 0.5) * 200}px, ${(Math.random() - 0.5) * 200}px) scale(1.5)`;
        star.style.opacity = 1;
    }, 10); // 小延迟以确保动画生效

    // 淡出效果
    setTimeout(() => {
        star.style.transform += ' scale(0)';
        star.style.opacity = 0;
    }, 300);

    // 移除星星
    setTimeout(() => document.body.removeChild(star), 800);
}
