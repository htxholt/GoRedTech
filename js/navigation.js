// Mark JavaScript availability before CSS renders so mobile navigation has no layout flash.
document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', () => {
    // One accessible navigation state shared across every generated page.
    const toggle = document.querySelector('.menu-toggle');
    const menu = document.querySelector('.primary-nav');
    if (!toggle || !menu) return;

    const closeMenu = () => {
        toggle.setAttribute('aria-expanded', 'false');
        toggle.querySelector('.sr-only').textContent = 'Open navigation';
        menu.classList.remove('is-open');
        document.body.classList.remove('menu-open');
    };

    toggle.addEventListener('click', () => {
        const open = toggle.getAttribute('aria-expanded') !== 'true';
        toggle.setAttribute('aria-expanded', String(open));
        toggle.querySelector('.sr-only').textContent = open ? 'Close navigation' : 'Open navigation';
        menu.classList.toggle('is-open', open);
        document.body.classList.toggle('menu-open', open);
    });
    menu.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
    window.addEventListener('resize', () => { if (window.innerWidth > 900) closeMenu(); });
});