document.addEventListener('DOMContentLoaded', () => {
    const btnMenu = document.getElementById('btn-menu');
    const btnFecharMenu = document.getElementById('btn-fechar-menu');
    const menuLateral = document.getElementById('menu-lateral');

    btnMenu.addEventListener('click', () => {
        menuLateral.classList.add('open');
        document.body.style.overflow = 'hidden';
    });

    btnFecharMenu.addEventListener('click', () => {
        menuLateral.classList.remove('open');
        document.body.style.overflow = '';
    });

    window.addEventListener('click', (e) => {
        if (menuLateral.classList.contains('open') &&
            !menuLateral.contains(e.target) &&
            e.target.id !== 'btn-menu') {
            menuLateral.classList.remove('open');
            document.body.style.overflow = '';
        }
    });
});
