(() => {
    // Progressive enhancement for capability filters and FAQ disclosures.
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
        const answer = document.getElementById(button.getAttribute('aria-controls'));
        if (!answer) return;
        answer.hidden = button.getAttribute('aria-expanded') !== 'true';
        button.disabled = false;
        button.addEventListener('click', () => {
            const open = button.getAttribute('aria-expanded') === 'true';
            button.setAttribute('aria-expanded', String(!open));
            answer.hidden = open;
        });
    });

    // The planner keeps all data in the browser and composes a plaintext mailto.
    const form = document.querySelector('[data-project-planner]');
    if (!form) return;
    const emailLink = document.querySelector('[data-email-project]');
    if (!emailLink) return;
    const summaryFields = ['need', 'budget', 'completion', 'disruption'];
    const summary = Object.fromEntries(summaryFields.map(name => [name, document.querySelector(`[data-summary="${name}"]`)]));
    const valueOf = name => String(form.elements[name]?.value || '').trim() || 'Not specified';
    const update = () => {
        summaryFields.forEach(name => { if (summary[name]) summary[name].textContent = valueOf(name); });
        const subject = encodeURIComponent(`Project brief — ${valueOf('need')}`);
        const body = encodeURIComponent([
            `Name: ${valueOf('name')}`,
            `Email: ${valueOf('email')}`,
            `Organization: ${valueOf('organization')}`,
            `Phone: ${valueOf('phone')}`,
            `Preferred contact: ${valueOf('contact_method')}`,
            `Primary need: ${valueOf('need')}`,
            `Budget range: ${valueOf('budget')}`,
            `Desired completion date: ${valueOf('completion')}`,
            `People affected: ${valueOf('people')}`,
            `Existing systems/tools: ${valueOf('systems')}`,
            `Current disruption: ${valueOf('disruption')}`,
            `Optional URL: ${valueOf('url')}`,
            '',
            'Problem and desired outcome:',
            valueOf('details')
        ].join('\n'));
        emailLink.href = `mailto:chad@goredtech.com?subject=${subject}&body=${body}`;
    };
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    form.addEventListener('submit', event => {
        event.preventDefault();
        update();
        window.location.href = emailLink.href;
    });
    const requestedNeed = new URLSearchParams(window.location.search).get('need');
    if (requestedNeed) {
        const option = Array.from(form.elements.need.options).find(item => item.value === requestedNeed);
        if (option) form.elements.need.value = requestedNeed;
    }
    update();
})();