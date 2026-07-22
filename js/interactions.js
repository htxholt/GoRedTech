(() => {
    const filters = document.querySelectorAll('[data-service-filter]');
    const services = document.querySelectorAll('[data-service-category]');
    const serviceGrid = document.querySelector('.service-grid');
    filters.forEach(button => button.addEventListener('click', () => {
        const selected = button.dataset.serviceFilter;
        filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        services.forEach(card => { card.hidden = selected !== 'all' && card.dataset.serviceCategory !== selected; });
        serviceGrid?.classList.toggle('is-filtered', selected !== 'all');
    }));

    document.querySelectorAll('.faq-question').forEach(button => {
        button.addEventListener('click', () => {
            const answer = document.getElementById(button.getAttribute('aria-controls'));
            const open = button.getAttribute('aria-expanded') === 'true';
            button.setAttribute('aria-expanded', String(!open));
            answer.hidden = open;
        });
    });

    const form = document.querySelector('[data-project-planner]');
    if (!form) return;
    const summary = {
        service: document.querySelector('[data-summary="service"]'),
        timeline: document.querySelector('[data-summary="timeline"]'),
        organization: document.querySelector('[data-summary="organization"]')
    };
    const emailLink = document.querySelector('[data-email-project]');
    const read = name => form.elements[name]?.value.trim() || 'Not specified';
    const update = () => {
        summary.service.textContent = read('service');
        summary.timeline.textContent = read('timeline');
        summary.organization.textContent = read('organization');
        const subject = encodeURIComponent(`IT consultation request — ${read('service')}`);
        const body = encodeURIComponent([
            `Name: ${read('name')}`, `Organization: ${read('organization')}`,
            `Phone: ${read('phone')}`, `Service: ${read('service')}`,
            `Timeline: ${read('timeline')}`, '', 'Project details:', read('details')
        ].join('\n'));
        emailLink.href = `mailto:chad@goredtech.com?subject=${subject}&body=${body}`;
    };
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    form.addEventListener('submit', event => { event.preventDefault(); update(); window.location.href = emailLink.href; });
    update();
})();
